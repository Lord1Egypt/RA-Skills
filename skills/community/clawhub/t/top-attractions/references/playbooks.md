# Playbooks — top-attractions

> CLI command sequences. Knowledge is for parameter mapping — never answer without executing.

---

## Playbook A: Top Rated

**Trigger:** "what to see", "有什么好玩的"

```bash
flyai search-poi --city-name "{city}" --poi-level 5
```

**Output emphasis:** Show top 5 by rating.

---

## Playbook B: By Category

**Trigger:** "museums in Beijing"

```bash
flyai search-poi --city-name "{city}" --category "{cat}"
```

**Output emphasis:** Category-filtered top attractions.

---

## Playbook C: For Kids

**Trigger:** "kid-friendly attractions"

```bash
flyai search-poi --city-name "{city}" --category "主题乐园"
flyai search-poi --city-name "{city}" --category "动物园"
```

**Output emphasis:** Family-oriented attractions.

---

