# Data Sources

| Dataset | Provider / access route | Use | Limitations |
| --- | --- | --- | --- |
| TSLA and GME price history | Yahoo Finance through yfinance | Historical stock price exploration | Live retrieval; document download date and adjustment settings |
| Tesla revenue | IBM Skills Network course HTML | Revenue extraction exercise | Historical course snapshot; validate frequency and USD-million units |
| GameStop revenue | IBM Skills Network course HTML | Revenue extraction exercise | Historical course snapshot; validate frequency and USD-million units |

## Source URLs

- Tesla: https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm
- GameStop: https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html
- Stock retrieval: `yf.Ticker("TSLA").history(period="max")` and `yf.Ticker("GME").history(period="max")`.

## Documentation gaps

The notebook does not document a controlled data snapshot or a fresh retrieval date. Commit dates are not treated as data retrieval dates.

For a reproducible revision, record retrieval dates, coverage, columns, units, transformations, missing values, duplicate checks, and source usage terms.

This repository does not claim ownership of external data.

## Refactored retrieval settings

Price retrieval sets auto_adjust=False explicitly. The notebook declares a fixed cutoff. No new live download date is claimed; source availability and coverage must be recorded after a successful live run.
