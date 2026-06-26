# Playbooks — red-flights

> CLI command sequences only. Knowledge is for parameter mapping — never answer without executing.

## Quick Reference

| Parameter | Flag | This Skill |
|-----------|------|-----------|
| dep-hour-start | `--dep-hour-start` | Default: **21** (9 PM) |
| dep-hour-end | `--dep-hour-end` | Default: **6** (6 AM) |
| sort-type | `--sort-type` | Default: **3** (price ascending) |
| journey-type | `--journey-type` | Optional: **1** (direct only) |

---

## Playbook A: Cheapest Red Eye

**Trigger:** User says "cheapest red eye", "最便宜的红眼航班".

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --dep-hour-start 21 --dep-hour-end 6 --sort-type 3
```

**Output:** Red eye flights sorted by lowest price.

---

## Playbook B: Latest Departure Red Eye

**Trigger:** User says "latest red eye", "最晚的红眼航班".

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --dep-hour-start 21 --dep-hour-end 6 --sort-type 7
```

**Output:** Red eye flights sorted by latest departure time.

---

## Playbook C: Direct Red Eye Only

**Trigger:** User says "direct red eye", "直飞红眼".

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --dep-hour-start 21 --dep-hour-end 6 --journey-type 1 --sort-type 3
```

**Output:** Non-stop red eye flights only, sorted by price.

---

## Playbook D: Broad Search (no red eyes found)

**Trigger:** Playbook A/B/C returns 0 results.

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --sort-type 3
flyai keyword-search --query "{origin} to {destination} late night flights"
```

**Output:** Broader results without time filter, plus keyword fallback.
