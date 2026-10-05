"""Offline checks using synthetic fixtures, not market observations."""
import sys
import types
from unittest.mock import patch

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from analysis_utils import clean_prices, clean_revenue, extract_quarterly_revenue, make_graph, stock_history


def check_rejects(call, label):
    try:
        call()
    except (ValueError, TypeError):
        return
    raise AssertionError(label)


def run_checks():
    html = """<table><tr><th>Tesla Annual Revenue</th><th>Value</th></tr>
    <tr><td>2020</td><td>$999,999</td></tr></table>
    <table><tr><th>Tesla Quarterly Revenue</th><th>USD millions</th></tr>
    <tr><td>2020-06-30</td><td>$1,200</td></tr>
    <tr><td>2020-03-31</td><td>$900</td></tr>
    <tr><td>2019-12-31</td><td></td></tr></table>"""
    revenue = extract_quarterly_revenue(html, "Tesla")
    assert revenue["Revenue"].tolist() == [900, 1200]
    assert revenue["Date"].is_monotonic_increasing
    check_rejects(lambda: clean_revenue(pd.DataFrame({"Date": ["2020-01-01"] * 2, "Revenue": [1, 2]})), "duplicate dates accepted")
    check_rejects(lambda: clean_revenue(pd.DataFrame({"Date": ["bad"], "Revenue": [1]})), "invalid date accepted")
    check_rejects(lambda: clean_revenue(pd.DataFrame({"Date": ["2020-01-01"], "Revenue": ["bad"]})), "invalid revenue accepted")
    index = pd.DatetimeIndex(["2020-06-30", "2020-03-31", "2021-07-01"], tz="America/New_York", name="Date")
    raw_prices = pd.DataFrame({"Close": [20, 10, 30], "Open": [19, 9, 29]}, index=index)
    prices = clean_prices(raw_prices)
    assert prices["Date"].is_monotonic_increasing and prices["Date"].dt.tz is None
    fake_yf = types.SimpleNamespace(Ticker=lambda symbol: types.SimpleNamespace(history=lambda **kwargs: raw_prices.copy()))
    with patch.dict(sys.modules, {"yfinance": fake_yf}):
        history = stock_history("TSLA", "2021-06-14")
    assert len(history) == 2 and history["Close"].tolist() == [10, 20]
    fig = make_graph(raw_prices, revenue, "Synthetic fixture", "2021-06-14")
    assert fig.axes[1].get_ylabel() == "USD millions"
    assert fig.axes[1].lines[0].get_ydata().tolist() == [900, 1200]
    plt.close(fig)
    print("PASS: quarterly selection, numeric conversion, sorting, empty handling, invalid values, duplicate rejection, timezone handling, cutoff and chart units.")


if __name__ == "__main__":
    run_checks()
