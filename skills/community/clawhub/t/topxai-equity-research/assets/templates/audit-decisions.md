# <TICKER> report · Round N audit dispositions (vN -> vN+1)

> Template. Save as `research/<report-id>/audit-vN-decisions.md`.

Disposition date: <YYYY-MM-DD>. Audit files: `audit-vN-<lane>.md` (lane initial X) ...
The valuation model `calc/model.py` moves to vN+1 and its output is `calc/model-vN+1-output.txt`. Valuation numbers in the
body follow that output and are never calculated by hand.

## 0. Did the conclusion flip?
Whether the rating or target price changed, which finding triggered the change, in one paragraph.

## 1. Disposition of each finding
| ID | Finding (one sentence) | Verdict (upheld / partly / rejected) | Action | Where (chapter / table / model input) | In the Appendix C revision log? |
|---|---|---|---|---|---|

## 2. Why rejected findings are rejected
For each, give the reason for not changing and the evidence. For the skeptic lane, state which parameter combination would
need what evidence grade to flip the rating.
