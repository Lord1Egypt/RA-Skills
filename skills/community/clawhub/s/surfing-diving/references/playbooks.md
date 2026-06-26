# Playbooks — surfing-diving

> CLI command sequences. Knowledge is for parameter mapping — never answer without executing.

---

## Playbook A: Surfing

**Trigger:** "surfing spots"

```bash
flyai search-poi --city-name "{city}" --category "冲浪"
```

**Output emphasis:** Surfing beaches.

---

## Playbook B: Diving

**Trigger:** "diving sites"

```bash
flyai search-poi --city-name "{city}" --category "潜水"
```

**Output emphasis:** Scuba diving locations.

---

## Playbook C: Snorkeling

**Trigger:** "snorkeling"

```bash
flyai search-poi --city-name "{city}" --keyword "浮潜"
```

**Output emphasis:** Snorkeling-friendly spots.

---

