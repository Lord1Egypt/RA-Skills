# 📘 ViBo Thread Memory — how to store conversations (guide)

## Your choice: store EVERYTHING or only the ESSENCE

ViBo can store your conversations with a bot/agent in two ways.
You choose once — and it works forever.

---

## 1️⃣ FULL mode — the whole conversation (default)

```
What is stored:   EVERY message (encrypted)
What goes to context: a compressed summary (for savings)
What you can do:  restore the FULL chain of events
                  ("what did we discuss 3 days ago?" — exact answer)
```

**For whom:** lawyers, managers, sales, support — anyone who must
remember every detail.

```bash
# Enable (choose once):
vibo dialog mode full

# Then just write:
vibo dialog add "client asked for a 10% discount"
vibo dialog add "agreed on price $120"
...
# A week later, ask:
vibo dialog ask "what did we agree on the price?"
→ "Agreed on $120, 10% discount if paid today"
```

---

## 2️⃣ SUMMARY mode — only the essence

```
What is stored:   key phrases, decisions, numbers (essence)
What goes to context: the same essence (maximum savings)
What is lost:     verbatim messages (the big picture remains)
```

**For whom:** anyone who wants maximum savings and privacy — the agent
remembers the ESSENCE, but stores nothing extra.

```bash
# Enable (choose once):
vibo dialog mode summary

# Write as usual:
vibo dialog add "discussed delivery options"
vibo dialog add "chose CDEK delivery, 500 RUB"
...
# Old messages are compressed into an essence automatically
# (by default: once more than 40 messages have accumulated)
```

---

## How to check the current mode

```bash
vibo dialog mode
→ Mode: full    (or summary)
```

## Switch at any time

```bash
vibo dialog mode full      # switch to the full archive
vibo dialog mode summary   # switch to the essence
```

The mode is saved in a `<name>.mode` file next to your dialog memory.

---

## Comparison

| | 1️⃣ FULL | 2️⃣ SUMMARY |
|---|---|---|
| Stores | every message | only the essence |
| Restoration | exact chain | big picture |
| Token savings | high (−72%) | maximum |
| Privacy | encryption | encryption + deletion |
| Ideal for | lawyers, managers, sales | savings, privacy |

---

## FAQ

**Can I switch without losing data?**
Switching full → summary compresses old messages into an essence.
Switching summary → full stores new messages in full.

**What if I want to delete the conversation entirely?**
Delete the dialog memory file (e.g. `thread.web`) — everything
inside is gone forever. ⚠️ **This is irreversible and cannot be undone — make a backup first** (copy the file elsewhere) if the history may contain anything you might need later.

**Is it safe?**
Everything is encrypted (AES-256-GCM). In summary mode secrets are
additionally removed after compression.

---

*ViBo — memory for AI agents. Questions: hello@wwwvibo.com · @ViBomemorybot*
