# Hair Diagnostics — interpretation & output

Each API returns `data.results.hair_<x>{ mapping, term }` (length has term only). Present the
**term** as the main value.

- **Density (hair_density)**: term ∈ [Extremely Low Density, Low Density, Medium Density,
  High Density]. `mapping` is a float string (e.g. "2.16") — internal reference only.
- **Type (hair_type)**: Andre Walker–style scale; mapping like "2b to 2c", term like
  "Medium to Thick Wavy".
- **Frizziness (hair_frizziness)**: mapping 0–3; term ∈ [Not Frizzy, Slightly Frizzy, Frizzy,
  Extreme Frizzy].
- **Length (hair_length)**: term like "ear length", "long hair" (term only, no numeric mapping).

## Output format
1. One row per selected metric: metric | level (term) | one-line note.
2. Overall summary across the selected metrics.
3. Care directions: gentle, non-medical tips based on frizziness/density (e.g. high frizz →
   hydrating care, avoid high heat).
4. Closing note: "This is an AI-based hair detection, not a medical diagnosis; for hair-loss or
   scalp concerns, consult a dermatologist."

Exact fields follow the latest doc version; this file is interpretation guidance.
