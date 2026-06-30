# 📈 Stock Price Explorer

A Streamlit web app that compares how big tech stocks (AAPL, GOOG, MSFT, AMZN, NFLX, FB) have grown since January 2018.

**Live app:** https://stocks-projectgit-ekaqctnd4kgv2sqeiwewyt.streamlit.app/
**GitHub repo:** https://github.com/krumpledecva/Stocks-project

---

## Features

- **Normalized price chart** — compare growth on the same scale
- **Best & least performer badges** — 🏆 top stock, 📉 bottom stock highlighted automatically
- **Date-range slider** — zoom into any period since Jan 2018
- **Investment calculator** — "what if I invested $1,000?" per stock
- **Growth bar chart** — side-by-side total growth comparison
- **Volatility indicator** — which stock bounced around the most
- **Beat the Market** — each stock vs. the equal-weighted Big Tech average, with ✅/❌ verdict
- **Risk vs. Return scatter** — growth % vs. volatility for all stocks, with quadrant lines
- **Rotating "Did you know?"** — real facts fetched about Apple, Microsoft, Google, Amazon, Netflix and Meta; new fact every 30 seconds

---

## Architecture

### How the app is built and delivered

```mermaid
graph LR
    A["📊 Plotly Built-in\nStock Data\n(px.data.stocks)"] --> B["🐍 app.py\nStreamlit App"]
    B --> C["🐙 GitHub\nstock-explorer repo"]
    C --> D["☁️ Streamlit\nCommunity Cloud"]
    D --> E["🌐 Live URL\n.streamlit.app"]
    E --> F["👤 User\n(Browser)"]

    style A fill:#F7DA9E,stroke:#3D3225
    style B fill:#F4B6C2,stroke:#3D3225,color:#3D3225
    style C fill:#3D3225,stroke:#000,color:#FBF6EC
    style D fill:#B5DDC8,stroke:#3D3225,color:#3D3225
    style E fill:#A8C8E1,stroke:#3D3225,color:#3D3225
    style F fill:#F5EDE0,stroke:#3D3225
```

![Architecture diagram](https://mermaid.ink/img/pako:eNqVzzFOwzAUgOG9p3hKl1ZqIquKqNIBqUlaGDqgok5NBje1IaprW7YDzciKQBSxwMTCITgPF4AjoFhp1AGQWO3vf8--UFhewnTWAgAYLZyv16dbOGPCsBLCImfGzXnCz43I1hBjgxPekVtvhQ32dHWou04KrnsMYdXu7gFL6cmyShTBG5YbGEnppHZ-aGVk5Quc5Oa0WCbcznHJVjKhiAJFpKh9ZH28cD6ebz7fH6CZmfBIbDYFz00JERPFqg5iG4yrBXc7mOZXBOazacI9vS893LxmbPGkwo9vMNdEJbwTKnGtieo6acsibUpGYAQ0Z2zYpoj6lPa0UWJNhm0fH2V0cODCvaP-0l82LssQQqiXCSZUdUkPkqhO-n4_6JMm-dXH_18xrhOEMj_AByuCYDD4OZn89eFvY1u2BQ)

### User journey

```mermaid
journey
    title User Journey: Exploring Big Tech Stocks
    section Open App
      Navigate to live URL: 5: User
      App loads instantly: 5: App
    section Explore Data
      Select stocks from sidebar: 5: User
      Adjust date range slider: 4: User
      View normalized price chart: 5: App
    section Analyse
      Compare growth metrics: 5: App
      Check best performer badge: 5: App
      Run investment calculator: 4: User
      Check Beat the Market verdict: 5: App
      Read Risk vs. Return scatter: 5: App
    section Share
      Copy live URL: 5: User
      Share with colleagues: 5: User
```

![User journey diagram](https://mermaid.ink/img/pako:eNp1kMFOw0AMRO98xXwEXHIrhQtCIFHK3d24G7eb3ZXttISvR6QtqAWuozfjJ2_KoJnHKwBw8cRYGiseDnGD-_eaikqOuJWIVw4dFl7C1qaGcXApGc-VM2a1TiHwRDuJ5AwvSLJjLF8eG9w00_aRmdWKVKg1SDan7GmckNPKafogwLgjp2N1wYmDwyYPrLX0MGl5RfrrSLsZzNF-uSjlyLAkLWuD6zPuTXiPXLSnJB_coqoERuhI_U-pWaY0Gh_b89JXUkbUsvcOPbtKsLMiMO84bLFic1TWddGeFStqI1-AL0OG5B2b95wdgVIYEnm5kD6pLDrSH5E6_vvwCcRevEMoKTHFge0b-gR-IKIu)

---

## Quick start

```bash
pip install streamlit pandas plotly streamlit-autorefresh
streamlit run app.py
```

---

## Files

| File | Purpose |
|------|---------|
| `app.py` | Main Streamlit application |
| `requirements.txt` | Python dependencies for Streamlit Cloud |
| `.streamlit/config.toml` | Warm parchment colour theme |
| `.gitignore` | Keeps secrets and temp files out of git |
| `README.md` | This file |

---

## Reflection

The MCP that helped me the most was **GitHub** — it pushed my code to a public repository with a single instruction, which I would not have known how to do on my own. **Fetch** was also very useful because it pulled real facts about the companies straight from the web, so the "Did you know?" section in the app shows genuine information instead of something I had to make up. The thing that surprised me most was **Playwright** — I expected to have to open a browser myself and take a screenshot manually, but it opened the live app, waited for it to load, and took the screenshot completely on its own, like a real QA tester. I ended up adding extra features like a Beat the Market indicator and a Risk vs. Return chart, and I was surprised by how easy it was to keep adding things just by describing what I wanted in plain English.
