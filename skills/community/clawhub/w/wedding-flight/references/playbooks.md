# Playbooks — wedding-flight

> Scenario-specific CLI command templates.

---

## Playbook A: Honeymoon Flight

**Trigger:** "honeymoon flight", "蜜月机票", "蜜月旅行"

**Context:** Couple booking direct flights for honeymoon, prefer recommended sorting.

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --journey-type 1 --sort-type 2
```

**Fallback if 0 results:** Remove `--journey-type` to include connecting flights.

---

## Playbook B: Wedding Guest Group Search

**Trigger:** "wedding guest flight", "婚礼航班", "婚庆出行"

**Context:** Multiple guests flying to wedding venue, economy class, best value.

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --seat-class-name economy --sort-type 2
```

**Fallback if 0 results:** Try `--sort-type 3` for cheapest options.

---

## Playbook C: Flexible Date Honeymoon

**Trigger:** "honeymoon flexible dates", "蜜月旅行随便哪天", "婚庆假期灵活"

**Context:** Couple with flexible schedule, searching across a date window.

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date-start {start} --dep-date-end {end} --journey-type 1 --sort-type 2
```

**Fallback if 0 results:** Remove `--journey-type 1` or widen date range.

---

## Playbook D: Broad Search (last resort)

**Trigger:** All above playbooks return 0 results.

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --sort-type 2
flyai keyword-search --query "{origin} to {destination} wedding honeymoon flights"
```
