import io
import zipfile
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# ============================================================
# EV INSIGHTS | ELECTRIC VEHICLE POPULATION ANALYSIS
# ============================================================

st.set_page_config(
    page_title="EV Insights | Population Analysis",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------- LIGHT WEBSITE THEME -----------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}
.stApp {
    background: #f4f7fb;
    color: #172b4d;
}
.block-container {
    max-width: 1450px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}
[data-testid="stSidebar"] {
    background: #102b46;
}
[data-testid="stSidebar"] * {
    color: #f5f8fc !important;
}
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
    color: #e2edf7 !important;
}
[data-testid="stMetric"] {
    background: #ffffff !important;
    border: 1px solid #e1e8f0;
    border-radius: 15px;
    padding: 17px 19px;
    box-shadow: 0 4px 14px rgba(23, 43, 77, 0.06);
}
[data-testid="stMetricLabel"],
[data-testid="stMetricLabel"] p {
    color: #52657d !important;
    font-weight: 600 !important;
}
[data-testid="stMetricValue"],
[data-testid="stMetricValue"] div {
    color: #123653 !important;
    font-weight: 800 !important;
}
.hero {
    background: linear-gradient(120deg, #102b46 0%, #155b78 58%, #188b91 100%);
    padding: 42px 46px;
    border-radius: 22px;
    color: #ffffff;
    margin-bottom: 24px;
}
.hero .eyebrow {
    color: #a8e4df;
    text-transform: uppercase;
    letter-spacing: .15em;
    font-size: .75rem;
    font-weight: 800;
}
.hero h1 {
    color: #ffffff !important;
    font-size: 2.65rem;
    line-height: 1.13;
    margin: 12px 0;
    font-weight: 800;
}
.hero p {
    color: #e1f0f4 !important;
    font-size: 1.05rem;
    max-width: 780px;
    margin-bottom: 0;
}
.section-kicker {
    color: #13828a;
    font-size: .76rem;
    letter-spacing: .13em;
    text-transform: uppercase;
    font-weight: 800;
    margin-bottom: .25rem;
}
.info-card {
    background: #ffffff;
    border: 1px solid #e1e8f0;
    border-radius: 15px;
    padding: 22px;
    min-height: 145px;
    box-shadow: 0 4px 14px rgba(23, 43, 77, 0.04);
}
.info-card .number {
    color: #13828a;
    font-weight: 800;
    font-size: .8rem;
    letter-spacing: .12em;
}
.info-card h3 {
    color: #173653 !important;
    margin: 9px 0;
    font-size: 1.12rem;
}
.info-card p {
    color: #5d7087 !important;
    font-size: .92rem;
    margin: 0;
}
div[data-testid="stDataFrame"] {
    background: #ffffff;
    border-radius: 12px;
}
hr {
    border-color: #dce5ee;
}
</style>
""", unsafe_allow_html=True)

sns.set_theme(style="whitegrid", palette=["#167d9a", "#25a18e", "#f2a541", "#7768ae"])

# ----------------------- DATA LOADING -----------------------
@st.cache_data(show_spinner="Loading EV population dataset...")
def load_uploaded_file(file_name, file_bytes):
    if file_name.lower().endswith(".zip"):
        with zipfile.ZipFile(io.BytesIO(file_bytes)) as archive:
            csv_files = [n for n in archive.namelist() if n.lower().endswith(".csv")]
            if not csv_files:
                raise ValueError("The ZIP archive does not contain a CSV file.")
            with archive.open(csv_files[0]) as csv:
                return pd.read_csv(csv, low_memory=False)
    return pd.read_csv(io.BytesIO(file_bytes), low_memory=False)


@st.cache_data(show_spinner="Loading local dataset...")
def load_local_file(path, modified_time):
    path_obj = Path(path)
    if path_obj.suffix.lower() == ".zip":
        with zipfile.ZipFile(path_obj) as archive:
            csv_files = [n for n in archive.namelist() if n.lower().endswith(".csv")]
            if not csv_files:
                raise ValueError("The ZIP archive does not contain a CSV file.")
            with archive.open(csv_files[0]) as csv:
                return pd.read_csv(csv, low_memory=False)
    return pd.read_csv(path_obj, low_memory=False)


# ----------------------- SIDEBAR -----------------------
with st.sidebar:
    st.markdown("## ⚡ EV INSIGHTS")
    st.caption("ELECTRIC VEHICLE POPULATION")
    st.markdown("---")
    page = st.radio(
        "NAVIGATION",
        ["Home", "Dashboard", "Numerical Analysis",
         "Categorical Analysis", "Insights & Dataset"],
        label_visibility="visible"
    )
    st.markdown("---")
    st.markdown("### DATA SOURCE")
    uploaded = st.file_uploader("Upload dataset (CSV or ZIP)", type=["csv", "zip"])
    local_path = st.text_input(
        "Or local filename",
        value="Electric_Vehicle_Population_Data.csv.zip"
    )
    st.markdown("---")
    st.markdown("### FILTERS")
    st.caption("Filters update the analysis pages.")

try:
    if uploaded is not None:
        df = load_uploaded_file(uploaded.name, uploaded.getvalue())
    elif Path(local_path).exists():
        df = load_local_file(local_path, Path(local_path).stat().st_mtime)
    else:
        df = None
except Exception as exc:
    st.error(f"Unable to load dataset: {exc}")
    st.stop()

if df is None:
    st.markdown("""
    <div class="hero">
      <div class="eyebrow">Electric mobility • Data exploration</div>
      <h1>Understand the shift<br>to electric mobility.</h1>
      <p>Explore electric vehicle adoption patterns, manufacturers, driving range
      and geographic distribution through clear, interactive visualizations.</p>
    </div>
    """, unsafe_allow_html=True)
    st.warning(
        "Upload your EV Population CSV/ZIP in the sidebar, or place "
        "Electric_Vehicle_Population_Data.csv.zip in the same folder as this Python file."
    )
    st.stop()

df.columns = df.columns.str.strip()
required = ["Make", "Model Year", "Electric Range", "Base MSRP", "County", "Electric Vehicle Type"]
missing = [c for c in required if c not in df.columns]
if missing:
    st.error("Required dataset columns not found: " + ", ".join(missing))
    st.stop()

for col in ["Model Year", "Electric Range", "Base MSRP"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

for col in df.select_dtypes(include="object").columns:
    df[col] = df[col].fillna("Unknown").astype(str)

# ----------------------- FILTERS -----------------------
with st.sidebar:
    make_options = sorted(df["Make"].dropna().unique().tolist())
    chosen_makes = st.multiselect("Manufacturer", make_options)
    type_options = sorted(df["Electric Vehicle Type"].dropna().unique().tolist())
    chosen_types = st.multiselect("Vehicle type", type_options)
    county_options = sorted(df["County"].dropna().unique().tolist())
    chosen_counties = st.multiselect("County", county_options)

    valid_years = df["Model Year"].dropna()
    if not valid_years.empty:
        min_year, max_year = int(valid_years.min()), int(valid_years.max())
        chosen_years = st.slider("Model year range", min_year, max_year, (min_year, max_year))
    else:
        chosen_years = None

filtered = df.copy()
if chosen_makes:
    filtered = filtered[filtered["Make"].isin(chosen_makes)]
if chosen_types:
    filtered = filtered[filtered["Electric Vehicle Type"].isin(chosen_types)]
if chosen_counties:
    filtered = filtered[filtered["County"].isin(chosen_counties)]
if chosen_years:
    filtered = filtered[filtered["Model Year"].between(chosen_years[0], chosen_years[1])]

if filtered.empty:
    st.warning("No records match the selected filters. Please adjust the filters.")
    st.stop()

# ----------------------- HELPERS -----------------------
def heading(kicker, title, description):
    st.markdown(f'<div class="section-kicker">{kicker}</div>', unsafe_allow_html=True)
    st.title(title)
    st.write(description)

def display_chart(fig):
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

def kpi_row():
    positive_range = filtered.loc[filtered["Electric Range"] > 0, "Electric Range"].dropna()
    median_range = positive_range.median() if not positive_range.empty else 0
    bev_count = (filtered["Electric Vehicle Type"] == "Battery Electric Vehicle (BEV)").sum()
    bev_share = bev_count / len(filtered) * 100
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Vehicle records", f"{len(filtered):,}")
    c2.metric("Manufacturers", f"{filtered['Make'].nunique():,}")
    c3.metric("Median electric range", f"{median_range:.0f} mi" if median_range else "N/A")
    c4.metric("BEV share", f"{bev_share:.1f}%")
    st.caption("Range statistics exclude zero and missing values. Counts are dataset records.")

# ----------------------- HOME -----------------------
if page == "Home":
    st.markdown("""
    <div class="hero">
      <div class="eyebrow">Electric mobility • Data exploration</div>
      <h1>Understand the shift<br>to electric mobility.</h1>
      <p>An interactive exploration of electric vehicle population data.
      Discover adoption patterns, compare manufacturers, and examine driving
      range and geographic distribution.</p>
    </div>
    """, unsafe_allow_html=True)

    kpi_row()
    st.markdown("### Explore the analysis")
    c1, c2, c3 = st.columns(3)
    cards = [
        (c1, "01", "Numerical analysis", "Study electric range, MSRP and model-year patterns."),
        (c2, "02", "Categorical analysis", "Compare manufacturers, vehicle types and counties."),
        (c3, "03", "Insights & dataset", "Review findings, summary statistics and the data.")
    ]
    for col, number, title, description in cards:
        with col:
            st.markdown(
                f'<div class="info-card"><div class="number">{number}</div>'
                f'<h3>{title}</h3><p>{description}</p></div>',
                unsafe_allow_html=True
            )
    st.info("Choose a page from the navigation menu in the left sidebar.")

# ----------------------- DASHBOARD -----------------------
elif page == "Dashboard":
    heading("OVERVIEW", "Electric Vehicle Dashboard",
            "A consolidated view of the selected electric vehicle records.")
    kpi_row()

    left, right = st.columns(2)
    with left:
        counts = filtered["Make"].value_counts().head(10).sort_values()
        fig, ax = plt.subplots(figsize=(8, 4.7))
        ax.barh(counts.index, counts.values, color="#167d9a")
        ax.set_title("Top 10 Manufacturers", color="#173653", weight="bold")
        ax.set_xlabel("Number of vehicle records")
        ax.set_ylabel("Manufacturer")
        display_chart(fig)
    with right:
        counts = filtered["Electric Vehicle Type"].value_counts()
        fig, ax = plt.subplots(figsize=(8, 4.7))
        ax.pie(counts.values, labels=counts.index, autopct="%1.1f%%",
               startangle=90, wedgeprops={"edgecolor": "white"})
        ax.set_title("Electric Vehicle Type Distribution", color="#173653", weight="bold")
        display_chart(fig)

    counts = filtered["Model Year"].value_counts().sort_index()
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(counts.index, counts.values, marker="o", color="#168b87", linewidth=2)
    ax.set_title("Vehicle Records by Model Year", color="#173653", weight="bold")
    ax.set_xlabel("Model year")
    ax.set_ylabel("Number of records")
    display_chart(fig)

# ----------------------- NUMERICAL ANALYSIS -----------------------
elif page == "Numerical Analysis":
    heading("DATA TYPE 01", "Numerical Analysis",
            "Explore distributions, spread and relationships between numerical variables.")

    range_values = filtered.loc[filtered["Electric Range"] > 0, "Electric Range"].dropna()
    left, right = st.columns(2)

    with left:
        if not range_values.empty:
            fig, ax = plt.subplots(figsize=(8, 4.7))
            ax.hist(range_values, bins=30, color="#168b87", edgecolor="white")
            ax.set_title("Distribution of Electric Range", color="#173653", weight="bold")
            ax.set_xlabel("Electric range (miles)")
            ax.set_ylabel("Number of vehicle records")
            display_chart(fig)
            st.write(f"**Mean:** {range_values.mean():.1f} miles")
            st.write(f"**Median:** {range_values.median():.1f} miles")

    with right:
        box_data = filtered[filtered["Electric Range"] > 0]
        types = box_data["Electric Vehicle Type"].unique()
        if len(types):
            values = [
                box_data.loc[box_data["Electric Vehicle Type"] == t, "Electric Range"].dropna().values
                for t in types
            ]
            fig, ax = plt.subplots(figsize=(8, 4.7))
            ax.boxplot(values, tick_labels=[
                str(t).replace("Battery Electric Vehicle", "BEV")
                .replace("Plug-in Hybrid Electric Vehicle", "PHEV") for t in types
            ], showfliers=False)
            ax.set_title("Electric Range by Vehicle Type", color="#173653", weight="bold")
            ax.set_xlabel("Vehicle type")
            ax.set_ylabel("Electric range (miles)")
            display_chart(fig)

    scatter = filtered[(filtered["Electric Range"] > 0) & (filtered["Base MSRP"] > 0)].copy()
    if not scatter.empty:
        if len(scatter) > 5000:
            scatter = scatter.sample(5000, random_state=42)
        fig, ax = plt.subplots(figsize=(10, 5))
        for vehicle_type, group in scatter.groupby("Electric Vehicle Type"):
            ax.scatter(group["Electric Range"], group["Base MSRP"],
                       alpha=.55, s=20, label=vehicle_type)
        ax.set_title("Electric Range vs Base MSRP", color="#173653", weight="bold")
        ax.set_xlabel("Electric range (miles)")
        ax.set_ylabel("Base MSRP (USD)")
        ax.legend(title="Vehicle type", fontsize=8)
        display_chart(fig)
        st.caption("Only positive range and MSRP records are shown; up to 5,000 points are sampled.")

    st.markdown("### Descriptive statistics")
    st.dataframe(
        filtered[["Model Year", "Electric Range", "Base MSRP"]].describe().round(2),
        use_container_width=True
    )

# ----------------------- CATEGORICAL ANALYSIS -----------------------
elif page == "Categorical Analysis":
    heading("DATA TYPE 02", "Categorical Analysis",
            "Compare groups and identify the most frequent categories in the dataset.")

    left, right = st.columns(2)
    with left:
        counts = filtered["Make"].value_counts().head(10).sort_values()
        fig, ax = plt.subplots(figsize=(8, 4.7))
        ax.barh(counts.index, counts.values, color="#167d9a")
        ax.set_title("Top 10 Manufacturers", color="#173653", weight="bold")
        ax.set_xlabel("Number of records")
        ax.set_ylabel("Manufacturer")
        display_chart(fig)
    with right:
        counts = filtered["Electric Vehicle Type"].value_counts()
        fig, ax = plt.subplots(figsize=(8, 4.7))
        ax.pie(counts.values, labels=counts.index, autopct="%1.1f%%",
               startangle=90, wedgeprops={"edgecolor": "white"})
        ax.set_title("Vehicle Type Distribution", color="#173653", weight="bold")
        display_chart(fig)

    left, right = st.columns(2)
    with left:
        counts = filtered["County"].value_counts().head(10).sort_values()
        fig, ax = plt.subplots(figsize=(8, 4.7))
        ax.barh(counts.index, counts.values, color="#e6a23c")
        ax.set_title("Top 10 Counties", color="#173653", weight="bold")
        ax.set_xlabel("Number of records")
        ax.set_ylabel("County")
        display_chart(fig)
    with right:
        cafv = "Clean Alternative Fuel Vehicle (CAFV) Eligibility"
        if cafv in filtered.columns:
            counts = filtered[cafv].value_counts().head(10)
            fig, ax = plt.subplots(figsize=(8, 4.7))
            ax.bar(counts.index, counts.values, color="#7868a6")
            ax.set_title("CAFV Eligibility Categories", color="#173653", weight="bold")
            ax.set_xlabel("Eligibility category")
            ax.set_ylabel("Number of records")
            ax.tick_params(axis="x", rotation=18)
            display_chart(fig)

# ----------------------- INSIGHTS & DATASET -----------------------
elif page == "Insights & Dataset":
    heading("FINDINGS", "Insights & Dataset",
            "Review the key patterns and inspect the records used in this analysis.")
    kpi_row()

    top_make = filtered["Make"].value_counts().idxmax()
    top_county = filtered["County"].value_counts().idxmax()
    zero_range_pct = (filtered["Electric Range"] == 0).mean() * 100

    a, b = st.columns(2)
    a.metric("Most frequent manufacturer", top_make)
    b.metric("Most represented county", top_county)

    st.markdown("### Key observations")
    st.write(f"- **{top_make}** is the most frequent manufacturer in the selected records.")
    st.write(f"- **{top_county}** is the most represented county in the selected records.")
    st.write(f"- **{zero_range_pct:.1f}%** of records have zero electric range. Treat these values cautiously.")
    positive_msrp = filtered.loc[filtered["Base MSRP"] > 0, "Base MSRP"].dropna()
    st.write(f"- **{len(positive_msrp):,}** records have positive MSRP values.")

    st.markdown("### Dataset preview")
    st.dataframe(filtered.head(100), use_container_width=True)

    st.markdown("### Download filtered data")
    st.download_button(
        "Download filtered dataset (CSV)",
        data=filtered.to_csv(index=False).encode("utf-8"),
        file_name="filtered_ev_population.csv",
        mime="text/csv"
    )

# ----------------------- FOOTER -----------------------
st.markdown("---")
st.caption("EV Insights | Numerical • Categorical • Data Integrity")
