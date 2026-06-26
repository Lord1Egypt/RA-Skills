---
name: settle-agent-invoice
description: Agent settles an invoice at the end of a multi-step task using CAI transfer after user confirms payee and amount. Includes resolve_transfer_recipient and transfer_status proof. Powered by CAI.com. Canonical skill v1.0.15.
metadata:
  version: 1.0.15
---

# Settle an agent invoice with CAI

Long-running agents often end with **"pay this invoice"** — vendor email, PDF, or on-chain address. This skill frames that **closing payment** as a standard CAI flow: balance check → confirm → transfer → proof.

## When to Use

- "Settle the invoice my agent prepared"
- "Pay the bill at the end of this task"
- "Send payment to the address on the invoice"
- "Complete payment and show me proof"

## Task flow (agent-native)

1. Agent extracts invoice: payee, amount, asset, chain (or asks user to clarify).
2. `wallet_balances`.
3. User confirms irreversible transfer details.
4. `resolve_transfer_recipient` for @cai.com payees, else `to_address`.
5. `transfer` after explicit yes.
6. `transfer_status` + `wallet_activity_list`; optional mail summarize for receipt.

## Quick Setup

```bash
openclaw secrets set CAI_API_KEY "your_dashboard_api_key"
```

## Canonical Reference

- https://cai.com/skill.md
- https://cai.com/skill-references/agent-payment-workflow.md
- https://cai.com/developers.html
