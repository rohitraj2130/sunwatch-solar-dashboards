# Mini Project Report

## Title
**SunWatch: Solar PV Performance Monitor and Underperformance Alert Dashboard**

## Abstract
Solar photovoltaic output changes with solar irradiance and module temperature. This project presents a Python-based dashboard that analyses DC voltage, DC current, irradiance and module-temperature readings. It calculates measured power, estimates expected power using a simplified temperature-corrected PV model, estimates daily energy generation and flags readings that may indicate underperformance. An interactive dashboard helps users compare measured and estimated output. A simulated dataset is included so the software can be demonstrated without hardware.

## 1. Objectives
1. Apply basic electrical power and energy equations to PV-system data.
2. Study the effect of irradiance and module temperature on PV output.
3. Develop a simple expected-power model and compare it with measured output.
4. Create a dashboard that visualises performance and highlights unusual readings.
5. Practise Python programming, data handling and technical documentation.

## 2. Software and tools
- Python 3.10 or newer
- Streamlit for the user interface
- Pandas and NumPy for data processing
- Plotly for interactive graphs
- CSV file for the input readings

## 3. Input parameters
The software accepts timestamp, irradiance (W/m²), module temperature (°C), DC voltage (V) and DC current (A). The user also enters the PV plant rated capacity, temperature coefficient, assumed system efficiency and alert threshold.

## 4. Methodology
1. Read the CSV file and validate the required columns.
2. Calculate measured DC power using `P = V × I`.
3. Estimate expected output using the irradiance and temperature-corrected model documented in the README.
4. Calculate a demonstration performance ratio when expected power is sufficiently high.
5. Flag readings when the expected power is above the minimum level and the measured-to-expected ratio is below the chosen threshold.
6. Estimate daily energy from power and timestamp intervals.
7. Display the results using time-series, daily-energy and comparison plots.

## 5. Results and discussion
The included demonstration dataset contains seven simulated days. It deliberately includes a period of reduced simulated output to show how the alert logic works. The dashboard displays the measured and modelled power curves, daily energy estimates and flagged readings. Because the dataset is simulated, these results demonstrate the software workflow only; they are not experimental findings about a physical PV plant.

## 6. Limitations
- The sample data is simulated, not collected from a physical PV module.
- The expected-power equation is a simplified model.
- An alert indicates a reading worth checking; it does not identify the exact cause.
- Real deployment requires calibrated sensors, validated models, safe installation and qualified supervision.

## 7. Conclusion
SunWatch demonstrates how electrical engineering concepts can be combined with Python to monitor solar PV performance. The project calculates electrical power and energy, compares measured output with a simplified expected value and visualises possible underperformance. It can be extended using real, supervised laboratory measurements and more detailed PV-system models.

## 8. References for further study
- The datasheet of the specific PV module used in a real experiment (for rated power and temperature coefficient).
- Standard solar PV engineering texts covering irradiance, module temperature, I–V characteristics and PV-system performance.
- Python, Pandas, NumPy, Streamlit and Plotly official documentation.
