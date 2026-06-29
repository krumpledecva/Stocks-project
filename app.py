import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Stock Explorer", layout="wide")
st.title("📈 Stock Price Explorer")

st.info(
    "💡 Did you know? Apple's 1980 IPO created ~300 millionaires in a single day, "
    "with shares jumping from $22 to $29."
)


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
cols = st.columns(len(chosen) + 1)
for col, t in zip(cols, chosen):
    growth = (dff[t].iloc[-1] - 1) * 100
    label = f"🏆 {t}" if t == best else t
    col.metric(label, f"{dff[t].iloc[-1]:.2f}x", f"{growth:+.1f}%")
cols[-1].metric("Best performer", best, f"+{(dff[best].iloc[-1]-1)*100:.1f}%")

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
