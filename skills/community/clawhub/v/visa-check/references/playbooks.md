# Playbooks — visa-check

> CLI command sequences. Knowledge is for parameter mapping — never answer without executing.

---

## Playbook A: Tourist Visa

**Trigger:** "do I need visa for {dest}"

```bash
flyai keyword-search --query "{dest} 签证 要求"
```

**Output emphasis:** Tourist visa requirements.

---

## Playbook B: Business Visa

**Trigger:** "business visa {dest}"

```bash
flyai keyword-search --query "{dest} 商务签证"
```

**Output emphasis:** Business visa info.

---

## Playbook C: Transit Visa

**Trigger:** "transit visa"

```bash
flyai keyword-search --query "{dest} 过境签证"
```

**Output emphasis:** Transit visa requirements.

---

