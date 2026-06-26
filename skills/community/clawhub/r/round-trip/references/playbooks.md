# Playbooks — round-trip

> CLI command sequences only. Knowledge is for parameter mapping — never answer without executing.

## Quick Reference

| Parameter | Flag | This Skill |
|-----------|------|-----------|
| back-date  sort-type | `--sort-type` | Default: **2** (recommended) |
| back-date-start  back-date-end | `--back-date-end` | Optional: flexible return end |

---

## Playbook A: Recommended Round-Trip

**Trigger:** User says "round-trip flights", "往返机票".

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {dep_date} --sort-type 2
```

---

## Playbook B: Cheapest Round-Trip

**Trigger:** User says "cheapest round-trip", "最便宜往返".

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {dep_date} --sort-type 3
```

---

## Playbook C: Flexible Return Date

**Trigger:** User says "flexible return date", "回程日期灵活".

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {dep_date} --sort-type 3
```

---

## Playbook D: Broad Search

**Trigger:** Playbook A/B/C returns 0 results.

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {dep_date} --sort-type 2
flyai keyword-search --query "{origin} to {destination} round-trip flights"
```
