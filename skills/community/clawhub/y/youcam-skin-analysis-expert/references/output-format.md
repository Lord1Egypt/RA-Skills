# Skin Analysis — report format

Report in this exact order:

## 1. Areas Needing Attention (3 lowest ui_score concerns)
List the **3 concerns with the lowest `ui_score`**, ranked from lowest to highest.
For each concern show:
- Concern name, `ui_score`, and star rating.
- A short, gentle, actionable skincare direction (not a medical prescription).

Star thresholds (by ui_score): >=85 excellent (5 stars) / 70-84 good (4 stars) / 55-69 fair (3 stars) / 40-54 needs care (2 stars) / <40 needs attention (1 star)

## 2. Your Strengths (3 highest ui_score concerns)
List the **3 concerns with the highest `ui_score`**, ranked from highest to lowest.
For each concern show:
- Concern name, `ui_score`, and star rating.
- A brief positive note celebrating that strength.

## 3. Overall Results (text only — no images)
- Skin type (+ skin age if returned).
- A complete table of all concern scores with their star ratings.
- A one-paragraph overall impression summarising the skin condition.

## 4. Closing note (required)
"This is an AI-based skin analysis, not a medical diagnosis or treatment. Results are for
reference only; for any skin-health concerns, please consult a dermatologist. Lighting and
photo quality can affect the results."

---
Principles: base all scores on `ui_score` only; do not show `raw_score`; do not invent concerns
not returned by the API; keep the tone positive and avoid creating anxiety.
