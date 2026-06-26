# Automation Paths — Walmart

Choose the path that matches the real operating surface.

## Path 1: Consumer Browser Automation

Use this for ordinary Walmart.com grocery and household orders.

Preferred stable entry points:
- `Account -> Purchase History -> Reorder all`
- `My Items -> Reorder`
- order detail pages for edit, reschedule, and recovery
- `Chat with Shopper` or Live Shopper during active delivery shopping

Good browser-automation tasks:
- rebuild a prior order
- add or remove items from a draft basket
- set fulfillment mode to pickup, delivery, or shipping
- review substitution settings before checkout
- reschedule or recover an order inside Walmart's documented edit flows

Keep it user-mediated:
- refresh live price, stock, and time-slot state before apply
- require explicit confirmation before checkout or order mutation
- stop when login, MFA, or sensitive payment steps appear

## Path 2: Marketplace API Automation

Use this only for seller or solution-provider work.

What the official portal supports:
- items
- inventory
- orders
- pricing and promotions
- returns
- shipping and reports

This is not the same as consumer grocery automation. If the user wants to automate their own shopping account, do not route them into Marketplace APIs.

## Path 3: Text to Shop and App-Native Flows

Walmart also exposes user-facing flows like Text to Shop, app check-in, and live shopper messaging.

Use them as supported product features, not as undocumented APIs:
- help the user choose when they are the fastest path
- do not invent backend calls behind them
- treat them as account-native actions the user can confirm and review

## Practical Automation Order

1. Load household memory and decide basket mode.
2. Pick the safest entry path: reorder, my items, or fresh cart.
3. Build or adjust the basket.
4. Review substitutions and split-fulfillment risk.
5. Confirm timeslot and delivery mode.
6. Ask for explicit final confirmation before checkout.

## Hard Boundaries

- No credential capture in chat
- No hidden background ordering
- No pharmacy execution without explicit confirmation
- No claims of a public consumer Walmart API unless the user provides one
