# Playbooks — three-day-trip-planner

> CLI command sequences. Knowledge is for parameter mapping — never answer without executing.

---

## Playbook A: 3-Day City

**Trigger:** "3 days in {city}"

```bash
flyai search-flight → search-hotels → search-poi (multiple categories)
```

**Output emphasis:** 3-day single city deep dive.

---

## Playbook B: 3-Day Multi-City

**Trigger:** "3 days 2 cities"

```bash
Flights + hotels per city + poi per city
```

**Output emphasis:** Split 3 days across 2 cities.

---

