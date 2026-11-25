"""SunWatch: Solar PV Performance Monitor and Fault Alert Dashboard.

Educational project for Electrical Engineering students. The dashboard compares
measured PV output with a simple temperature-corrected expected-power model.
It is a learning/demo tool, not a certified protection or diagnostic system.
"""

from pathlib import Path
from typing import List

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


APP_DIR = Path(__file__).resolve().parent
SAMPLE_FILE = APP_DIR / "data" / "sample_solar_data.csv"
REQUIRED_COLUMNS: List[str] = [
    "timestamp",
    "irradiance_Wm2",
    "module_temp_C",
    "voltage_V",
    "current_A",
]


@st.cache_data
def load_sample_data() -> pd.DataFrame:
    """Load the sample CSV shipped with the project."""
    return pd.read_csv(SAMPLE_FILE)


def validate_and_prepare(raw: pd.DataFrame) -> pd.DataFrame:
    """Validate the uploaded data and return a cleaned copy."""
    missing = [column for column in REQUIRED_COLUMNS if column not in raw.columns]
    if missing:
        raise ValueError("Missing required column(s): " + ", ".join(missing))

    df = raw[REQUIRED_COLUMNS].copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    numeric_columns = REQUIRED_COLUMNS[1:]
    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    df = df.dropna(subset=REQUIRED_COLUMNS).sort_values("timestamp")
    if df.empty:
        raise ValueError("No valid rows found. Check the timestamp and numeric values.")
    if (df[["irradiance_Wm2", "voltage_V", "current_A"]] < 0).any().any():
        raise ValueError("Irradiance, voltage and current must not be negative.")
    if (df["irradiance_Wm2"] > 1400).any():
        raise ValueError("Irradiance above 1400 W/m² was found. Please check the CSV units.")
    return df.reset_index(drop=True)


def add_performance_calculations(
    df: pd.DataFrame,
    rated_capacity_kw: float,
    temperature_coefficient: float,
    system_efficiency: float,
    alert_threshold: float,
) -> pd.DataFrame:
    """Add measured power, modelled power, performance ratio and alert status."""
    result = df.copy()
    result["actual_power_W"] = result["voltage_V"] * result["current_A"]

    temperature_factor = 1 + temperature_coefficient * (result["module_temp_C"] - 25)
    temperature_factor = temperature_factor.clip(lower=0)
    irradiance_factor = result["irradiance_Wm2"] / 1000
    result["expected_power_W"] = (
        rated_capacity_kw * 1000 * irradiance_factor * temperature_factor * system_efficiency
    )

    result["performance_ratio"] = np.where(
        result["expected_power_W"] > 100,
        result["actual_power_W"] / result["expected_power_W"],
        np.nan,
    )
    result["status"] = np.where(
        (result["expected_power_W"] > 300)
        & (result["performance_ratio"] < alert_threshold),
        "Check performance",
        "Normal / low sunlight",
    )
    result["date"] = result["timestamp"].dt.date.astype(str)
    return result


def calculate_daily_energy(df: pd.DataFrame) -> pd.DataFrame:
    """Estimate daily energy using measured power and time between readings."""
    ordered = df.sort_values("timestamp").copy()
    intervals = ordered["timestamp"].diff().dt.total_seconds().div(3600)
    positive_intervals = intervals[(intervals > 0) & (intervals <= 2)]
    typical_interval = float(positive_intervals.median()) if not positive_intervals.empty else 0.25

    # Attribute each interval to the earlier reading. Limit large data gaps so
    # a missing afternoon of data is not counted as continuous generation.
    durations = ordered["timestamp"].shift(-1).sub(ordered["timestamp"]).dt.total_seconds().div(3600)
    durations.iloc[-1] = typical_interval
    durations = durations.clip(lower=0, upper=max(typical_interval * 2, 0.5))
    ordered["energy_kWh"] = ordered["actual_power_W"] * durations / 1000
    return ordered.groupby("date", as_index=False)["energy_kWh"].sum()


