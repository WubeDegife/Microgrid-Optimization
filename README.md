
# 🏛️ ASU Memorial Union Microgrid Dispatch Optimization

This project simulates and optimizes the seasonal and monthly energy dispatch of the ASU Memorial Union building using a hybrid microgrid system that includes diesel generators, solar PV, wind turbines, grid power, and lithium-ion battery storage. The application is built using **Streamlit** for interactivity and **PyPSA** for power systems modeling and optimization.

## 🔍 Project Overview

The Memorial Union building at Arizona State University consumes energy with hourly variability. This tool models dispatch scenarios over different months and seasons by allowing users to upload real 8760-hour datasets for:
- Load (`building.csv`)
- Solar generation profile (`solar.csv`)
- Wind power profile (`wind.csv`)

📌 **Important**: Each CSV file must:
- Contain **8760 rows** (one per hour of the year)
- Be a **single-column** CSV file
- Have **no header row**
- Units must be in **kW**

Sample files for testing:
- [`building.csv`](./building.csv)
- [`solar.csv`](./solar.csv)
- [`wind.csv`](./wind.csv)

The application allows configuration of key technical and economic parameters and simulates optimal dispatch using **PyPSA's** linear optimization engine. The results are visualized in interactive plots and tables, and a recommended dispatch mix is generated based on cost-minimization.

## 🧠 Key Features

- ⚙️ User-defined asset capacities & efficiencies
- 📉 Dynamic cost input & seasonal cost adjustment (e.g., diesel inflation in summer)
- 📊 Month-by-month simulation and visual comparison
- ⚡ Battery state-of-charge tracking and dispatch curves
- 📋 Recommended dispatch summary & merit-order cost estimation
- ⭐ User feedback via rating export (CSV)

## 📁 File Structure

| File               | Description                                                                 |
|--------------------|-----------------------------------------------------------------------------|
| `app.py`           | Streamlit app with interactive UI, optimization model, and result display   |
| `assumptions.md`   | Summary of technical, economic, and modeling assumptions                    |
| `building.csv`     | Hourly energy consumption profile (no header, 8760 values in kW)            |
| `solar.csv`        | Hourly solar generation profile (no header, 8760 values in kW)              |
| `wind.csv`         | Hourly wind generation profile (no header, 8760 values in kW)               |

## 📊 Technologies Used

- Python  
- Streamlit  
- PyPSA (Python for Power System Analysis)  
- Pandas  
- Matplotlib  

## 🧪 How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/memorial-union-microgrid.git
   cd memorial-union-microgrid
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Launch the app:
   ```bash
   streamlit run app.py
   ```

4. Upload your datasets (8760-hour CSVs) via the sidebar and select a season and month.

## 📝 Example Assumptions

| Asset           | Parameter           | Value        |
|----------------|---------------------|--------------|
| Diesel Gen      | Capacity             | 500 kW        |
| Solar PV        | Capacity             | 300 kW        |
| Wind Turbine    | Capacity             | 200 kW        |
| Battery         | Energy Capacity      | 500 kWh       |
| Grid Tariff     | Energy Cost          | $0.0884/kWh   |
| Diesel Cost     | Variable by season   | $0.32/kWh ±   |

See full assumptions in [`assumptions.md`](./assumptions.md).

## 🎓 Author

**Wubishet Degife Mammo**  
PhD Student 
Arizona State University
