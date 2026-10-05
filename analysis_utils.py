"""Helpers for course-based stock and revenue exploration.

Refactored learning code. See THIRD_PARTY_NOTICES.md for course attribution.
Live-source availability is separate from the offline checks.
"""
from io import StringIO
from urllib.request import urlopen

import pandas as pd
import matplotlib.pyplot as plt


def download_text(url):
    """Download a UTF-8 resource; HTTP errors propagate to the caller."""
    with urlopen(url, timeout=30) as response:
        return response.read().decode("utf-8")


def clean_revenue(frame):
    """Return sorted quarterly revenue, with dates and USD-million values."""
    if frame.shape[1] != 2:
        raise ValueError("Expected exactly two revenue table columns.")
    frame = frame.copy()
    frame.columns = ["Date", "Revenue"]
    values = frame["Revenue"].astype("string").str.strip()
    frame = frame.loc[frame["Date"].notna() & values.notna() & values.ne("")].copy()
    values = values.loc[frame.index].str.replace(r"[$,]", "", regex=True).str.strip()
    frame["Revenue"] = pd.to_numeric(values, errors="raise")
    frame["Date"] = pd.to_datetime(frame["Date"], format="%Y-%m-%d", errors="raise")
    if frame.empty or frame[["Date", "Revenue"]].isna().any().any():
        raise ValueError("Revenue data is empty or contains invalid values.")
    if frame["Date"].duplicated().any():
        raise ValueError("Duplicate quarterly revenue dates.")
    return frame.sort_values("Date").reset_index(drop=True)


def extract_quarterly_revenue(html_text, company):
    """Select the quarterly table by its heading, rather than its position."""
    tables = pd.read_html(
        StringIO(html_text), match=f"{company} Quarterly Revenue", flavor="lxml"
    )
    if len(tables) != 1:
        raise ValueError("Expected one identifiable quarterly revenue table.")
    return clean_revenue(tables[0])


def clean_prices(frame, price_column="Close"):
    frame = frame.copy()
    if "Date" not in frame.columns:
        frame = frame.reset_index()
    if "Date" not in frame.columns or price_column not in frame.columns:
        raise ValueError("Missing Date or requested price column.")
    frame["Date"] = pd.to_datetime(frame["Date"], errors="raise").dt.tz_localize(None)
    frame[price_column] = pd.to_numeric(frame[price_column], errors="raise")
    if frame.empty or frame[["Date", price_column]].isna().any().any():
        raise ValueError("Price data is empty or contains invalid values.")
    if frame["Date"].duplicated().any():
        raise ValueError("Duplicate stock price dates.")
    return frame.sort_values("Date").reset_index(drop=True)


def stock_history(symbol, cutoff, price_column="Close"):
    import yfinance as yf
    # The end parameter is exclusive. auto_adjust is explicit for reproducibility.
    end = (pd.Timestamp(cutoff) + pd.Timedelta(days=1)).date().isoformat()
    frame = yf.Ticker(symbol).history(
        start="2000-01-01", end=end, auto_adjust=False, timeout=30
    )
    frame = clean_prices(frame, price_column)
    return frame.loc[frame["Date"] <= pd.Timestamp(cutoff)].reset_index(drop=True)


def make_graph(stock_data, revenue_data, company, cutoff):
    prices = clean_prices(stock_data)
    revenue = clean_revenue(revenue_data)
    limit = pd.Timestamp(cutoff)
    prices = prices.loc[prices["Date"] <= limit]
    revenue = revenue.loc[revenue["Date"] <= limit]
    if prices.empty or revenue.empty:
        raise ValueError("No observations within the requested cutoff.")
    fig, axes = plt.subplots(2, 1, figsize=(11, 7))
    axes[0].plot(prices["Date"], prices["Close"])
    axes[0].set(title=f"{company}: closing price", ylabel="USD", xlabel="Date")
    axes[1].plot(revenue["Date"], revenue["Revenue"], color="tab:green")
    axes[1].set(title=f"{company}: quarterly revenue", ylabel="USD millions", xlabel="Date")
    fig.autofmt_xdate()
    fig.tight_layout()
    return fig
