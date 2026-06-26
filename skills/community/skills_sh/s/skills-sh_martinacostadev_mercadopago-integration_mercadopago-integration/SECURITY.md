# Security Policy

## Accepted Risks

### W009: Direct money access capability detected

**Status:** Accepted with mitigations
**Scanner:** Snyk
**Severity:** Medium (risk score 1.00)
**Date accepted:** 2026-03-09

#### Finding

Snyk classifies this skill as "Direct Financial Execution" because it provides
payment gateway integration architecture for MercadoPago.

#### Why we accept this risk

This skill is a **non-executing scaffolding tool**. It generates mock adapters
and provider-agnostic interfaces — it does not execute live transactions.

#### Mitigations in place

| Control | Detail |
|---------|--------|
| No SDK imports | No MercadoPago SDK or any payment provider SDK is imported or installed |
| No credentials | No secrets, API keys, or access tokens are read or written |
| No live calls | All adapters use deterministic mock IDs (`mock_${orderId}`) |
| No webhooks | No callback or notification handlers exist |
| No callback routes | SKILL.md explicitly forbids producing callback code |
| Mock-only mode | `CheckoutProvider` contract is satisfied by `MockCheckoutProvider` only |
| Safety boundaries | SKILL.md mandates a security handoff note if live execution is requested |
| Atomic DB updates | All database adapters use `WHERE status = ?` guards to prevent double-processing |
| SQL injection prevention | Raw PostgreSQL adapter uses column whitelist for dynamic updates |

#### What would change this assessment

If any of the following are introduced, this risk must be re-evaluated:

- Import of `mercadopago`, `@mercadopago/sdk-js`, or any payment SDK
- Environment variables for provider credentials (`MP_ACCESS_TOKEN`, etc.)
- Routes that call external payment APIs
- Webhook or callback handlers that process live notifications
- Code that creates real checkout sessions or preferences

#### Contact

Report security concerns via GitHub Issues on this repository.
