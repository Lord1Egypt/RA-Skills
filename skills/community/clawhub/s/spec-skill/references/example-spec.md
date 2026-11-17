# A worked spec, end to end

One small tier-3 change, written out in full, so the shapes are copyable rather
than described. Read this when you are unsure what a criterion, a task, or a
receipt should actually look like. It is deliberately short: two requirements,
four tasks. A real money-path spec would be longer, not differently shaped.

The change: a refund-locked resource currently falls through to the generic
upgrade empty state, which reads as "upgrade to see this" to someone who was
refunded. It should say plainly that access ended with the refund.

Tier 3, because it touches the access-control path and the refund gate. Both are
money adjacent and a mistake is visible to a paying customer.

File paths below are invented. Copy the shapes, not the names.

---

## `requirements.md`

```markdown
# Refund-locked resources get their own empty state

## Overview

A refunded resource is locked by `access.ts`'s refund gate, which runs before
the plan gate. Today the client receives the same empty-state shape as a free
user, so the UI offers an upgrade path that will not restore access. This spec
gives the refunded case its own reason code and its own empty state.

## User roles

- **Refunded owner**: bought the resource, was refunded, still has the URL.
- **Free-plan owner**: never paid, sees the upgrade empty state. Must be
  unaffected.

## Requirements

### Requirement 1: the server states why access ended

**User story:** As a refunded owner, I want the page to tell me access ended
with my refund, so that I stop trying to unlock what I no longer own.

**Acceptance criteria:**

1.1 WHEN a resource's owning order is refunded THE SYSTEM SHALL return
`lockReason: 'refunded'` alongside the empty-state payload.
1.2 IF a resource is both refunded and below the required plan THEN THE SYSTEM
SHALL return `lockReason: 'refunded'`, because the refund is the earlier and
more specific gate.
1.3 WHEN a resource is not refunded THE SYSTEM SHALL omit `lockReason` entirely
rather than sending a null, so no client branch changes shape.

### Requirement 2: the client says it once, plainly

**User story:** As a refunded owner, I want one clear sentence instead of an
upgrade prompt, so that the page is not misleading.

**Acceptance criteria:**

2.1 WHEN `lockReason` is `refunded` THE SYSTEM SHALL render the refunded empty
state and SHALL NOT render any checkout or upgrade control.

## Non-regression

- WHEN a resource is locked by plan alone THE SYSTEM SHALL CONTINUE TO return the
  existing empty-state payload byte for byte.
  Proven by: `src/api/__tests__/access.test.ts`
- WHEN a share link is opened for a refunded resource THE SYSTEM SHALL CONTINUE
  TO refuse it at the refund gate, before the plan gate.
  Proven by: `src/api/__tests__/share.test.ts`

## Out of scope

- Any change to refund attribution or which resources a refund locks.
- Email or in-app notification of the refund.

## Open questions

None. The one that existed (whether to reuse `trimReason`) is settled in the
ledger as decision `lock-reason-field`.
```

Note the shapes the validator depends on: criteria are `N.M` at the start of a
line, and every `SHALL CONTINUE TO` carries a `Proven by:` naming a real test.

---

## `design.md`