def main() -> None:
    st.set_page_config(
        page_title="SunWatch | Solar PV Monitor",
        page_icon="☀️",
        layout="wide",
    )

    st.title("☀️ SunWatch — Solar PV Performance Monitor")
    st.caption(
        "An Electrical Engineering mini-project: compare measured solar output with an "
        "expected-power model and highlight possible underperformance."
    )

    with st.sidebar:
        st.header("System settings")
        rated_capacity = st.number_input(
            "PV plant rated capacity (kW)", min_value=0.5, max_value=500.0,
            value=5.0, step=0.5,
        )
        temperature_coefficient = st.number_input(
            "Power temperature coefficient (1/°C)", min_value=-0.010,
            max_value=0.000, value=-0.004, step=0.001, format="%.3f",
            help="A typical illustrative value is around -0.004 per °C. Use your panel datasheet value for real analysis.",
        )
        system_efficiency = st.slider(
            "Model system efficiency", min_value=0.60, max_value=1.00,
            value=0.90, step=0.01,
            help="A simplified allowance for system losses. This is an assumption, not a measured value.",
        )
        alert_threshold = st.slider(
            "Underperformance alert threshold", min_value=0.50, max_value=0.95,
            value=0.75, step=0.05,
            help="An alert is raised when measured power is below this fraction of modelled power.",
        )
        st.divider()
        st.markdown("**Data source**")
        uploaded_file = st.file_uploader("Upload a PV readings CSV", type=["csv"])
        st.caption("No hardware is required. Start with the included demonstration dataset.")

    try:
        raw_data = pd.read_csv(uploaded_file) if uploaded_file is not None else load_sample_data()
        data = validate_and_prepare(raw_data)
    except Exception as exc:  # Show actionable errors instead of a traceback.
        st.error(f"Could not load the data: {exc}")
        st.info("Use the column names listed in the README and upload a valid CSV file.")
        st.stop()

    results = add_performance_calculations(
        data,
        rated_capacity_kw=float(rated_capacity),
        temperature_coefficient=float(temperature_coefficient),
        system_efficiency=float(system_efficiency),
        alert_threshold=float(alert_threshold),
    )
    daily_energy = calculate_daily_energy(results)

    sunlight_rows = results[results["expected_power_W"] > 300]
    average_pr = sunlight_rows["performance_ratio"].mean() if not sunlight_rows.empty else np.nan
    alert_rows = results[results["status"] == "Check performance"]
    total_energy = daily_energy["energy_kWh"].sum() if not daily_energy.empty else 0.0
    peak_power = results["actual_power_W"].max() if not results.empty else 0.0

    first_col, second_col, third_col, fourth_col = st.columns(4)
    first_col.metric("Estimated energy", f"{total_energy:,.2f} kWh")
    second_col.metric("Peak measured power", f"{peak_power:,.0f} W")
    third_col.metric("Average performance ratio", "—" if pd.isna(average_pr) else f"{average_pr:.1%}")
    fourth_col.metric("Performance alerts", f"{len(alert_rows):,}")

    st.subheader("Power output over time")
    power_chart = go.Figure()
    power_chart.add_trace(go.Scatter(
        x=results["timestamp"], y=results["expected_power_W"],
        mode="lines", name="Expected power (model)",
    ))
    power_chart.add_trace(go.Scatter(
        x=results["timestamp"], y=results["actual_power_W"],
        mode="lines", name="Measured power (V × I)",
    ))
    power_chart.update_layout(
        xaxis_title="Time", yaxis_title="Power (W)",
        legend_title="Series", height=390, margin=dict(l=10, r=10, t=25, b=10),
    )
    st.plotly_chart(power_chart, use_container_width=True)

    left, right = st.columns(2)
    with left:
        st.subheader("Daily energy generation")
        energy_chart = px.bar(
            daily_energy, x="date", y="energy_kWh",
            labels={"date": "Date", "energy_kWh": "Energy (kWh)"},
        )
        energy_chart.update_layout(height=330, margin=dict(l=10, r=10, t=20, b=10))
        st.plotly_chart(energy_chart, use_container_width=True)
    with right:
        st.subheader("Measured vs expected power")
        scatter = px.scatter(
            results[results["expected_power_W"] > 100],
            x="expected_power_W", y="actual_power_W", color="status",
            labels={"expected_power_W": "Expected power (W)", "actual_power_W": "Measured power (W)"},
        )
        scatter.update_layout(height=330, margin=dict(l=10, r=10, t=20, b=10))
        st.plotly_chart(scatter, use_container_width=True)

    st.subheader("Performance alerts")
    if alert_rows.empty:
        st.success("No underperformance alerts were detected in the selected data.")
    else:
        st.warning(
            f"{len(alert_rows)} reading(s) are below the selected threshold. "
            "Check sensor readings, shading, soiling, wiring and operating conditions. "
            "This dashboard does not identify the exact physical cause."
        )
        st.dataframe(
            alert_rows[["timestamp", "irradiance_Wm2", "module_temp_C", "actual_power_W", "expected_power_W", "performance_ratio"]]
            .assign(performance_ratio=lambda frame: frame["performance_ratio"].map(lambda value: f"{value:.1%}")),
            use_container_width=True,
            hide_index=True,
        )

    with st.expander("View processed readings"):
        st.dataframe(results, use_container_width=True, hide_index=True)

    csv_bytes = results.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download processed results (CSV)",
        data=csv_bytes,
        file_name="sunwatch_processed_results.csv",
        mime="text/csv",
    )

    st.divider()
    st.markdown(
        "**Engineering note:** Expected power is an estimate based on irradiance, "
        "module temperature, rated capacity and an assumed system-efficiency factor. "
        "Use calibrated sensors and the PV module datasheet for a real installation. "
        "This student project is for learning and demonstration only."
    )


if __name__ == "__main__":
    main()
