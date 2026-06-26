# Playbooks — seasonal-flight

> CLI command sequences only. Knowledge is for parameter mapping — never answer without executing.

## Quick Reference

| Parameter | Flag | This Skill |
|-----------|------|-----------|
| dep-date-start | `--dep-date-start` | Seasonal window start |
| dep-date-end | `--dep-date-end` | Seasonal window end |
| sort-type | `--sort-type` | Default: **2** (recommended), off-season: **3** |

---

## Playbook A: Summer Seasonal Flights

**Trigger:** User says "summer flight", "暑期航班", "暑假机票".

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date-start {summer_start} --dep-date-end {summer_end} --sort-type 3
```

**Output:** Cheapest flights within summer window (Jul-Aug).

---

## Playbook B: Winter Seasonal Flights

**Trigger:** User says "winter flight", "冬季航班", "寒假机票".

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date-start {winter_start} --dep-date-end {winter_end} --sort-type 2
```

**Output:** Recommended flights within winter window (Dec-Feb).

---

## Playbook C: Off-Season Bargain

**Trigger:** User says "off-season flight", "淡季机票", "错峰出行".

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date-start {off_start} --dep-date-end {off_end} --sort-type 3
```

**Output:** Cheapest flights during off-peak season.

---

## Playbook D: Broad Search (no seasonal flights found)

**Trigger:** Playbook A/B/C returns 0 results.

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --sort-type 2
flyai keyword-search --query "{origin} to {destination} seasonal flights {season}"
```

**Output:** Broader search + keyword fallback.
