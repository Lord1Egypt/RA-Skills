---
name: Return Window Rescue Planner
description: Build an urgent return action sheet for items with deadlines, packing needs, proof, route order, and a final checklist.
version: "1.0.0"
type: prompt-flow
tags:
  - life-admin
  - returns
  - deadlines
  - logistics
  - shopping
author: Bell (design)
---

# Return Window Rescue Planner

## Overview

Return Window Rescue Planner helps a user triage items that need to be returned before their deadlines. It turns scattered return details into a practical action sheet with deadlines, proof needed, packing requirements, route order, and a final checklist.

The skill is designed for urgent admin and logistics. It reminds the user to verify current store policies and remove or cover personal data on shipping labels, packing slips, and receipts.

## When to Use

Use this skill when the user asks to:

- Organize items to return before deadlines
- Decide which returns to do first
- Plan a return route
- Prepare packages, receipts, labels, or QR codes
- Avoid missing a return window

**Trigger phrases:** "I need to return these before the deadline", "plan my returns", "return window is closing", "organize my returns", "what do I need to pack for returns".

## Inputs to Request

Ask the user for each item:

- Item name
- Store or seller
- Purchase date, delivery date, or return deadline
- Return method: mail, store drop-off, pickup, locker, carrier, or unknown
- Condition: unopened, opened, worn, defective, wrong item, damaged, or other
- Proof available: receipt, order number, email, app record, QR code, label, or packing slip
- Packing needs: box, bag, original packaging, tags, accessories, manual, charger, parts
- Refund target: original payment, store credit, replacement, exchange, or unknown
- Location of the item and packaging
- Any constraints, such as work hours, store hours known by the user, transport, or heavy items

If the deadline or policy is unclear, ask the user to verify it with the store or seller before relying on the plan.

## Workflow

### Step 1 - Capture Items

Create a return inventory with one row or bullet per item. Include the current status and missing information. Do not invent deadlines, policies, addresses, store hours, fees, or eligibility rules.

### Step 2 - Confirm Deadlines

Sort items by urgency:

- **Today or overdue risk:** action needed immediately
- **Next 1 to 3 days:** prepare now
- **This week:** schedule soon
- **Later:** batch if convenient
- **Unknown:** verify before planning

Remind the user that store policies can vary by item, condition, seller, holiday rules, membership status, and return method.

### Step 3 - Gather Proof

For each item, list proof needed:

- Receipt or invoice
- Order number
- Email confirmation
- App return QR code
- Printed label
- Packing slip
- Warranty or defect note
- Photos of damage if relevant

Mark missing proof as a blocker.

### Step 4 - Prepare Packing Needs

For each return, identify what needs to go in or on the package:

- Item
- Tags
- Accessories
- Cables or parts
- Manuals
- Original packaging if required
- Protective padding
- Printed label or QR code
- RMA or return authorization if provided

Add a privacy reminder: remove, cover, or shred personal data on old labels, packing slips, and receipts not needed for the return.

### Step 5 - Plan Route or Batch Order

Build a route order using only user-provided locations and constraints. Prioritize:

1. Earliest deadlines
2. Items with fixed appointments or pickup windows
3. Stores or carriers near each other
4. Heavy or bulky items when transport is available
5. Returns needing printing, packaging, or verification before leaving

If exact geography is unknown, provide a logical batch order rather than pretending to know the fastest route.

### Step 6 - Build the Action Sheet

Create a return action sheet with:

- Item list
- Deadline status
- Return method
- Proof needed
- Packing needs
- Blockers
- Route or batch order
- Final checklist

Make urgent items visually obvious.

### Step 7 - Final Checklist

End with a checklist the user can run before leaving or mailing:

- Verify policy and deadline
- Start return in store app or website if required
- Confirm refund or exchange target
- Gather proof
- Pack item and accessories
- Remove or cover personal data
- Attach label or save QR code
- Photograph package if useful
- Keep drop-off receipt or tracking
- Mark item done after refund is confirmed

## Output Template

```markdown
# Return Window Rescue Action Sheet

**Scope note:** Deadlines and policies must be verified with the store or seller before relying on this plan.

## 1. Deadline Triage
- **Today or overdue risk:** ...
- **Next 1 to 3 days:** ...
- **This week:** ...
- **Unknown deadline:** verify ...

## 2. Return Inventory
| Item | Store | Deadline | Method | Proof needed | Packing needs | Blocker | Priority |
|---|---|---|---|---|---|---|---|
| ... | ... | ... | ... | ... | ... | ... | ... |

## 3. Route or Batch Order
1. ...
2. ...
3. ...

## 4. Packing Station Checklist
- [ ] ...

## 5. Final Before-You-Go Checklist
- [ ] Verify each store policy and deadline.
- [ ] Remove or cover personal data on old labels and paperwork.
- [ ] Keep drop-off receipts or tracking numbers.
```

Avoid markdown tables if the delivery channel does not render them well; use bullets instead.

## Safety and Compliance

- Reminds the user to verify current store policies, deadlines, fees, and eligibility before acting
- Does not invent store policies, addresses, hours, return fees, refund guarantees, or eligibility rules
- Flags unknown deadlines and missing proof as blockers
- Reminds the user to remove, cover, or shred personal data on labels and paperwork
- Does not access accounts, emails, order histories, maps, files, or websites unless the user separately provides information
- Encourages keeping drop-off receipts and tracking numbers until refund or exchange is confirmed
- This is a prompt-only skill with zero code execution, zero network calls, and zero credential requirements

## Example Prompts

- "I have three items to return this week and the deadlines are tight. Help me plan my returns."
- "I bought clothes online that don't fit. Build a return action sheet before the 14-day window closes."
- "I need to return a defective blender to the store and two Amazon items by mail. Organize my return plan."

## Acceptance Criteria

1. The output captures each item with store, deadline, method, proof, and packing needs when provided.
2. Deadlines are triaged by urgency, with unknown deadlines marked for verification.
3. Store policy verification is explicitly recommended.
4. Missing proof, packaging, labels, or authorization details are marked as blockers.
5. Route order or batch order is based only on user-provided locations and constraints.
6. The final checklist includes personal data removal and receipt or tracking retention.
