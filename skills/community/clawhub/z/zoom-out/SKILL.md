---
name: zoom-out
description: Tell the agent to zoom out and give broader context or a higher-level perspective on a section of code. Use when you're unfamiliar with a code area or need to understand how it fits into the bigger picture.
author: GenorTG
attribution: Adapted from the GSD Core project by TÂCHES / open-gsd (https://github.com/open-gsd/gsd-core)
---

# Zoom Out

When you're deep in unfamiliar code, zoom out to see the architecture before diving deeper.

## When to Use

Trigger this when:
- You're dropped into an unfamiliar codebase or module
- You need to understand how a piece fits into the bigger picture
- You've been reading low-level code and lost the thread of what it's for
- You need a map before making changes

## What It Does

The agent stops reading individual functions/files and instead:
1. Maps the module's boundary — what it exposes and what it depends on
2. Lists all callers of the module's public API
3. Identifies the module's role in the broader architecture (layer, service, utility, etc.)
4. Uses the project's own domain vocabulary rather than generic terms
5. Returns a compressed but complete picture of what this area does and how it connects

## Example Output Shape

```
## Module: `src/payments/processor.ts`

**Role:** Payment orchestration layer between API routes and external gateways

**Public API:**
- `processPayment(orderId, amount, method)` — called by CheckoutController
- `refundPayment(transactionId, reason)` — called by AdminController
- `getPaymentStatus(orderId)` — called by three route handlers

**Dependencies:**
- Stripe SDK (external gateway)
- `src/db/transactions.ts` — stores payment records
- `src/notifications/email.ts` — sends receipts

**Callers:**
- CheckoutController (create flow)
- AdminController (refund flow)
- OrderStatus display component (read-only)
```

## Anti-patterns

- Don't zoom out when the question is about a specific bug — that needs diagnose, not zoom-out
- Don't zoom out repeatedly in the same session — one map is enough
- Don't use zoom-out for language/framework basics — those need docs, not architecture
