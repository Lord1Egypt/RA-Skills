# Playbooks — zoo-aquarium

> CLI command sequences. Knowledge is for parameter mapping — never answer without executing.

---

## Playbook A: Zoos

**Trigger:** "zoo tickets"

```bash
flyai search-poi --city-name "{city}" --category "动物园"
```

**Output emphasis:** Zoos and wildlife parks.

---

## Playbook B: Aquariums

**Trigger:** "aquarium"

```bash
flyai search-poi --city-name "{city}" --category "海洋馆"
```

**Output emphasis:** Aquariums and ocean parks.

---

## Playbook C: Safari

**Trigger:** "safari park"

```bash
flyai search-poi --city-name "{city}" --keyword "野生动物园"
```

**Output emphasis:** Safari and drive-through parks.

---

