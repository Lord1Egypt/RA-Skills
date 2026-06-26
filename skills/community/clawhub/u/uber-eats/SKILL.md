---
name: Uber Eats
slug: uber-eats
version: 1.0.0
homepage: https://clawic.com/skills/uber-eats
description: Navigate Uber Eats in a live browser or app handoff to compare merchants, manage carts, and reach checkout safely.
changelog: Initial release with live-session ordering flow, access-denied fallback, checkout guardrails, and issue recovery for Uber Eats orders.
metadata: {"clawdbot":{"emoji":"🍔","requires":{"bins":[],"config":["~/uber-eats/"]},"os":["darwin","linux","win32"],"configPaths":["~/uber-eats/"]}}
---

## When to Use

User needs Uber Eats specifically, not generic delivery advice. Use this when the task depends on the user's real Uber Eats session, saved addresses, live merchant availability, promo state, cart contents, grocery or convenience ordering, or post-order troubleshooting inside Uber Eats.

Choose this skill when the next step is to browse merchants, compare ETAs and fees, prepare a cart, verify checkout details, or recover from Uber Eats-specific problems such as address mistakes, cancellation windows, missing items, or web-session access failures. If the task is platform-agnostic, route to `food-delivery`.

## Architecture

Memory lives in `~/uber-eats/`. If `~/uber-eats/` does not exist, run `setup.md`. See `memory-template.md` for structure and starter fields.

