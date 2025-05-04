| **Asset**           | **Parameter**                  | **Value (Units)**             | **Source**                                                                                                           |
|---------------------|-------------------------------|-------------------------------|----------------------------------------------------------------------------------------------------------------------|
| **Diesel generator**| Capacity                      | 500 kW                        | Assumed for MU peak demand sizing                                                                                     |
|                     | Minimum loading               | 20% (100 kW)                  | Typical genset minimum load                                                                                          |
|                     | Marginal cost                 | $0.32 /kWh                   | Based on $4.21/gal fuel price × 35% efficiency                                                                       |
|                     | Conversion efficiency         | 35%                           | Real‐world steady‐state                                                                                                |
| **Grid**            | Purchase price (energy)       | $0.0884 /kWh                 | Commercial rate, Tempe, AZ                                                                                            |
|                     | Demand charge                 | $10 /kW‑month                | Assumed mid‑range for APS medium general service                                                                      |
|                     | Capacity                      | Unlimited                     | Utility connection                                                                                                   |
| **Solar PV**        | Capacity (Peak)               | 300 kW                        | Assumed PV installation                                                                                                |
|                     | Marginal cost                 | $0 /kWh                      | Zero fuel cost                                                                                                       |
|                     | Profile                       | Hourly irradiance (TMY3)      | NREL TMY3 for Phoenix/Tempe                                                                                           |
| **Wind turbine**    | Capacity (Rated)              | 200 kW                        | Assumed small turbine                                                                                                 |
|                     | Marginal cost                 | $0 /kWh                      | Zero fuel cost                                                                                                       |
|                     | Profile                       | Hourly power (2007–2013)      | NREL WIND Toolkit                                                                                                      |
| **Battery storage** | Energy capacity               | 500 kWh                       | Assumed Li‑ion system                                                                                                  |
|                     | Power rating                  | 250 kW                        |                                                                                                                      |
|                     | Round‑trip efficiency         | 90%                           | Typical Li‑ion performance                                                                                             |
|                     | Marginal cost                 | $0 /kWh                      | No fuel cost                                                                                                         |
| **Optimization**    | Objective                     | Minimize total cost (fuel + grid + demand charges) |                                                                                                         |
|                     | Reserve requirement           | 10% spinning reserve          |                                                                                                                      |


---

## ⏱️ Input Data Format Assumptions

- All CSV input files (`building.csv`, `solar.csv`, `wind.csv`) must:
  - Contain **8760 rows** (one per hour of the year)
  - Use **kW** as the unit for all values
  - Be formatted as a **single column**
  - Have **no header row**
