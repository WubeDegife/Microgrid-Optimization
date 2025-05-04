import streamlit as st
import pandas as pd
import pypsa
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import pathlib

# Page setup
st.set_page_config(page_title="Memorial Union Microgrid", page_icon="🏛️", layout="wide")
st.title("🏛️ Memorial Union Microgrid Dispatch")
st.caption("Season‑by‑season & month‑level optimisation for ASU’s Memorial Union building")

# Header image
hero = pathlib.Path(__file__).with_name("MU.jpg")
if hero.exists():
    st.image(str(hero), use_container_width=True)

# --- Sidebar: CSV uploads ---
with st.sidebar:
    st.header("Upload 8760‑row CSVs")
    loadFile  = st.file_uploader("building.csv (Load)",  type="csv")
    solarFile = st.file_uploader("solar.csv (Solar)",    type="csv")
    windFile  = st.file_uploader("wind.csv  (Wind)",     type="csv")

# --- Inputs ---
left, right = st.columns(2)
with left:
    st.subheader("Capacities & η")
    # Diesel capacity and minimum load % side-by-side
    c1, c2 = st.columns(2)
    DieselCapacity   = c1.number_input("Diesel kW", 500)
    DieselMinLoadPct = c2.slider("Diesel Min %", 0, 100, 20)/100
    # Solar and wind capacities side-by-side
    c3, c4 = st.columns(2)
    SolarCapacity = c3.number_input("Solar kW", 300)
    WindCapacity  = c4.number_input("Wind kW", 200)
    # Battery capacity and power side-by-side
    c5, c6 = st.columns(2)
    BatteryCapacity = c5.number_input("Battery kWh", 500)
    BatteryPower    = c6.number_input("Battery kW", 250)
    # Diesel and battery efficiencies side-by-side
    c7, c8 = st.columns(2)
    DieselEff  = c7.slider("Diesel η", 0.0, 1.0, 0.35)
    BatteryEff = c8.slider("Battery η", 0.0, 1.0, 0.9)
with right:
    st.subheader("Marginal Costs $/kWh")
    # Diesel and grid costs side-by-side
    d1, d2 = st.columns(2)
    DieselCost = d1.number_input("Diesel", 0.32, format="%.4f")
    GridCost   = d2.number_input("Grid",   0.0884, format="%.4f")
    # Solar and wind costs side-by-side
    d3, d4 = st.columns(2)
    SolarMCost = d3.number_input("Solar", 0.02, format="%.4f")
    WindMCost  = d4.number_input("Wind",  0.03, format="%.4f")
    # Battery O&M cost full width
    BatteryMCost = st.number_input("Battery O&M", 0.02, format="%.4f")

# --- Season & Month ---
season_quarters = {"Winter":1, "Spring":2, "Summer":3, "Fall":4}
season_tab = st.radio("Season", list(season_quarters.keys()), horizontal=True)
quarter = season_quarters[season_tab]
# seasonal diesel adjustment
diesel_factors = {"Winter":0.8, "Spring":1.0, "Summer":1.2, "Fall":0.9}
DieselCost *= diesel_factors[season_tab]

# --- Helper: load CSV series ---
def load_series(f):
    df = pd.read_csv(f)
    series = df.iloc[:,0]
    if len(series) != 8760:
        st.error("Each CSV must have 8760 rows"); st.stop()
    return pd.Series(series.values,
                     index=pd.date_range("2023-01-01", periods=8760, freq="H"))

# color palette
color_map = {'solar':'#E69F00','wind':'#56B4E9','diesel':'#999999','grid':'#D55E00','load':'#666666'}

# --- Optimization function via PyPSA ---
def optimise(load, solar, wind):
    n = pypsa.Network()
    n.set_snapshots(load.index)
    n.add("Bus","bus")
    n.add("Load","d",bus="bus",p_set=load)
    n.add("Generator","solar",bus="bus",
          p_nom=SolarCapacity,p_max_pu=solar/SolarCapacity,marginal_cost=SolarMCost)
    n.add("Generator","wind",bus="bus",
          p_nom=WindCapacity,p_max_pu=wind/WindCapacity,marginal_cost=WindMCost)
    n.add("Generator","diesel",bus="bus",
          p_nom=DieselCapacity,p_min_pu=DieselMinLoadPct,
          marginal_cost=DieselCost,efficiency=DieselEff)
    n.add("Generator","grid",bus="bus",p_nom=1000,marginal_cost=GridCost)
    n.add("StorageUnit","battery",bus="bus",
          p_nom=BatteryPower,max_hours=BatteryCapacity/BatteryPower,
          efficiency_store=BatteryEff,efficiency_dispatch=BatteryEff,
          marginal_cost=BatteryMCost)
    n.optimize(solver_name="highs")
    return n

