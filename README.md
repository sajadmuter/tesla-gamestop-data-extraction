# Tesla and GameStop Stock and Revenue Exploration

Course-based Python learning exercise for retrieving stock history, extracting quarterly revenue, and plotting series with explicit dates and units.

## Learning question

How can data from different sources be prepared and visualized without confusing dates, revenue units, or text and numeric values?

## Files

- [`Final Assignment(2).ipynb`](<Final Assignment(2).ipynb>): the notebook.
- `analysis_utils.py`: extraction, cleaning and plotting helpers.
- `validate_analysis.py`: offline checks with synthetic fixtures.
- `DATA-SOURCES.md` and `THIRD_PARTY_NOTICES.md`: provenance and attribution.

## Corrections applied

- Created every variable explicitly and removed repeated download and plotting definitions.
- Selected quarterly revenue by table heading rather than position.
- Converted revenue to numbers and dates to datetime, sorted chronologically, and rejected duplicate dates.
- Fixed the historical cutoff to 2021-06-14 and labelled revenue as USD millions.
- Added HTTP timeout handling and explicit `auto_adjust=False` for price retrieval.
- Cleared the old notebook outputs; they must not be interpreted as results of the corrected code.

## Run

Python 3 is required. Create an isolated environment:

```bash
python -m venv .venv
```

Windows:

```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe validate_analysis.py
.venv\Scripts\python.exe -m jupyter lab
```

macOS / Linux: replace `.venv\Scripts\python.exe` with `.venv/bin/python`.

Open `Final Assignment(2).ipynb` and run all cells from a fresh kernel. Internet access is required for the live retrieval cells.

## Validation status

Offline checks passed on synthetic fixtures for quarterly-table selection, currency cleaning, date sorting, invalid values, duplicate rejection, timezone handling, the historical cutoff and chart units. Notebook cells were also exercised sequentially with mocked remote inputs.

**Live-source retrieval has not been verified.** Dependencies are listed, not version-locked. No market findings or employer business impact are claimed.

## Sources and scope

Yahoo Finance through yfinance provides price history. IBM Skills Network course HTML provides historical revenue snapshots. Their time windows may differ. This is a learning exercise, not a financial forecast or telecom analytics project.

Original course author and copyright notices are preserved in the notebook. No blanket MIT license is asserted for third-party course material.
