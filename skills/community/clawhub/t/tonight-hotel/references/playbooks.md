# Playbooks — tonight-hotel

> CLI command sequences. Knowledge is for parameter mapping — never answer without executing.

---

## Playbook A: Tonight Cheapest

**Trigger:** "hotel tonight", "今晚住哪"

```bash
flyai search-hotel --dest-name "{city}" --check-in-date {today} --check-out-date {tomorrow} --sort price_asc
```

**Output emphasis:** Available tonight, cheapest first.

---

## Playbook B: Tonight Near Me

**Trigger:** "nearest hotel tonight"

```bash
flyai search-hotel --dest-name "{city}" --check-in-date {today} --check-out-date {tomorrow} --sort distance_asc
```

**Output emphasis:** Closest available hotels tonight.

---

## Playbook C: Tonight Decent

**Trigger:** "decent hotel tonight"

```bash
flyai search-hotel --dest-name "{city}" --check-in-date {today} --check-out-date {tomorrow} --hotel-stars 3,4 --sort price_asc
```

**Output emphasis:** 3-4 star available tonight.

---