# --- Main logic ---
if loadFile and solarFile and windFile:
    # load full-year series
    full_load, full_solar, full_wind = map(load_series, [loadFile, solarFile, windFile])
    # select month
    months_avail = full_load[full_load.index.quarter==quarter].index.month.unique()
    month_names = {1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun',
                   7:'Jul',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'}
    month = st.selectbox("Month", sorted(months_avail), format_func=lambda m:month_names[m])
    # slice month data
    mask = full_load.index.month==month
    load = full_load[mask]; solar = full_solar[mask]; wind = full_wind[mask]

    # run PyPSA optimize
    try:
        net = optimise(load, solar, wind)
    except Exception as e:
        st.error(e); st.stop()

    gen = net.generators_t.p
    soc_series = net.storage_units_t.state_of_charge['battery']

    # calculate demand & merit-order dispatch
    demand = load.sum()
    avail = {'Solar':solar.sum(), 'Battery':BatteryCapacity,
             'Wind':wind.sum(), 'Grid':float('inf'), 'Diesel':float('inf')}
    costs = {'Solar':SolarMCost,'Battery':BatteryMCost,
             'Wind':WindMCost,'Grid':GridCost,'Diesel':DieselCost}
    rem = demand; dispatch={}
    for asset in sorted(avail, key=lambda x:costs[x]):
        take = min(rem, avail[asset]); dispatch[asset]=take; rem-=take
        if rem<=0: break

    # metrics
    st.metric("Month Demand", f"{demand:,.0f} kWh")
    total_cost = sum(dispatch[a]*costs[a] for a in dispatch)
    st.metric("Merit-Order Cost", f"${total_cost:,.2f}")

    # --- Plots & tables ---
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("All Assets Dispatch – Full‑month window")
        figA, axA = plt.subplots(figsize=(6,4))
        gen[['solar','wind','diesel','grid']].plot.area(ax=axA, stacked=True,
            color=[color_map[k] for k in ['solar','wind','diesel','grid']], alpha=0.6)
        load.plot(ax=axA, color=color_map['load'], linewidth=1, label='Load')
        axA.grid(True, color='grey', linestyle='-', linewidth=0.8, alpha=0.5)
        axA.legend(loc='upper right'); figA.autofmt_xdate(); st.pyplot(figA)

        st.subheader("Recommended Assets Dispatch – Full‑month window")
        figB, axB = plt.subplots(figsize=(6,3))
        rec_assets = [a.lower() for a in dispatch if a.lower() in ['solar','wind','diesel','grid']]
        gen[rec_assets].plot.area(ax=axB, stacked=True,
            color=[color_map[k] for k in rec_assets], alpha=0.6)
        load.plot(ax=axB, color=color_map['load'], linewidth=1, label='Load')
        axB.grid(True, color='grey', linestyle='-', linewidth=0.8, alpha=0.5)
        axB.legend(loc='upper right'); figB.autofmt_xdate(); st.pyplot(figB)

        st.subheader("Battery SoC (%)")
        figC, axC = plt.subplots(figsize=(6,2))
        axC.plot(load.index, soc_series/BatteryCapacity*100, color='#377eb8', linewidth=1.2)
        axC.set_ylim(0,100); axC.grid(True, color='grey', linestyle='-', linewidth=0.8, alpha=0.5)
        figC.autofmt_xdate(); st.pyplot(figC)

    with col2:
        st.subheader("Recommended Mix Table")
        df = pd.DataFrame({"Source":list(dispatch.keys()),
                           "Energy (kWh)":list(dispatch.values())})
        df['Cost ($)'] = df.apply(lambda r: r['Energy (kWh)']*costs[r['Source']], axis=1)
        st.dataframe(df, use_container_width=True)

        st.subheader("Cost Breakdown Pie")
        figP, axP = plt.subplots(figsize=(4,4))
        cost_vals = df['Cost ($)']
        wedges, _ = axP.pie(cost_vals, startangle=90)
        labels = [f"{src} {val/cost_vals.sum()*100:.1f}%" for src,val in zip(df['Source'], cost_vals)]
        axP.legend(wedges, labels, title="Source", loc='center left', bbox_to_anchor=(1,0.5))
        axP.axis('equal'); st.pyplot(figP)

    # summary before rating
    summary = ' + '.join([f"{a} {int(v)} kWh" for a,v in dispatch.items()])
    st.markdown(f"**Summary:** For {month_names[month]} {season_tab}, dispatch = {summary} to meet {demand:,.0f} kWh demand.")

    # --- Rating & Export ---
    st.markdown("### Rate this optimisation")
    rating = st.select_slider("Your Rating", options=["★☆☆☆☆","★★☆☆☆","★★★☆☆","★★★★☆","★★★★★"], value="★★★☆☆")
    st.write(f"Rating: {rating}")
    if st.button("Export Rating"):
        df_r = pd.DataFrame([{"Season":season_tab, "Month":month_names[month], "Rating":rating.count('★')}])
        st.download_button("Download rating.csv", df_r.to_csv(index=False), "rating.csv", "text/csv")
