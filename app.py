import time
import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Stock Explorer", layout="wide")

# ── SquadAway-inspired design system ─────────────────────────────────────────
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Caveat+Brush&family=Caveat:wght@500;700&family=Nunito:wght@400;600;700;800&display=swap" rel="stylesheet">
<style>
:root {
  --bg:#F5EDE0; --bg-accent:#EFE4D2; --paper:#FBF6EC;
  --ink:#3D3225; --ink-soft:#7A6A55;
  --pink:#F4B6C2; --rose:#E89BAD;
  --mint:#B5DDC8; --mint-deep:#7DBFA0;
  --butter:#F7DA9E; --butter-deep:#E8B968;
  --sky:#A8C8E1; --sky-deep:#7AA8C9;
  --lilac:#C9B8DD; --lilac-deep:#A290C0;
  --peach:#F5C2A0;
  --border:#D9C9AE;
  --f-display:'Caveat Brush','Marker Felt',cursive;
  --f-hand:'Caveat','Comic Sans MS',cursive;
  --f-body:'Nunito',system-ui,sans-serif;
}

/* Page background */
.stApp {
  background:
    radial-gradient(circle at 10% 10%, #F4B6C222 0%, transparent 50%),
    radial-gradient(circle at 90% 30%, #B5DDC822 0%, transparent 50%),
    radial-gradient(circle at 50% 90%, #F7DA9E22 0%, transparent 50%),
    #F5EDE0 !important;
  font-family: var(--f-body) !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
  background: var(--bg-accent) !important;
  border-right: 3px solid var(--ink) !important;
}
section[data-testid="stSidebar"] .stMarkdown,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p {
  font-family: var(--f-hand) !important;
  color: var(--ink) !important;
  font-weight: 600;
}
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
  font-family: var(--f-display) !important;
  color: var(--ink) !important;
  letter-spacing: 1px;
}

/* Main title */
h1 {
  font-family: var(--f-display) !important;
  font-size: 3rem !important;
  color: var(--ink) !important;
  text-shadow: 3px 3px 0 var(--pink), 6px 6px 0 var(--butter);
  letter-spacing: 1px;
}

/* Section headings */
h2, h3 {
  font-family: var(--f-hand) !important;
  color: var(--ink) !important;
  font-weight: 700 !important;
}

/* Metric cards — paper style */
[data-testid="metric-container"] {
  background: var(--paper) !important;
  border: 2px solid var(--border) !important;
  border-radius: 18px !important;
  padding: 18px 20px !important;
  box-shadow: 0 4px 0 rgba(60,50,37,.12), 0 6px 16px rgba(60,50,37,.06) !important;
}
[data-testid="metric-container"] [data-testid="stMetricLabel"] {
  font-family: var(--f-hand) !important;
  font-size: 1rem !important;
  font-weight: 700 !important;
  color: var(--ink-soft) !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
  font-family: var(--f-display) !important;
  font-size: 2rem !important;
  color: var(--ink) !important;
}
[data-testid="metric-container"] [data-testid="stMetricDelta"] {
  font-family: var(--f-hand) !important;
  font-weight: 700 !important;
}

/* Info / Did you know box */
[data-testid="stAlert"] {
  background: var(--butter) !important;
  border: 2px solid var(--ink) !important;
  border-radius: 18px !important;
  box-shadow: 0 4px 0 var(--ink) !important;
  color: var(--ink) !important;
  font-family: var(--f-hand) !important;
  font-size: 1.05rem !important;
  font-weight: 600 !important;
}
[data-testid="stAlert"] svg { display: none; }

/* Chart containers — paper card */
[data-testid="stPlotlyChart"] {
  background: var(--paper) !important;
  border: 2px solid var(--border) !important;
  border-radius: 18px !important;
  padding: 12px !important;
  box-shadow: 0 4px 0 rgba(60,50,37,.10), 0 6px 16px rgba(60,50,37,.05) !important;
}

/* Caption */
[data-testid="stCaptionContainer"] {
  font-family: var(--f-hand) !important;
  color: var(--ink-soft) !important;
  font-size: 0.95rem !important;
}

/* Warning box */
[data-testid="stWarning"] {
  background: var(--peach) !important;
  border: 2px solid var(--ink) !important;
  border-radius: 14px !important;
  color: var(--ink) !important;
  font-family: var(--f-hand) !important;
  font-weight: 600 !important;
}

/* Streamlit multiselect tags */
[data-baseweb="tag"] {
  background: var(--mint) !important;
  border: 2px solid var(--ink) !important;
  border-radius: 99px !important;
  color: var(--ink) !important;
  font-family: var(--f-hand) !important;
  font-weight: 700 !important;
}

/* Slider */
[data-testid="stSlider"] [role="slider"] {
  background: var(--rose) !important;
  border: 3px solid var(--ink) !important;
}

/* Dividers */
hr { border-color: var(--border) !important; border-style: dashed !important; }

/* Plotly charts font override */
.js-plotly-plot .plotly .g-gtitle text,
.js-plotly-plot .plotly text { font-family: 'Nunito', sans-serif !important; }
</style>
""", unsafe_allow_html=True)

# ── Title & auto-refresh ──────────────────────────────────────────────────────
st.title("📈 Stock Price Explorer")
st_autorefresh(interval=30_000, key="fact_refresh")

# ── Did you know? rotating facts ─────────────────────────────────────────────
DID_YOU_KNOW = [
    ("🍎 Apple", "Apple's 1980 IPO created ~300 millionaires in a single day, with shares jumping from $22 to $29."),
    ("🪟 Microsoft", "Microsoft's 1986 IPO made an estimated 4 billionaires and 12,000 millionaires from its employees alone."),
    ("🪟 Microsoft", "In July 2012, Microsoft posted its first-ever quarterly net loss — $492 million — despite setting a revenue record that same quarter."),
    ("🔍 Google", "Google's 2005 profit surged 700% as companies shifted ad budgets away from traditional media to the internet."),
    ("🔍 Google", "Between 2007–2010, Google reduced its effective tax rate to just 2.3% by routing profits through Ireland, Netherlands, and Bermuda."),
    ("📦 Amazon", "Amazon surpassed Walmart as the world's largest retailer outside China in 2021, driven by over 200 million Prime subscribers."),
    ("📦 Amazon", "In 2025, Amazon generated $716.9 billion in revenue with $77.67 billion in net income — second-largest company globally."),
    ("🎬 Netflix", "Netflix's stock dropped 35% in a single week in April 2022 after it revealed password-sharing concerns were hurting growth."),
    ("🎬 Netflix", "In 2011, Netflix lost 800,000 subscribers in one quarter after a botched plan to spin off its DVD service as 'Qwikster'."),
    ("📘 Meta", "Facebook's 2012 IPO raised $16 billion — third-largest in US history — yet the stock fell 16.5% in its very first week of trading."),
]

fact_index = int(time.time() / 30) % len(DID_YOU_KNOW)
company, fact = DID_YOU_KNOW[fact_index]
st.info(f"💡 **Did you know? {company}** — {fact}")


@st.cache_data
def load_data():
    df = px.data.stocks()  # columns: date + 6 big tech stocks; prices indexed to 1.00 at Jan 2018
    df["date"] = pd.to_datetime(df["date"])
    return df


df = load_data()
tickers = [c for c in df.columns if c != "date"]

# ── Sidebar ───────────────────────────────────────────────────────────────────
st.sidebar.header("Controls")
chosen = st.sidebar.multiselect("Choose stocks", tickers, default=["AAPL", "MSFT", "GOOG"])

date_min, date_max = df["date"].min().date(), df["date"].max().date()
start_date, end_date = st.sidebar.slider(
    "Date range",
    min_value=date_min,
    max_value=date_max,
    value=(date_min, date_max),
    format="MMM YYYY",
)

invest_amount = st.sidebar.number_input(
    "What if I invested $… ?", min_value=100, max_value=1_000_000, value=1_000, step=100
)

if not chosen:
    st.warning("Pick at least one stock from the sidebar.")
    st.stop()

mask = (df["date"].dt.date >= start_date) & (df["date"].dt.date <= end_date)
dff = df[mask].copy()

if dff.empty or len(dff) < 2:
    st.warning("No data in the selected date range. Please widen the range.")
    st.stop()

for t in tickers:
    dff[t] = dff[t] / dff[t].iloc[0]

st.caption(
    f"Prices re-indexed to 1.00 at {start_date.strftime('%b %Y')} "
    f"— showing growth through {end_date.strftime('%b %Y')}."
)

# ── Key metrics row ───────────────────────────────────────────────────────────
best = max(chosen, key=lambda t: dff[t].iloc[-1])
worst = min(chosen, key=lambda t: dff[t].iloc[-1])
cols = st.columns(len(chosen) + 2)
for col, t in zip(cols, chosen):
    growth = (dff[t].iloc[-1] - 1) * 100
    if t == best:
        label = f"🏆 {t}"
    elif t == worst:
        label = f"📉 {t}"
    else:
        label = t
    col.metric(label, f"{dff[t].iloc[-1]:.2f}x", f"{growth:+.1f}%")
cols[-2].metric("Best performer", best, f"+{(dff[best].iloc[-1]-1)*100:.1f}%")
cols[-1].metric("Least growth", worst, f"{(dff[worst].iloc[-1]-1)*100:+.1f}%")

# ── $X investment calculator ──────────────────────────────────────────────────
st.subheader(f"💸 What if you invested ${invest_amount:,}?")
inv_cols = st.columns(len(chosen))
for col, t in zip(inv_cols, chosen):
    final_value = invest_amount * dff[t].iloc[-1]
    profit = final_value - invest_amount
    col.metric(t, f"${final_value:,.0f}", f"{profit:+,.0f}")

# ── Line chart ────────────────────────────────────────────────────────────────
SQUAD_COLORS = ["#E89BAD", "#7DBFA0", "#E8B968", "#7AA8C9", "#A290C0", "#D99668"]
fig_line = px.line(
    dff, x="date", y=chosen,
    title="Normalized price over time",
    color_discrete_sequence=SQUAD_COLORS,
)
fig_line.update_layout(
    yaxis_title="Price (indexed)", xaxis_title="Date",
    font_family="Nunito",
    plot_bgcolor="#FBF6EC",
    paper_bgcolor="#FBF6EC",
    title_font=dict(family="Caveat Brush", size=22, color="#3D3225"),
    legend=dict(font=dict(family="Caveat", size=14)),
    xaxis=dict(gridcolor="#D9C9AE", linecolor="#3D3225"),
    yaxis=dict(gridcolor="#D9C9AE", linecolor="#3D3225"),
)
st.plotly_chart(fig_line, use_container_width=True)

# ── Bar chart: total growth ───────────────────────────────────────────────────
growth_vals = {t: (dff[t].iloc[-1] - 1) * 100 for t in chosen}
fig_bar = px.bar(
    x=list(growth_vals.keys()),
    y=list(growth_vals.values()),
    labels={"x": "Stock", "y": "Total growth (%)"},
    title="Total growth % over selected period",
    color=list(growth_vals.values()),
    color_continuous_scale=["#E89BAD", "#F7DA9E", "#7DBFA0"],
)
fig_bar.update_layout(
    coloraxis_showscale=False,
    font_family="Nunito",
    plot_bgcolor="#FBF6EC",
    paper_bgcolor="#FBF6EC",
    title_font=dict(family="Caveat Brush", size=22, color="#3D3225"),
    xaxis=dict(gridcolor="#D9C9AE", linecolor="#3D3225"),
    yaxis=dict(gridcolor="#D9C9AE", linecolor="#3D3225"),
)
st.plotly_chart(fig_bar, use_container_width=True)

# ── Volatility indicator ──────────────────────────────────────────────────────
st.subheader("🌪 Volatility (daily % swings)")
vol_data = {t: dff[t].pct_change().std() * 100 for t in chosen}
most_volatile = max(vol_data, key=vol_data.get)
vol_cols = st.columns(len(chosen))
for col, t in zip(vol_cols, chosen):
    label = f"🌪 {t}" if t == most_volatile else t
    col.metric(label, f"{vol_data[t]:.2f}%")
