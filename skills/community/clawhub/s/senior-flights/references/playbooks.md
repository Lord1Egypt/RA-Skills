# Playbooks — senior-flights

> CLI command sequences only. Knowledge is for parameter mapping — never answer without executing.

## Quick Reference

| Parameter | Flag | This Skill |
|-----------|------|-----------|
| dep-hour-start | `--dep-hour-start` | Default: **6** (morning) |
| dep-hour-end | `--dep-hour-end` | Default: **18** (avoid late night) |
| sort-type | `--sort-type` | Default: **2** (recommended) |
| journey-type | `--journey-type` | Optional: 1=direct (preferred) |

---

## Playbook A: Recommended Senior Flight

**Trigger:** User says "senior flights", "老年机票".

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --dep-hour-start 6 --dep-hour-end 18 --sort-type 2
```

**Output:** Morning-to-evening flights, best recommended options.

---

## Playbook B: Shortest Senior Flight

**Trigger:** User says "shortest flight for elderly", "老人最短航班".

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --dep-hour-start 6 --dep-hour-end 18 --sort-type 4
```

**Output:** Shortest duration flights within comfortable hours.

---

## Playbook C: Direct-Only Senior Flight

**Trigger:** User says "direct senior flight", "老人直飞".

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --dep-hour-start 6 --dep-hour-end 18 --journey-type 1 --sort-type 8
```

**Output:** Direct flights only, morning-to-evening.

---

## Playbook D: Broad Search (no suitable flights)

**Trigger:** Playbook A/B/C returns 0 results.

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --sort-type 2
flyai keyword-search --query "{origin} to {destination} senior discount flights"
```

**Output:** Broader search without hour filter + keyword fallback.
