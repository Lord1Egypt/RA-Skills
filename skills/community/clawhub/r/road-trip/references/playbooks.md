# Playbooks — road-trip

> CLI command sequences. Knowledge is for parameter mapping — never answer without executing.

---

## Playbook A: Road Trip

**Trigger:** "self-drive trip"

```bash
flyai keyword-search --query "租车 {city}"
flyai search-poi along route
```

**Output emphasis:** Car rental + scenic stops.

---

## Playbook B: Scenic Route

**Trigger:** "scenic drive"

```bash
search-poi at multiple points along route
```

**Output emphasis:** Focus on scenic waypoints.

---

## Playbook C: Family Road Trip

**Trigger:** "drive with family"

```bash
Car rental + family-friendly stops + hotels along route
```

**Output emphasis:** Family road trip with rest stops.

---

