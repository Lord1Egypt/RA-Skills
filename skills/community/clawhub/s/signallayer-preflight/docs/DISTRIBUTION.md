# SignalLayer — distribution and commercial validation

This document distinguishes **technical discovery**, **wallet-capable buyers**, and **settled payments from independent customers**. A marketplace listing is not proof of revenue. It is maintained as a checklist, not an assertion of real-time availability.

Last editorial review: 2026-10-07. Do not treat unverified marketplace claims below as completed registrations.

## Free acquisition channels

| Channel | Evidence / actions | Next step |
| --- | --- | --- |
| [ClawHub](https://clawhub.ai/xavierleterrible-hub/skills/signallayer-preflight) | Skill v0.1.0 was publicly published and passed its platform scan. | Publish a new version when important GitHub SKILL.md changes have been reviewed; do not assume GitHub sync is automatic. |
| [GitHub](https://github.com/xavierleterrible-hub/signallayer-preflight) | Public Agent Skill source, read-only offer helper, CI. | Maintain accurate docs and installation examples. |
| [skills.sh](https://skills.sh/) | GitHub root SKILL.md is eligible for direct installation via the Skills CLI. Listing/ranking depends on real user installations. | Use `npx skills add xavierleterrible-hub/signallayer-preflight`; do not self-install repeatedly to inflate analytics. |
| [Official MCP Registry](https://registry.modelcontextprotocol.io/) | Published previously under `io.github.xavierleterrible-hub/signallayer`. | Verify version listed against live server version, update using official publisher if stale. |
| [Glama](https://glama.ai/) | Remote MCP server previously connected and indexed. | Verify public listing and individual tool availability. |
| [Smithery](https://smithery.ai/) | MCP server previously published and discoverable. | Verify public visibility and that tool schemas/annotations are up to date. |
| [x402scan](https://www.x402scan.com/) | HTTP x402 endpoints previously registered. | Verify exact resources/prices and latest crawl; do not conflate listing with settlements. |
| [x402dev](https://www.x402dev.com/) | Three HTTP tools previously recorded. | Recheck prices and status in directory. |
| [Agent402](https://agent402.tools/) | Seller previously listed in unproven tier. | Check if `agent_preflight` at $0.01 qualifies for unproven routing. Distinct external payers must develop naturally. |
| [Saylor Agent Bazaar](https://bazaar.saylorinnovations.com/) | Submission was blocked by provider's Cloudflare/D1 issue. | Follow upstream issue; retry only when provider confirms repair. |
| [MCP Market](https://mcpmarket.com/submit) | Supports a free review queue for GitHub-hosted Agent Skills. | A submitter email is required; use free queue, do not select paid placement. |
| [PulseMCP](https://www.pulsemcp.com/) | Check whether listing is ingested from official MCP Registry. | If absent, use their official manual submission process if available. |
| [x402 List](https://x402-list.com/api) | Supports reviewed endpoint submissions. | **Do not submit blindly**: some free-host / resubmission cases require a non-refundable $0.50–$1.50 USDC payment. Explicit approval first. |

## Ready-to-paste submission copy

**Agent Skill title:** SignalLayer Preflight

**Agent Skill repository:** https://github.com/xavierleterrible-hub/signallayer-preflight

**Remote MCP endpoint:** https://signallayer.floot.app/_api/mcp

**Description:** Check x402 payment terms and structural Base recipient signals before user-authorized API purchases. Free tool selection and evidence-aware $0.01 USDC Preflight on Base, with explicit uncertainty and no private-key collection.

**Tags (separate):** x402, payment-preflight, base, usdc, agent-security, mcp

**Categories:** Security, Development, Finance (use the actual marketplace taxonomy).

**Public homepage:** https://signallayer.floot.app

**Tool URLs:**
- `https://signallayer.floot.app/_api/v1/agent/preflight` ($0.01)
- `https://signallayer.floot.app/_api/v1/market/execution-intel` ($0.03)
- `https://signallayer.floot.app/_api/v1/web/structured-extract` ($0.02)

Pricing above is informational; the actual 402 requirement controls transaction terms, and buyer approval is mandatory.

## Conversion metrics to measure

1. **Installations** (ClawHub / skills.sh separately; counts are not necessarily unique users).
2. **Real discovery calls** (count by endpoint and source, distinguish bots/crawlers).
3. **Selected paid tool / HTTP 402** (not revenue).
4. **Verified and settled payments on Base** (transaction hashes, net receipts).
5. **Distinct external payers and repeat payers** (self-tests excluded).
6. **Variable cost per call and net contribution margin** (especially structured_extract).

Use this funnel to decide whether to iterate the product after 14 and 30 days. Do not create paid tests to manufacture marketplace trust or inflate demand.

## Verified external-discovery audit (2026-10-08 01:16 UTC)

A read-only GitHub Actions diagnostic, run **without calling Floot or SignalLayer**, confirmed:

- PayAI `GET /discovery/resources?limit=1`: HTTP 200, **16,626** resources reported in the global catalog.
- PayAI `GET /discovery/resources?payTo=0x60B3C6c053E926460D1E1053c516c859C95365e6&limit=100`: HTTP 200, **0** items and `pagination.total=0`.
- **Conclusion:** the catalog itself works, but none of SignalLayer's three paid resources were returned for the payee at the time checked. This is strong evidence of a current PayAI Bazaar discovery gap, not a proof that the x402 payment mechanism fails.
- Official MCP Registry API check timed out from that GitHub runner. Version status remains unverified by this audit.

[Audit run and downloadable JSON](https://github.com/xavierleterrible-hub/signallayer-preflight/actions/runs/37712026538).

**Next backend diagnosis (do not change payment facilitator blindly):** inspect the *live* HTTP 402 `extensions.bazaar`, whether the x402 V2 payment payload echoes it, and any `EXTENSION-RESPONSES` after settlement. Compare with the [official Bazaar specification](https://github.com/x402-foundation/x402/blob/main/specs/extensions/bazaar.md). Avoid another self-payment without explicit authorization. Re-query PayAI after any verified correction.

## Production deployment — SignalLayer 2.1.1 (2026-10-07)

- Added **MCP Bazaar discovery extensions** in paid MCP PaymentRequired results for `agent_preflight`, `market_execution_intel`, and `structured_extract`.
- Read-only verification of all three **live** MCP paid-tool challenges confirmed `extensions.bazaar.info.input.type = "mcp"`, correct tool name, unchanged Base Mainnet network, recipient wallet and fees ($0.01 / $0.03 / $0.02).
- HTTP paid endpoints also returned their existing `extensions.bazaar` in all three unsigned 402 challenges. The free router remained HTTP 200.
- Added **privacy-safe payment telemetry** recording whether an incoming authorized x402 payment echoes the Bazaar extension and the facilitator's optional `EXTENSION-RESPONSES` Bazaar status. No private keys, full signatures, or payment authorization payloads are logged.
- Production `/_api/x402-status` now reports version 2.1.1.
- The external PayAI seller filter still returned zero resources immediately after deployment, as expected until cataloging happens on a compatible external settlement (or PayAI resolves another cataloging issue). **Do not call this a published PayAI Bazaar listing yet.**
- Typecheck clean; existing Floot specs passed. Unpaid production tests confirm challenge metadata only; **paid MCP settlement remains unproven**, and should not be advertised as tested.
- Next business milestone: one independent buyer, with `bazaarEchoed=true` and a successful `bazaarCatalogStatus` if supported. Self-payments are not counted as customers.

## Major unverified integration gaps

- Does the facilitator index SignalLayer's actual resources in **Bazaar**? A public `.well-known/x402.json` alone does not prove this. Validate via facilitator discovery catalog and extension processing status.
- Does x402-over-**MCP** settle successfully, or only x402-over-HTTP?
- Do MCP `structuredContent` values conform to declared `outputSchema`?
- Are externally sourced fields safely escaped and protected against SSRF / prompt injection?
- What are the variable costs and latency percentiles per paid tool?
