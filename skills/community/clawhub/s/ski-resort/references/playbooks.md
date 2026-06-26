# Playbooks — ski-resort

> CLI command sequences. Knowledge is for parameter mapping — never answer without executing.

---

## Playbook A: Ski Resorts

**Trigger:** "skiing near me"

```bash
flyai search-poi --city-name "{city}" --category "滑雪"
```

**Output emphasis:** Ski resorts and snow parks.

---

## Playbook B: Beginner Ski

**Trigger:** "learn to ski"

```bash
flyai search-poi --city-name "{city}" --keyword "初级滑雪"
```

**Output emphasis:** Beginner-friendly resorts.

---

## Playbook C: Pro Ski

**Trigger:** "advanced slopes"

```bash
flyai search-poi --city-name "{city}" --category "滑雪" --poi-level 5
```

**Output emphasis:** Top-rated ski resorts.

---

