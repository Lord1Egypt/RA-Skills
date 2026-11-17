---
name: whmcs-invoice-only-safety
description: "Use when building or reviewing an authorized WHMCS invoice-only order adapter that creates an unpaid invoice and never takes payment. Covers pinned-product preconditions, login/cart verification, checkout field discipline, single-submit semantics, and post-submit invoice validation. Use when creating a WHMCS order that stops at an unpaid invoice, or auditing automation for accidental payment."
version: 0.1.0
license: MIT-0
platforms: [linux]
metadata:
  openclaw:
    tags: [whmcs, ordering, safety, invoicing]
  hermes:
    tags: [whmcs, ordering, safety, testing]
    related_skills: [test-driven-development]
---
# WHMCS invoice-only order safety

**Overview (EN).** Guardrails for WHMCS/Lagom order automation that must stop at
an **unpaid invoice** and never move money. Covers pinned-product preconditions,
positive login verification, scoped cart checks, checkout field discipline,
single-submit semantics under durable state, and post-submit invoice validation.
Written for authorized ordering only; creating an unpaid invoice is the intended
terminal state. Applies to any agent that can drive HTTP forms (Hermes, OpenClaw,
Claude Code, or a plain script).

## When to use
Implement or review authorized WHMCS/Lagom automation that creates an unpaid invoice, never a payment. This does not authorize purchases, product changes, or final submissions by itself.

## Procedure
1. Pin product ID, name, quantity, currency, monthly amount, and permitted side effects before writing code. Reject unknown form layouts and unsupported mandatory configurable options.
2. Load `test-driven-development`; write and run failing synthetic boundary tests before implementing each behavior. Place pytest temporary files under the configured scratch directory, not the system temporary directory.
3. Positively verify login using a same-origin authenticated logout/account marker. Missing login forms alone are not evidence. Validate HTTPS origin and endpoint before every request and redirect; never replay a POST after 307/308, and disable HTTP retries.
4. Prove the preexisting cart is empty using a visible, scoped empty-cart marker inside the cart container — not a phrase found anywhere in the document. Ignore hidden/template markers. Never clear another cart.
5. Serialize successful controls with hidden tokens and duplicate names intact; omit unchecked/disabled controls. Handle select defaults and disabled optgroups. Explicitly choose the authorized monthly option and verify its currency and price.
6. Generate root passwords with cryptographic randomness, upper/lower/digit/symbol categories, and the intersection of the site's length bounds with authorized minimum strength. Fail closed when bounds are unsupported. Save only the designated dotenv key before configuration, under a stable sidecar lock shared by cooperating env writers; do not serialize the entire environment or log passwords.
7. Re-read checkout immediately before submission. Verify one product, quantity one, item price, total, recurring price, no addons, no promotion. Set existing-customer mode, accept terms, explicitly disable both applycredit and usecredit, and prohibit card storage. Select only an actually offered, approved manual gateway; reject automatic/card/credit/debit choices and labels.
8. Require caller-owned durable in-progress state and process locking before checkout. Submit at most once. Do not follow external/payment redirects. Derive exactly one invoice ID from the response; GET the canonical invoice URL and verify the exact invoice ID, unpaid status, product, amount, currency, and monthly cycle when shown.
9. After any final-POST ambiguity, return a fixed sanitized terminal error and forbid retry. A genuine sold-out result before submission may be handled separately; login, WAF, and parsing failures are not sold-out evidence.

## Pitfalls
- Currency suffixes may be adjacent (`¥138.00CNY`). Strip only validated currency markers before parsing Decimal amounts; reject signed negative prices, malformed grouping, and ambiguous currencies.
- Lagom empty carts may redirect `a=view` to `a=checkout` and lack `frmCheckout`. One observed Lagom store used `.message-no-data .message-title` with the text `您的购物车目前为空` ("your cart is currently empty"); re-verify the selector per theme instead of treating it as a constant.
- Public Lagom `order.min.js` confirms configuration uses `ajax=1&a=confproduct` plus serialized `frmConfigureProduct`; an empty response or explicit boolean `status:true` may mean success. Reject other response bodies without echoing them.
- Advisory dotenv locks cannot protect against unrelated editors that ignore the lock. Document this rather than claiming universal concurrent-write safety.

## Verification
Run synthetic fixture tests covering guards, unsafe gateways, credits, redirect leaks, stale tokens, invoice false success, and timeout non-retry behavior. For live login/sold-out probes, block all POSTs except login and replace password persistence with a hard refusal: a stock change must not silently turn a read-only probe into configuration, env writes, or checkout. Report separately what was verified live and what remains synthetic, and never present a test invoice as a real order.

## License and provenance
Original prose, no third-party code. Released under MIT-0, the license ClawHub
applies to every published skill; `license:` is stated here so the file is also
correct when read straight from a git repository.
