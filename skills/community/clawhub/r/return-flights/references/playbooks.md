# Playbooks — return-flights

> CLI command sequences. Knowledge is for parameter mapping — never answer without executing.

---

## Playbook A: Bundled Round Trip

**Trigger:** "round trip price", "往返总价"

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {out} --back-date {ret} --sort-type 3
```

**Output emphasis:** Show bundled round-trip options.

---

## Playbook B: Separate Legs Compare

**Trigger:** "cheapest combination"

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {out} --sort-type 3
flyai search-flight --origin "{d}" --destination "{o}" --dep-date {ret} --sort-type 3
```

**Output emphasis:** Compare: bundled total vs separate legs total.

---

## Playbook C: Flexible Return

**Trigger:** "return date flexible"

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {out} --sort-type 3
flyai search-flight --origin "{d}" --destination "{o}" --dep-date-start {ret-2} --dep-date-end {ret+2} --sort-type 3
```

**Output emphasis:** Fixed outbound + flexible return for max savings.

---

