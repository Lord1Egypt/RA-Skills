# Playbooks — rafting-spots

> CLI command sequences. Knowledge is for parameter mapping — never answer without executing.

---

## Playbook A: Rafting

**Trigger:** "rafting near me"

```bash
flyai search-poi --city-name "{city}" --category "漂流"
```

**Output emphasis:** Rafting experiences.

---

## Playbook B: Extreme Rafting

**Trigger:** "extreme rapids"

```bash
flyai search-poi --city-name "{city}" --keyword "激流"
```

**Output emphasis:** Advanced/extreme rafting.

---

## Playbook C: Family Rafting

**Trigger:** "gentle rafting"

```bash
flyai search-poi --city-name "{city}" --keyword "漂流"
```

**Output emphasis:** Family-friendly floating.

---

