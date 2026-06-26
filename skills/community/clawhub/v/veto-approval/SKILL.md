---
name: Veto Approval
description: Pause your agent for human approval before high-risk actions.
parameters:
  action_title: string (e.g. "Delete user database")
  user_email: string (The approver's email)
  context: string (Optional context for the email)
---

# Veto Approval Skill

This skill allows your agent to send a 1-click approval email to you before proceeding with sensitive tasks.

## Setup
1. Get your API Key at [vetoapi.com](https://vetoapi.com)
2. Add `VETO_API_KEY` to your environment.

## Usage

```python
from veto_skill import ask_human_permission

approved = ask_human_permission(
    action_title="Send invoice for $5,000 to Client X",
    user_email="boss@company.com",
    context="Monthly retainer — Q1 2026"
)

if approved:
    send_invoice()
else:
    print("Action blocked by human.")
```

## How it works

1. Your agent calls `ask_human_permission()`
2. An approval email with **Approve** and **Reject** buttons is sent to `user_email`
3. The function blocks until a decision is made (polls every 5 seconds)
4. Returns `True` if approved, `False` if rejected
