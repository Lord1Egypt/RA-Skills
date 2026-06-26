# Playbooks — refundable-hotel

> CLI command sequences. Knowledge is for parameter mapping — never answer without executing.

---

## Playbook A: Free Cancel

**Trigger:** "free cancellation", "免费取消"

```bash
flyai search-hotel --dest-name "{city}" --key-words "免费取消" --sort rate_desc --check-in-date {in} --check-out-date {out}
```

**Output emphasis:** Hotels with free cancellation.

---

## Playbook B: Free Cancel + Budget

**Trigger:** "cheap free cancel"

```bash
flyai search-hotel --dest-name "{city}" --key-words "免费取消" --sort price_asc --check-in-date {in} --check-out-date {out}
```

**Output emphasis:** Cheapest with free cancellation.

---

