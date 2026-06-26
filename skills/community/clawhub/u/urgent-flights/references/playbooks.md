# Playbooks — urgent-flights

> CLI command sequences. Knowledge is for parameter mapping — never answer without executing.

---

## Playbook A: Fly Tonight

**Trigger:** "tonight", "今晚就飞"

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {today} --sort-type 6
```

**Output emphasis:** Show earliest available flights tonight.

---

## Playbook B: Tomorrow Morning

**Trigger:** "tomorrow", "明天一早"

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {tomorrow} --dep-hour-start 5 --dep-hour-end 12 --sort-type 6
```

**Output emphasis:** Morning flights tomorrow, earliest first.

---

## Playbook C: Cheapest ASAP

**Trigger:** "最便宜的 ASAP"

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {today} --sort-type 3
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {tomorrow} --sort-type 3
```

**Output emphasis:** Compare today vs tomorrow prices.

---

