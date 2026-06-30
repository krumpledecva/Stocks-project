import time
import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Stock Explorer", layout="wide")
st.title("📈 Stock Price Explorer")

# Auto-refresh every 30 seconds to rotate the Did you know? fact
st_autorefresh(interval=30_000, key="fact_refresh")

DID_YOU_KNOW = [
    ("🍎 Apple", "Apple's 1980 IPO created ~300 millionaires in a single day, with shares jumping from $22 to $29."),
    ("🪟 Microsoft", "Microsoft's 1986 IPO made an estimated 4 billionaires and 12,000 millionaires from its employees alone."),
    ("🪟 Microsoft", "In July 2012, Microsoft posted its first-ever quarterly net loss — $492 million — despite setting a revenue record that same quarter."),
    ("🔍 Google", "Google's 2005 profit surged 700% as companies shifted advertising budgets away from traditional media to the internet."),
    ("🔍 Google", "Between 2007–2010, Google reduced its effective tax rate to just 2.3% by routing profits through Ireland, the Netherlands, and Bermuda."),
    ("📦 Amazon", "Amazon surpassed Walmart as the world's largest retailer outside China in 2021, driven by over 200 million Prime subscribers."),
    ("📦 Amazon", "In 2025, Amazon generated $716.9 billion in revenue with $77.67 billion in net income — second-largest company globally."),
    ("🎬 Netflix", "Netflix's stock dropped 35% in a single week in April 2022 after it revealed password-sharing concerns were hurting subscriber growth."),
    ("🎬 Netflix", "In 2011, Netflix lost 800,000 subscribers in one quarter after a botched plan to spin off its DVD service as 'Qwikster'."),
    ("📘 Meta", "Facebook's 2012 IPO raised $16 billion — the third-largest in US history — yet the stock fell 16.5% in its very first week of trading."),
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

# ── Sidebar ──────────────────────────────────────────────────────────────────
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

# Re-index every stock to 1.00 at the first day of the selected period so
# the charts and calculator reflect growth *within* the chosen window.
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
fig_line = px.line(dff, x="date", y=chosen, title="Normalized price over time")
fig_line.update_layout(yaxis_title="Price (indexed)", xaxis_title="Date")
st.plotly_chart(fig_line, use_container_width=True)

# ── Bar chart: total growth ───────────────────────────────────────────────────
growth_vals = {t: (dff[t].iloc[-1] - 1) * 100 for t in chosen}
fig_bar = px.bar(
    x=list(growth_vals.keys()),
    y=list(growth_vals.values()),
    labels={"x": "Stock", "y": "Total growth (%)"},
    title="Total growth % over selected period",
    color=list(growth_vals.values()),
    color_continuous_scale="RdYlGn",
)
fig_bar.update_layout(coloraxis_showscale=False)
st.plotly_chart(fig_bar, use_container_width=True)

# ── Volatility indicator ──────────────────────────────────────────────────────
st.subheader("🌪 Volatility (daily % swings)")
vol_data = {t: dff[t].pct_change().std() * 100 for t in chosen}
most_volatile = max(vol_data, key=vol_data.get)
vol_cols = st.columns(len(chosen))
for col, t in zip(vol_cols, chosen):
    label = f"🌪 {t}" if t == most_volatile else t
    col.metric(label, f"{vol_data[t]:.2f}%")
