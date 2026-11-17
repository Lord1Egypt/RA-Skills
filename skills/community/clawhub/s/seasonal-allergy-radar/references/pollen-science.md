# Pollen, Correlation, and Pre-Medication — Reference

## Why pollen calendars work

Wind-pollinated plants release pollen on photoperiod and temperature cues
that are stable year-to-year within a climate zone. Birch in temperate
Europe/North America peaks within ±2 weeks of the same date annually;
grass follows soil temperature; ragweed waits for decreasing day length
after summer solstice. That stability is what makes a static zone calendar
useful even without this year's live counts.

## Zone calendars (month-level risk 0–3)

### temperate-northern (US north/Europe north/Japan)
Tree: alder Feb–Mar(2→3), birch Apr(3), oak Apr–May(3), pine May–Jun(1, large grain, low allergen)
Grass: May(2) Jun(3) Jul(2)
Weed: plantain Jun–Aug(1), ragweed Aug(3) Sep(2) (NA mostly), mugwort Jul–Aug(2)

### mediterranean
Tree: cypress Jan–Feb(3! major allergen), olive Apr–Jun(3), plane Mar–Apr(2)
Grass: Apr(2) May(3) Jun(2)
Weed: pellitory Jun–Sep(2), amaranth Aug–Sep(2)

### continental (interior US/Canada/E-Europe/Russia)
Tree: birch Apr(2) May(3), oak May(2)
Grass: Jun(3) Jul(2)
Weed: mugwort Jul(3) Aug(2), ragweed Aug(3) Sep(2) (NA)

### subtropical (FL/Gulf/southern hemisphere coastal)
Tree: near-year-round (oak Jan–Mar(3), cedar Dec–Feb(3 TX hill country))
Grass: Bermuda Mar–Oct(3 long), Bahia May–Sep(2)
Weed: ragweed Jul–Nov(2)

### coastal-low (maritime, strong onshore winds)
Overall low; grass May–Aug(2) is usually the only notable season.

## The correlation method

Daily risk curve r_c(t) per class c from the tables (linear between month
scores). Your log s(t). Pearson correlation at lag L:
ρ_c(L) = corr(s(t), r_c(t−L)) for L in 0..7.

- |ρ| ≥ 0.5 with plausible lag → strong personal trigger
- 0.35–0.5 → likely contributor
- < 0.35 → no clear driver

Lag interpretation: 0–1 d direct response; 2–3 d priming (each exposure
lowers next-exposure threshold); >3 d usually weather confound (same
pressure system brings both pollen and symptoms via sinuses).

## Medication timing facts

- **2nd-gen antihistamines** (cetirizine, loratadine, fexofenadine):
  onset 1–2 h, but regular dosing beats PRN; start season −10 to −14 d.
- **Nasal corticosteroids** (fluticasone, mometasone): peak effect after
  several days to 2 weeks; start season −2 weeks; the single most
  effective allergic rhinitis intervention in trials.
- **Antihistamine eye drops** (ketotifen OTC): PRN plus pre-exposure
  before high-pollen outings.
- **Montelukast**: reserved, prescription, psychiatric side-effect box
  warnings — allergist conversation, not self-plan.
- **Immunotherapy** (tablets/injections): if your log shows ≥2 seasons of
  ≥3/5 scores lasting ≥6 weeks, that's the referral threshold worth
  discussing with a doctor.

## Logging protocol that produces clean correlations

- Fixed daily anchor time (evening) — recall bias halves.
- Score BEFORE taking rescue meds, else you log treatment effect.
- Note outliers: windows open, mowing, rain, travel out of zone.
- Zeros matter more than spikes; missing days are neutral (interpolated),
  but >30% missing in a season wrecks the lag search.

## Confounds checklist

- Mold spikes after rain/humidity — not in pollen calendars; note it.
- Air pollution (ozone) synergizes with pollen allergenicity in cities.
- Viral colds in spring overlap tree season: itchy eyes favor allergy,
  fever favors virus.
- Oral allergy syndrome (pollen-food) — see SKILL.md pitfalls.

## Limits

Static calendars don't know this year's weather: a warm February can start
cypress/birch 2–3 weeks early; drought suppresses grass. Use the forecast
flags as planning defaults and live counts/your own nose as ground truth.
Not a medical device; medication decisions belong with a pharmacist/doctor.
