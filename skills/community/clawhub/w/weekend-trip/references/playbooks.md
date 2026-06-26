# Playbooks — weekend-trip

> CLI command sequences. Knowledge is for parameter mapping — never answer without executing.

---

## Playbook A: Weekend Auto-Plan

**Trigger:** "周末去哪玩"

```bash
flyai search-flight --origin "{o}" --destination "{nearby}" --dep-date {fri} --back-date {sun} --sort-type 3
flyai search-hotel --dest-name "{nearby}" --check-in-date {fri} --check-out-date {sun} --sort rate_desc
flyai search-poi --city-name "{nearby}" --poi-level 5
```

**Output emphasis:** Auto-plan nearby weekend.

---

## Playbook B: Budget Weekend

**Trigger:** "cheap weekend escape"

```bash
flyai search-flight --origin "{o}" --destination "{nearby}" --dep-date {fri} --back-date {sun} --sort-type 3
flyai search-hotel --dest-name "{nearby}" --sort price_asc --check-in-date {fri} --check-out-date {sun}
```

**Output emphasis:** Budget-friendly weekend.

---

