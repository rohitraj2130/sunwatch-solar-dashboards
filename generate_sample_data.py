"""Generate a reproducible, simulated PV dataset for the SunWatch demo."""

from pathlib import Path
import numpy as np
import pandas as pd


def main() -> None:
    rng = np.random.default_rng(21)
    timestamps = pd.date_range("2026-01-01 00:00", periods=7 * 96, freq="15min")
    hour = timestamps.hour.to_numpy() + timestamps.minute.to_numpy() / 60
    day_number = (timestamps.normalize() - timestamps.normalize().min()).days.to_numpy()

    # Smooth daylight profile with modest day-to-day/cloud variation.
    daylight = np.maximum(0, np.sin(np.pi * (hour - 6) / 12))
    cloud_factor = np.clip(0.91 + 0.08 * np.sin(day_number * 1.7 + hour * 0.8)
                           + rng.normal(0, 0.035, len(timestamps)), 0.55, 1.05)
    irradiance = np.clip(950 * daylight * cloud_factor, 0, None)
    ambient_temp = 22 + 4 * np.sin((hour - 8) * np.pi / 12) + day_number * 0.25
    module_temp = ambient_temp + 0.028 * irradiance + rng.normal(0, 1.2, len(timestamps))

    rated_capacity_kw = 5.0
    temperature_coefficient = -0.004
    system_efficiency = 0.90
    temp_factor = np.clip(1 + temperature_coefficient * (module_temp - 25), 0, None)
    expected_power = rated_capacity_kw * 1000 * (irradiance / 1000) * temp_factor * system_efficiency

    performance = np.clip(0.94 + rng.normal(0, 0.025, len(timestamps)), 0.84, 1.00)
    # Simulated underperformance window for demonstrating the alert feature.
    fault_window = (timestamps >= "2026-01-04 10:00") & (timestamps <= "2026-01-04 14:00")
    performance[fault_window] *= 0.58
    actual_power = np.maximum(0, expected_power * performance)

    # Use a plausible DC bus voltage and derive current from the simulated power.
    voltage = np.where(irradiance > 20, 300 + 8 * daylight + rng.normal(0, 2, len(timestamps)), 0)
    current = np.divide(actual_power, voltage, out=np.zeros_like(actual_power), where=voltage > 0)

    frame = pd.DataFrame({
        "timestamp": timestamps.strftime("%Y-%m-%d %H:%M:%S"),
        "irradiance_Wm2": irradiance.round(1),
        "module_temp_C": module_temp.round(1),
        "voltage_V": voltage.round(2),
        "current_A": current.round(3),
    })
    output = Path(__file__).resolve().parent / "data" / "sample_solar_data.csv"
    output.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(output, index=False)
    print(f"Created {len(frame)} sample readings: {output}")


if __name__ == "__main__":
    main()
