# Controlled-Domain List (optional config, default empty)

> ⚠️ **This file is the config for D2-E1. The generic version ships with an empty list → D2-E1 passes ✅ by default.**
>
> Only when your team has internal services that **must** go through an SDK/CLI
> facade (and must NOT be hit via raw HTTP), register those domains in the
> "Controlled domains" table below. Once registered, D2-E1 / D2-W2 take effect
> for them automatically.

---

## Controlled domains (empty by default — fill in as needed)

> Add a row to the table to enable. Matching is fuzzy (substring match); subdomains also match.

| Domain (substring match) | Purpose | Why controlled | Required access method |
|----------------|---------|---------|----------------|
| _(example, not enabled)_ `api.internal.example.com` | Internal core service | Direct calls bypass auth/audit | Team SDK / CLI facade |

> Default state: no real enabled rows in the table → D2-E1 does not fire; all HTTP/browser calls are handled by D2-W2 (WARN-level hardcoded-URL review).

---

## How controlled domains apply across rules

| Rule | Trigger condition | Level |
|------|---------|------|
| **D2-E1** No raw HTTP/browser bypass of sensitive/controlled domains | Code makes an HTTP call or uses browser/web_fetch + a registered controlled domain | **ERR** |
| **D2-W2** Hardcoded-URL review | Controlled domains go to D2-E1; other internal/external domains → WARN | — |

---

## Adding a controlled domain

1. Add a new row to the "Controlled domains" table above (domain + purpose + why controlled + required access method)
2. Submit for review; confirm together with the relevant business owner
3. After merge, D2-E1 / D2-W2 apply the new list automatically — **no need to edit check-rules.md**

> Removing a controlled domain works the same way; evaluate the impact first (it may turn historical ERRs into WARNs, affecting the pass/fail decision).