```markdown
# Design: refund-locked empty state

## Overview

Both gates already exist and already run in the right order. This is a labelling
change, not a gating change: the refund gate gains one field on its response and
the client gains one branch. Requirement 1.2 is satisfied for free by the
existing order (access → expiry → refund → plan), which is why this spec adds
no ordering logic.

## Components

- `src/api/access.ts`: the refund gate adds `lockReason: 'refunded'` to the
  empty-state payload it already returns.
- `src/api/empty-state.ts`: untouched. The field is added by the caller, so the
  shared empty-state shape stays identical for the plan-only path, which is what
  makes the first non-regression assertion cheap to keep true.
- `src/components/LockedPanel.tsx`: one branch on `lockReason`.

## Data

`lockReason?: 'refunded'`. Optional, absent rather than null when it does not
apply (criterion 1.3), and a string union rather than a boolean so a later gate
can add its own value without another field.

### Decision: add a field rather than reuse `trimReason`

**Context:** `trimReason` already exists on the payload and describes why
sections were trimmed.
**Options:** 1. reuse it (no schema change, but conflates "trimmed" with
"revoked", and the share path already reads it) 2. new optional field (one more
key, no existing reader affected).
**Decision:** new optional field.
**Rationale:** `trimReason` is read by `GET /api/share`, so widening its
meaning would change a second public door onto the same data. Not worth it to
save a key.

## Error handling

The refund lookup already fails closed to locked. Unchanged: a spec that touches
money should not also change what happens when the lookup fails.

## Testing

Unit tests for both gates and for the absent-field case. No new e2e: the visual
change is one paragraph and the existing locked-route smoke already covers the
page rendering at all.

## Co-artifacts

`docs/access-gates.md` documents the gate order and the empty-state shape, so it
gains the new field. This is an API change: merging does not ship it. Name the
production apply step from the project overlay, and show the user the diff
before applying because it is on the access-control path.
```

---

## `tasks.md`

```markdown
# Tasks: refund-locked empty state

Foundation first: the server field lands and is proven before the client reads it,
so a half-deployed state degrades to today's behaviour rather than a blank panel.

- [ ] 1. Server
- [ ] 1.1 Add `lockReason: 'refunded'` at the refund gate in `access.ts`, and
      assert the plan-only path is unchanged.
  - Files: `src/api/access.ts`
  - Verify: `npm run test` covers the two new cases plus the byte-identical
    plan-only payload
  - _Requirements: 1.1, 1.2_
- [ ] 1.2 Assert the field is absent, not null, when no refund applies.
  - Files: `src/api/__tests__/access.test.ts`
  - Verify: `npm run test`
  - _Requirements: 1.3_
- [ ] 2. Client
- [ ] 2.1 Branch the locked panel on `lockReason` and drop the checkout control
      in the refunded case.
  - Files: `src/components/LockedPanel.tsx`
  - Verify: `npm run test` renders the locked route without a checkout button present
  - _Requirements: 2.1_
- [ ] 3. Co-artifacts
- [ ] 3.1 Document the field and the gate order it depends on.
  - Files: `docs/access-gates.md`
  - Verify: `npm run test`
  - _Requirements: enabler_
```

`3.1` is an `enabler`: it implements no user-visible criterion, and inventing a
citation for it would make the coverage count lie. `1.` `2.` `3.` are bare
parents carrying no work, so they need neither a `Verify:` nor a citation.

---

## `.spec-state.json`

After requirements were approved and design is out for review:

```json
{
  "type": "feature",
  "tier": 3,
  "approved": [
    {
      "file": "requirements.md",
      "sha256": "3d1f8c0a94b7e6521d0c8fa47b39e5c2118d6a0fbb4c9d7e2a5f83016c4b7d9e",
      "at": "2026-08-22T14:10:00Z"
    }
  ],
  "decisions": [
    {
      "id": "lock-reason-field",
      "title": "Reuse trimReason or add a field",
      "options": ["reuse trimReason", "new optional lockReason"],
      "recommended": "new optional lockReason",
      "answer": "new optional lockReason",
      "why": "trimReason is read by /api/share; widening it changes a second public door."
    }
  ],
  "blocking": "Waiting on review of design.md.",
  "context": { "template": "src/api/access.ts" }
}
```

No `closure` yet, because nothing has shipped. When it does, it moves
`implemented` → `merged` → `deployed` (only after the overlay's production apply
step) → `verified`, and only then does the dir get its `> Archived` headers.

---

## Checking it

```bash
node <this-skill-dir>/scripts/check-spec.mjs docs/plans/2026-08-22-refund-locked-empty-state
```

The `sha256` above is illustrative. Compute the real one with `shasum -a 256`, or
the validator will correctly call the receipt void.
