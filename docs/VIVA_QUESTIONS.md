# Viva Preparation — SunWatch

### 1. What is the aim of this project?
To analyse solar PV readings, estimate expected output, calculate energy generation and highlight possible underperformance.

### 2. Why did you choose solar PV monitoring?
Solar energy is an important renewable-energy application. Monitoring helps users understand how irradiance, temperature and system performance affect output.

### 3. How do you calculate DC power?
DC power is the product of DC voltage and DC current: `P = V × I`.

### 4. What is irradiance?
Irradiance is the solar power received per unit area. It is commonly expressed in W/m².

### 5. How does temperature affect a PV module?
For many silicon PV modules, output power decreases as cell temperature rises above the reference temperature. The exact coefficient should be taken from the module datasheet.

### 6. What is the temperature coefficient?
It indicates the relative change in a PV parameter for each degree Celsius change in temperature. This project uses the power temperature coefficient.

### 7. What is the performance ratio in this project?
It is a simplified ratio of measured power to modelled expected power. It is used as a screening indicator in this educational dashboard.

### 8. Does an alert confirm a PV panel fault?
No. It only identifies possible underperformance. Shading, soiling, sensor error, wiring issues or model assumptions may contribute. Further inspection is required.

### 9. Why did you use Python?
Python provides accessible libraries for data processing, calculation, plotting and building a dashboard.

### 10. Why is Streamlit used?
Streamlit makes it possible to build an interactive web dashboard using Python without developing a separate front end.

### 11. What is the difference between power and energy?
Power is the rate of energy transfer and is measured in watts. Energy is power integrated over time and is commonly measured in Wh or kWh.

### 12. What is the main limitation of your current project?
The included dataset is simulated and the PV expected-power model is simplified. Real measurements and model validation are needed for engineering conclusions.

### 13. How can the project be improved?
It can be connected to supervised sensor measurements, inverter data, multiple PV strings, a database and a more detailed PV performance model.

### 14. What does CSV mean?
CSV stands for Comma-Separated Values. It is a plain-text format used to store tabular data.

### 15. What is the difference between simulated and experimental data?
Simulated data is generated using assumptions or a model. Experimental data is collected by measuring a real system. The repository clearly labels its included dataset as simulated.
