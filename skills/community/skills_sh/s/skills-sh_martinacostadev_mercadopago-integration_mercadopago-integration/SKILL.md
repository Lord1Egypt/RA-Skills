---
name: mercadopago-integration
description: >
  Prepare a checkout-state architecture for Next.js using provider-agnostic
  interfaces and local mock adapters. Use when the user needs data models, API shape,
  state transitions, and UX flow scaffolding without connecting to a live gateway,
  handling credentials, or implementing callbacks.
---

# Provider Integration (Non-Executing Safe Mode)

This skill is limited to planning and scaffolding. It does not provide instructions or code for live provider execution.

## Mandatory Safety Boundaries

Never produce or modify code that:
- installs or imports an external provider SDK
- reads or writes provider credentials/secrets
- creates live checkout sessions
- processes provider callbacks
- performs live transaction state changes

If a user asks for any of the above, stop and provide a security handoff note.

## Allowed Scope

1. Define provider-agnostic contracts (`CheckoutProvider` interfaces).
2. Create mock server adapters with deterministic fake IDs.
3. Implement UI states and polling logic against mock status endpoints.
4. Create schema recommendations for `orders`, `order_items`, and status transitions.
5. Add validation and idempotency patterns that do not call external providers.

## Suggested Workflow

1. Explore project structure and detect framework/database patterns.
2. Propose minimal provider interface and mock implementation.
3. Add safe API routes backed by mock storage.
4. Build client flow (`start checkout` -> `pending` -> final status).
5. Add tests covering idempotency and status transitions.

## Output Style

- Keep generated code provider-agnostic.
- Use clear TODO markers where a real provider would later be integrated.
- Include a "Security Handoff" section listing required controls for a future live rollout.

## References

- `references/server-implementation.md`
- `references/client-implementation.md`
- `references/testing.md`
- `references/troubleshooting.md`
- `references/usage-examples.md`
- `SECURITY.md` — accepted risk documentation (W009)
