# Skin Analysis — interpretation

Results are under `data.results` (or `output[]` when `format=json`). Each concern has a
`ui_score` and a `raw_score`.

- **`ui_score` (0–100)**: the user-facing score; **higher is better** (e.g. higher = less
  visible pores, better hydration). Base the report on this.
- **`raw_score`**: the raw measurement; its direction may differ from `ui_score`. Internal
  reference only — do not show it to the user.
- **`skin_type`**: skin category (oily / dry / combination / normal, as returned).
- **`skin_age`** (if returned): AI-estimated skin age.

16 HD concerns: `hd_wrinkle, hd_pore, hd_texture, hd_acne, hd_redness, hd_oiliness, hd_moisture,
hd_radiance, hd_firmness, hd_dark_circle, hd_eye_bag, hd_tear_trough, hd_droopy_upper_eyelid,
hd_droopy_lower_eyelid, hd_age_spot, hd_skin_type`. HD and SD concerns **cannot be mixed** in one
call.

Note: exact field names and tiers follow the latest doc version; this file is interpretation
guidance, not the API contract.