```text
~/uber-eats/
|-- memory.md       # Activation defaults, session mode, and ordering boundary
|-- addresses.md    # Approved delivery addresses and zone caveats
|-- merchants.md    # Preferred merchants, cuisine notes, and fee patterns
|-- orders.md       # Recent orders, substitutions, and issue history
`-- incidents.md    # Access failures, payment issues, refunds, and support outcomes
```

## Quick Reference

Load only the smallest file needed for the current blocker.

| Topic | File |
|-------|------|
| Setup guide | `setup.md` |
| Memory template | `memory-template.md` |
| Live browser and app-handoff flow | `browser-flow.md` |
| Checkout safety and confirmation rules | `checkout-guardrails.md` |
| Web blocking and access-denied fallbacks | `access-fallbacks.md` |
| Failure patterns and recovery order | `issue-recovery.md` |

## Requirements

- A browser or app session where the user can access Uber Eats is strongly preferred.
- Any browser reading, clicking, typing, or screenshot capture must use a host-provided browser automation path that the user has already approved in the current environment.
- Saved addresses, payment methods, and account credentials should stay inside the user's own Uber Eats browser session or app.
- Explicit approval is required before controlling the user's daily browser session, changing delivery details, editing a non-empty cart, or placing any live order.
- If the skill activates without explicit current-thread approval for browser control, stay in planning mode and do not inspect the live session.

If Uber Eats web access is blocked or the browser shows `access denied`, stay calm and switch to a fallback path instead of pretending the session is usable.

## Control Modes

This skill supports four levels of intervention:

- **Browse mode**: inspect address, merchant cards, ETAs, fees, promos, and categories without changing cart state.
- **Draft cart mode**: open a merchant and prepare a candidate cart when the user clearly asked for an order draft.
- **Live checkout mode**: review payment, tip, notes, and total before placing the order.
- **Fallback mode**: when web access fails, use a locale route, app handoff, or manual support path instead of brittle blind automation.

Do not blur the boundary between browsing and ordering. A live Uber Eats session has real addresses, real payment methods, and real purchase consequences.

## Data Storage

Persistent local notes in `~/uber-eats/` are optional. If the user does not want local storage, operate statelessly and do not create or write that folder.

When local notes are allowed, keep only durable operating context in `~/uber-eats/`:
- whether the skill may reuse the daily browser profile or should stay read-only
- preferred addresses, neighborhoods, and delivery caveats approved by the user
- favorite merchants, reorder patterns, and substitution preferences
- issue history worth reusing, such as access-denied loops, weak promos, or frequent cancellation friction

Do not store account passwords, payment card data, one-time verification codes, or full receipts with sensitive payment details.

## Core Rules

### 1. Reuse the Real Session Only When the User Actually Wants That
- Prefer the user's already signed-in Uber Eats browser session when live state matters.
- This skill does not grant browser access by itself; it only uses an already-approved browser control path from the host environment.
- Ask before activating, switching tabs, typing, clicking, or capturing screenshots from the daily browsing profile.
- If the user only wants strategy, stay out of the real session and explain the flow instead.

### 2. Lock the Delivery Address Before Comparing Merchants
- Uber Eats ordering starts with sign-in plus a delivery address.
- Merchant availability, ETA, fees, and promos depend on the active address.
- If the address is missing or ambiguous, solve that first before treating merchant cards as meaningful.

### 3. Read the Merchant and Cart State Before Touching Checkout
- Confirm merchant name, ETA, delivery fee, service fee, promo state, and cart contents before adding or editing items.
- Re-read the page after every navigation or major action.
- If the cart already contains items, stop and clarify whether to preserve, edit, or replace it.

### 4. Separate Drafting From Live Purchase
- Building a candidate cart is not the same as placing an order.
- Before any live checkout step, summarize the merchant, items, substitutions, address, ETA, fees, total, tip, payment method, and delivery notes.
- Place the final order only after explicit approval in the current thread.

### 5. Treat Address and Cancellation as High-Risk Boundaries
- Official Uber Eats help says the order flow requires a confirmed delivery address before checkout.
- After an order is placed, address changes are unreliable and often require contacting support or the delivery partner; do not depend on them.
- Cancellation may be possible only before the merchant accepts the order or before dispatch; refund eligibility can disappear quickly.

### 6. Prepare a Fallback When the Web Session Misbehaves
- If the browser shows `access denied`, a blank screen, or another blocking page, do not keep clicking blindly.
- Try a supported locale route or app handoff first.
- If the session is still blocked, switch to manual guidance or support recovery instead of claiming the order can proceed.

### 7. Keep Memory About Preferences, Not Secrets
- Save reusable address choices, favorite merchants, cuisine habits, substitution preferences, and known problem merchants.
- Keep short notes about what worked, what arrived late, and what needed support.
- Never store full payment data, raw support transcripts, or copied personal verification details.

## Uber Eats Traps

- Treating the home page as actionable before an address is set -> merchant availability and fees are unreliable.
- Ignoring a web `access denied` or anti-bot page -> brittle automation and false progress.
- Modifying a non-empty cart without checking whether it contains unfinished items -> accidental cart damage.
- Assuming the subtotal is the real price -> delivery fee, service fee, and tip can reverse the decision.
- Assuming the delivery address can be safely changed after ordering -> support may cancel or charge anyway.
- Treating cancellation as guaranteed -> refund eligibility can disappear after merchant acceptance or dispatch.

## External Endpoints

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| https://www.ubereats.com | Addresses, search terms, cart state, checkout data, and account session cookies inside the user's own browser session | Browsing, cart preparation, checkout, and issue handling |
| Uber Eats app deep links or app continuation opened by the user | Merchant, cart, and checkout intent data | Native app continuation when browser flow is blocked or incomplete |
| https://help.uber.com/ubereats | Support requests, issue details, and help navigation opened by the user | Recovery, cancellation, address, and troubleshooting guidance |

No other data should be sent externally unless the user explicitly opens additional payment, map, or support surfaces during the Uber Eats workflow.

## Security & Privacy

**Data that leaves your machine:**
- addresses and search terms entered into Uber Eats
- cart and checkout data sent through the user's Uber Eats session
- support or issue details the user explicitly submits to Uber Eats

**Data that stays local:**
- optional Uber Eats operating notes in `~/uber-eats/`, only if the user wants persistent memory
- preferences, address labels, and known-good merchant patterns approved by the user

**This skill does NOT:**
- ask for Uber or Uber Eats passwords in chat
- store payment card numbers or one-time verification codes
- place live orders without explicit confirmation in the current thread
- claim a cart, address, or cancellation path is safe without re-reading the actual Uber Eats page

## Trust

By using this skill, data is sent to Uber Eats through the user's own browser or app session.
Only install and run it if you trust Uber Eats with your address, cart, payment, and order data.

## Scope

This skill ONLY:
- helps control Uber Eats ordering safely through a live browser or app handoff
- structures browse, draft-cart, live-checkout, fallback, and issue-recovery workflows
- keeps durable notes for addresses, merchants, preferences, and recurring issues

This skill NEVER:
- claim a live Uber Eats state it cannot verify
- promise merchant availability, ETA, promo validity, or cancellation success without checking the current page
- store secrets or raw payment data in its own memory files
- modify its own skill files

## Related Skills
Install with `clawhub install <slug>` if user confirms:

- `food-delivery` - Broader ordering logic when the user is not locked to Uber Eats.
- `maps` - Validate delivery geography, area fit, and route realism around the chosen address.
- `safari` - Control the user's real Safari session when Uber Eats works better there.
- `applescript` - Build safer macOS browser-control snippets when the workflow needs exact Apple Events.
- `shopping` - Compare fees, promos, and real checkout value instead of rushing to place the order.

## Feedback

- If useful: `clawhub star uber-eats`
- Stay updated: `clawhub sync`
