# Playbooks — student-flights

> CLI command sequences. Knowledge is for parameter mapping — never answer without executing.

---

## Playbook A: Ultra Budget

**Trigger:** "cheapest possible", "最便宜"

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --sort-type 3
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --dep-hour-start 21 --sort-type 3
flyai search-flight --origin "{o}" --destination "{d}" --dep-date-start {date-3} --dep-date-end {date+3} --sort-type 3
```

**Output emphasis:** Triple search: standard + red-eye + flexible dates.

---

## Playbook B: Holiday Budget

**Trigger:** "student holiday trip"

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date-start {off_peak_start} --dep-date-end {off_peak_end} --sort-type 3
```

**Output emphasis:** Search off-peak seasons for student holidays.

---

## Playbook C: Group Student Travel

**Trigger:** "和同学一起飞"

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --sort-type 3
# Note: some airlines offer group discounts for 10+ passengers
```

**Output emphasis:** Note group discount possibilities.

---

