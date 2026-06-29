# 📈 Stock Price Explorer

A Streamlit web app that lets you compare how the big tech stocks (AAPL, GOOG, MSFT, AMZN, NFLX, FB) have grown since January 2018.

**Live app:** _[paste your Streamlit Cloud URL here after deploying]_

---

## Features

- **Normalized price chart** — compare growth on the same scale
- **Best performer badge** — highlights the top stock in your selection
- **Date-range slider** — zoom into any period since Jan 2018
- **Investment calculator** — "what if I invested $1,000?"
- **Growth bar chart** — side-by-side total growth comparison
- **Volatility indicator** — which stock bounced around the most
- **Did you know?** — a real-world fact fetched about Apple's history
- **Custom dark theme** — branded red-on-dark colour scheme via `.streamlit/config.toml`

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

    style A fill:#f0f4ff,stroke:#4a6cf7
    style B fill:#ff4b4b,stroke:#cc0000,color:#fff
    style C fill:#24292e,stroke:#000,color:#fff
    style D fill:#ff4b4b,stroke:#cc0000,color:#fff
    style E fill:#00c49a,stroke:#009977,color:#fff
    style F fill:#f0f4ff,stroke:#4a6cf7
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
    section Share
      Copy live URL: 5: User
      Share with colleagues: 5: User
```

![User journey diagram](https://mermaid.ink/img/pako:eNp1kMFOw0AMRO98xXwEXHIrhQtCIFHK3d24G7eb3ZXttISvR6QtqAWuozfjJ2_KoJnHKwBw8cRYGiseDnGD-_eaikqOuJWIVw4dFl7C1qaGcXApGc-VM2a1TiHwRDuJ5AwvSLJjLF8eG9w00_aRmdWKVKg1SDan7GmckNPKafogwLgjp2N1wYmDwyYPrLX0MGl5RfrrSLsZzNF-uSjlyLAkLWuD6zPuTXiPXLSnJB_coqoERuhI_U-pWaY0Gh_b89JXUkbUsvcOPbtKsLMiMO84bLFic1TWddGeFStqI1-AL0OG5B2b95wdgVIYEnm5kD6pLDrSH5E6_vvwCcRevEMoKTHFge0b-gR-IKIu)

---

## Quick start

```bash
pip install streamlit pandas plotly
streamlit run app.py
```

---

## Files

| File | Purpose |
|------|---------|
| `app.py` | Main Streamlit application |
| `requirements.txt` | Python dependencies for Streamlit Cloud |
| `.streamlit/config.toml` | Custom dark theme |
| `.gitignore` | Keeps secrets and temp files out of git |
| `README.md` | This file |
| `Reflection.txt` | Personal reflection on the build process |

---

## Reflection

Building this app showed how powerful MCP skill packs are for accelerating development. **Context7** was the most helpful — it ensured the Streamlit code used up-to-date APIs rather than deprecated patterns. The most surprising thing was how seamlessly **Playwright** acted as a robot QA tester: it opened the live URL, waited for the app to wake up, and took a screenshot entirely on its own — no manual browser interaction needed.
