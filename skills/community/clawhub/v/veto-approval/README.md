# VetoAPI Skill for OpenClaw

Stop your AI agent from taking risky actions without human approval. Get an email to approve or reject on the fly — your agent waits and proceeds only when you say yes.

## Installation

```bash
pip install requests python-dotenv
```

Get your free API key at [vetoapi.com](https://vetoapi.com), then add it to your `.env`:

```env
VETO_API_KEY=veto_live_xxxxxxxxxxxx
```

## Usage

### As a Python module

```python
from veto_skill import ask_human_permission

# Your agent pauses here until a human approves or rejects via email
approved = ask_human_permission(
    action_title="Send invoice for $5,000 to Client X",
    user_email="boss@company.com",
    context="Monthly retainer payment — Q1 2026"
)

if approved:
    send_invoice()
else:
    print("Action blocked by human.")
```

### From the command line

```bash
python veto_skill.py "Delete production database" "admin@company.com" "Scheduled cleanup"
```

## How it works

1. Your agent calls `ask_human_permission()`
2. VetoAPI sends an approval email with **Approve** and **Reject** buttons
3. The function blocks (polls every 5 seconds) until a decision is made
4. Returns `True` if approved, `False` if rejected

## Environment variables

| Variable | Required | Description |
|----------|----------|-------------|
| `VETO_API_KEY` | Yes | Your VetoAPI key from vetoapi.com |

## Links

- [Get API Key](https://vetoapi.com/get-key)
- [API Reference](https://vetoapi.com/docs)
- [vetoapi.com](https://vetoapi.com)
