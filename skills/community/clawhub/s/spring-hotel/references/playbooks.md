# Playbooks — onsen-hotel

> CLI command sequences. Knowledge is for parameter mapping — never answer without executing.

---

## Playbook A: Hot Spring + Hotel

**Trigger:** "温泉酒店"

```bash
flyai search-poi --city-name "{city}" --category "温泉"
flyai search-hotel --dest-name "{city}" --key-words "温泉" --sort rate_desc --check-in-date {in} --check-out-date {out}
```

**Output emphasis:** Find hot springs → nearby hotels with onsen.

---

## Playbook B: Private Hot Spring

**Trigger:** "私汤"

```bash
flyai search-hotel --dest-name "{city}" --key-words "私汤" --sort rate_desc --check-in-date {in} --check-out-date {out}
```

**Output emphasis:** Hotels with in-room private hot spring.

---

## Playbook C: Hot Spring Resort Package

**Trigger:** "温泉度假"

```bash
flyai search-hotel --dest-name "{city}" --key-words "温泉度假" --sort rate_desc --check-in-date {in} --check-out-date {out}
```

**Output emphasis:** Full resort experience with hot spring.

---

