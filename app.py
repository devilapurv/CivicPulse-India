import pandas as pd
import streamlit as st
from pathlib import Path

st.set_page_config(page_title="CivicPulse India", page_icon="🏙️", layout="wide")
st.title("🏙️ CivicPulse India")
st.caption("Bengaluru civic complaint intelligence | Historical 2023–2024 data")

path = Path(__file__).parent / "civicpulse_dashboard.csv"
if not path.exists():
    st.error("Place civicpulse_dashboard.csv in the same folder as app.py, then refresh.")
    st.stop()

@st.cache_data
def load_data():
    data = pd.read_csv(path)
    required = ["ward", "date", "total_complaints", "priority_score", "priority_level",
                "anomaly", "final_alert", "increased_issue", "issue_increase",
                "suggested_action", "action_assessment"]
    missing = [c for c in required if c not in data.columns]
    if missing:
        raise ValueError("Missing columns: " + ", ".join(missing))
    data["date"] = pd.to_datetime(data["date"], errors="coerce")
    data["total_complaints"] = pd.to_numeric(data["total_complaints"], errors="coerce")
    data["anomaly"] = pd.to_numeric(data["anomaly"], errors="coerce")
    return data.dropna(subset=["ward", "date", "total_complaints"])

try:
    df = load_data()
except Exception as e:
    st.error(f"Could not load CSV: {e}")
    st.stop()

st.sidebar.header("Filters")
ward = st.sidebar.selectbox("Ward", ["All wards"] + sorted(df["ward"].unique().tolist()))
first, last = df["date"].min().date(), df["date"].max().date()
dates = st.sidebar.date_input("Month range", value=(first, last), min_value=first, max_value=last)
if len(dates) != 2:
    st.info("Select both a start and end date.")
    st.stop()
start, end = dates
data = df[(df["date"].dt.date >= start) & (df["date"].dt.date <= end)].copy()
if ward != "All wards":
    data = data[data["ward"] == ward]
if data.empty:
    st.warning("No records for these filters.")
    st.stop()

a,b,c,d = st.columns(4)
a.metric("Complaints", f'{int(data["total_complaints"].sum()):,}')
b.metric("Wards", data["ward"].nunique())
c.metric("Flagged ward-months", int((data["anomaly"] == -1).sum()))
d.metric("Months", data["date"].nunique())

left,right = st.columns([2,1])
with left:
    st.subheader("Monthly complaint trend")
    trend = data.groupby("date")["total_complaints"].sum()
    st.line_chart(trend)
with right:
    st.subheader("Historical ward priority")
    levels = data[["ward","priority_level"]].drop_duplicates("ward")
    counts = levels["priority_level"].value_counts().reindex(["High","Medium","Low"],fill_value=0)
    st.bar_chart(counts)

if ward == "All wards":
    st.subheader("Ward comparison")
    summary = data.groupby("ward").agg(
        complaints=("total_complaints","sum"),
        priority_score=("priority_score","first"),
        priority_level=("priority_level","first"),
        flagged_months=("anomaly",lambda x: int((x == -1).sum()))
    ).sort_values("complaints",ascending=False)
    st.bar_chart(summary.head(15)["complaints"])
    st.dataframe(summary, use_container_width=True)
else:
    st.subheader(f"Ward profile: {ward}")
    p = data.iloc[0]
    x,y = st.columns(2)
    x.metric("Historical priority level", str(p["priority_level"]))
    y.metric("Historical priority score", f'{float(p["priority_score"]):.1f} / 100')
    st.caption("Priority score is based on the full historical period, not the selected date range.")

st.subheader("Anomaly alerts and investigations")
anomalies = data[data["anomaly"] == -1].sort_values("date",ascending=False).copy()
if anomalies.empty:
    st.info("No flagged anomalies in this selection.")
else:
    anomalies["month"] = anomalies["date"].dt.strftime("%b %Y")
    st.dataframe(anomalies[["ward","month","total_complaints","final_alert",
                            "increased_issue","issue_increase","suggested_action",
                            "action_assessment"]],hide_index=True,use_container_width=True)

st.subheader("Monthly recommendations")
view = data.sort_values("date",ascending=False).copy()
view["month"] = view["date"].dt.strftime("%b %Y")
st.dataframe(view[["ward","month","total_complaints","priority_level","final_alert",
                   "suggested_action","action_assessment"]],hide_index=True,use_container_width=True)

st.download_button("Download filtered data",data.to_csv(index=False).encode("utf-8"),
                   "civicpulse_filtered.csv","text/csv")
st.divider()
st.caption("Historical, exploratory analysis only. Anomalies can reflect increases or decreases. "
           "Complaint records are not necessarily distinct incidents; recommendations require human review.")
