# Playbooks — travel-simcard

> CLI command sequences. Knowledge is for parameter mapping — never answer without executing.

---

## Playbook A: SIM Card

**Trigger:** "SIM card for {dest}"

```bash
flyai keyword-search --query "SIM卡 {dest}"
```

**Output emphasis:** Local SIM card options.

---

## Playbook B: eSIM

**Trigger:** "eSIM for travel"

```bash
flyai keyword-search --query "eSIM {dest}"
```

**Output emphasis:** Digital eSIM plans.

---

