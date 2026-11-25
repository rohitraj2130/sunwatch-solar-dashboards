# ☀️ SunWatch — Solar PV Performance Monitor & Fault Alert Dashboard

**An Electrical Engineering + Python project** that analyses solar photovoltaic (PV) readings, estimates expected output, calculates energy generation and flags possible underperformance.

> This repository contains a simulated dataset so the dashboard can be demonstrated without buying sensors or building hardware. It is an educational prototype, not a certified monitoring, protection or fault-diagnosis product.

## What the project does

- Calculates measured DC power from voltage and current readings.
- Estimates expected PV power using irradiance, module temperature, rated capacity and an assumed system-efficiency factor.
- Calculates a performance ratio and highlights readings below a user-selected threshold.
- Estimates daily energy generation in kWh.
- Displays interactive plots and lets the user download processed readings as a CSV.
- Accepts a CSV file from another experiment, provided it follows the column format below.

## Dashboard preview

Run the app locally to see the interactive dashboard. The included sample data covers seven simulated days and contains one deliberately simulated underperformance window so the alert feature can be demonstrated.

## Technology used

- **Electrical concepts:** solar PV generation, irradiance, temperature effect, DC voltage/current, power, energy and performance monitoring.
- **Programming:** Python, Pandas, NumPy, Streamlit and Plotly.
- **Data:** CSV readings (simulated sample data included).

## Project structure

```text
SunWatch-Solar-PV-Monitor/
├── app.py                      # Interactive dashboard
├── generate_sample_data.py     # Rebuild the demonstration dataset
├── requirements.txt             # Python dependencies
├── data/
│   └── sample_solar_data.csv   # Seven days of simulated readings
├── docs/
│   ├── PROJECT_REPORT.md       # Mini-project report
│   └── VIVA_QUESTIONS.md       # Questions to prepare for a viva
├── .gitignore
└── LICENSE
```

## Run on Windows

Install Python 3.10 or newer. Then open Command Prompt or the VS Code terminal inside this project folder and run:

```bash
py -m venv .venv
.venv\Scripts\activate
py -m pip install -r requirements.txt
py -m streamlit run app.py
```

The dashboard should open in your browser. If the `py` command is unavailable, try `python` instead.

## CSV format for your own readings

The uploaded CSV must contain these exact column names:

| Column | Unit | Meaning |
|---|---|---|
| `timestamp` | date/time | Date and time of each reading |
| `irradiance_Wm2` | W/m² | Solar irradiance measured at the PV plane |
| `module_temp_C` | °C | PV module temperature |
| `voltage_V` | V | Measured DC voltage |
| `current_A` | A | Measured DC current |

Example row:

```csv
timestamp,irradiance_Wm2,module_temp_C,voltage_V,current_A
2026-01-01 10:00:00,720,41.5,306.2,10.8
```

Use readings from a supervised lab or a trusted dataset. Do not connect equipment or work on live electrical circuits for this software demonstration.

## Engineering model

### 1. Measured DC power

\[
P_{measured}=V_{DC}\times I_{DC}
\]

### 2. Temperature-corrected expected power

\[
P_{expected}=P_{rated}\times\frac{G}{1000}\times[1+\gamma(T_m-25)]\times\eta_s
\]

Where:

- `P_rated` = PV plant rated capacity in watts (STC rating)
- `G` = plane-of-array irradiance in W/m²
- `γ` = power temperature coefficient per °C (normally negative; use the module datasheet)
- `T_m` = module temperature in °C
- `η_s` = assumed system-efficiency factor representing simplified system losses

The model clips a negative temperature factor to zero. It is intentionally simplified: it does not model inverter efficiency curves, shading geometry, module mismatch, MPPT behaviour or detailed irradiance/temperature dynamics.

### 3. Performance ratio used by this demo

\[
PR_{demo}=\frac{P_{measured}}{P_{expected}}
\]

The app only evaluates this ratio when expected power is above 100 W. It raises a **possible underperformance** alert when expected power is above 300 W and the ratio falls below the selected threshold. This is a configurable screening rule, not proof of a particular fault.

### 4. Energy

\[
E=\sum P_i\Delta t_i
\]

Power in kW multiplied by the time interval in hours gives energy in kWh. The dashboard estimates intervals from timestamps and limits long gaps to avoid counting missing data as continuous generation.

## How to demonstrate the project

1. Start the dashboard with the supplied sample data.
2. Point out the measured-power and expected-power curves.
3. Open the performance-alert section and explain that the sample includes an artificial underperformance period.
4. Change the rated capacity or alert threshold and observe how the calculations respond.
5. Upload a correctly formatted CSV and download the processed results.

## Future improvements

- Connect a low-voltage sensor setup or inverter data export under qualified supervision.
- Add inverter efficiency and MPPT operating-point information.
- Add temperature and irradiance sensor calibration checks.
- Compare multiple PV strings and add string-level analytics.
- Store readings in a database and add authentication for a deployed version.
- Validate the model against a real PV module datasheet and laboratory measurements.

## Suggested GitHub repository description

`Python dashboard for solar PV power, energy and performance monitoring with a temperature-corrected model and underperformance alerts.`

## Suggested GitHub topics

`electrical-engineering` `solar-energy` `solar-pv` `renewable-energy` `python` `streamlit` `data-visualization` `energy-monitoring`

## Author

Add your name, college, branch and semester here before publishing. Keep the project description honest: identify the included readings as simulated data unless you replace them with real, verified measurements.
