# Playbooks — unique-homestay

> CLI command sequences. Knowledge is for parameter mapping — never answer without executing.

---

## Playbook A: Best Rated Homestay

**Trigger:** "best homestay", "评价最好的民宿"

```bash
flyai search-hotel --dest-name "{city}" --hotel-types "民宿" --sort rate_desc --check-in-date {in} --check-out-date {out}
```

**Output emphasis:** Top-rated homestays.

---

## Playbook B: Budget Homestay

**Trigger:** "cheap homestay"

```bash
flyai search-hotel --dest-name "{city}" --hotel-types "民宿" --sort price_asc --check-in-date {in} --check-out-date {out}
```

**Output emphasis:** Affordable homestays.

---

## Playbook C: Unique Stay

**Trigger:** "独特住宿", "特色民宿"

```bash
flyai search-hotel --dest-name "{city}" --hotel-types "民宿" --key-words "特色" --sort rate_desc --check-in-date {in} --check-out-date {out}
```

**Output emphasis:** Character stays — treehouse, cave, etc.

---

