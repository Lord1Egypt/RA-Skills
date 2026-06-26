# Playbooks — travel-insurance

> CLI command sequences. Knowledge is for parameter mapping — never answer without executing.

---

## Playbook A: Basic Insurance

**Trigger:** "travel insurance"

```bash
flyai keyword-search --query "旅行保险 {dest}"
```

**Output emphasis:** Standard travel insurance plans.

---

## Playbook B: Medical Coverage

**Trigger:** "medical insurance abroad"

```bash
flyai keyword-search --query "境外医疗保险 {dest}"
```

**Output emphasis:** Medical-focused coverage.

---

## Playbook C: Premium Insurance

**Trigger:** "comprehensive travel insurance"

```bash
flyai keyword-search --query "全面旅行保险 {dest}"
```

**Output emphasis:** Comprehensive coverage plans.

---

