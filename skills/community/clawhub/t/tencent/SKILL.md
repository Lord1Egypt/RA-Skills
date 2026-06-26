---
name: Tencent
slug: tencent
version: 1.0.0
homepage: https://clawic.com/skills/tencent
description: Navigate Tencent products, Tencent Cloud services, and WeChat ecosystem decisions with region-aware planning and official-source verification.
changelog: Initial release with ecosystem routing, region-aware guidance, official-source verification, and safer Tencent planning workflows.
metadata: {"clawdbot":{"emoji":"T","requires":{"bins":[],"config":["~/tencent/"]},"os":["linux","darwin","win32"],"configPaths":["~/tencent/"]}}
---

## When to Use

User needs help choosing, comparing, implementing, or de-risking something in the Tencent ecosystem. Use this for Tencent Cloud architecture, WeChat and WeCom decisions, Mini Program planning, payments and ads context, China-versus-global rollouts, and official-doc verification when Tencent naming is ambiguous.

Do not use it as a general China market strategy skill or as a substitute for dedicated product skills when the task is already narrowed to a single tool.

## Architecture

Memory lives in `~/tencent/`. If `~/tencent/` does not exist, run `setup.md`. See `memory-template.md` for structure.

```text
~/tencent/
|- memory.md           # Activation rules, product scope, and preferred outputs
|- accounts.md         # Known tenants, products, and ownership boundaries
|- regions.md          # Mainland, Hong Kong, Singapore, and global rollout notes
|- sources.md          # Official docs, trusted translators, and weak-source warnings
`- decisions.md        # Final recommendations, assumptions, and open risks
```

## Quick Reference

Use the smallest relevant file for the current task.

| Topic | File | Use it for |
|-------|------|------------|
| Setup flow and saved defaults | `setup.md` | Initialize local state and activation rules |
| Memory schema and status values | `memory-template.md` | Create baseline local files |
| Tencent surface-area map | `ecosystem-map.md` | Route requests to the right Tencent product family |
| Product and vendor choice | `decision-framework.md` | Turn vague Tencent requests into a decision path |
| Tencent Cloud planning | `cloud-platform.md` | Map workloads, regions, and operations to Tencent Cloud |
| Mainland-versus-global constraints | `mainland-vs-global.md` | Check region, residency, language, and go-live risks |
| Official-source handling | `source-validation.md` | Verify docs, translations, and time-sensitive claims |
| Delivery and escalation checklist | `rollout-checklist.md` | Final review before recommending implementation or launch |

## Requirements

- No credentials required for planning, research, or source verification
- Account-specific execution may require user-approved access to Tencent Cloud, WeChat, or partner consoles
- Never ask the user to paste passwords, QR-login secrets, SMS codes, cookies, or private access keys into chat

## Data Storage

Save only durable context that improves later Tencent work:

- product families the user actually uses
- account or tenant names that the user explicitly shares
- preferred regions, languages, and documentation sources
- repeated compliance or rollout constraints
- final decisions with open risks and follow-up items

Do not store secrets, billing exports, raw customer data, or copied console tokens.

## Core Rules

### 1. Lock the Tencent Surface First
- Start by classifying the request into one primary surface: Tencent corporate, Tencent Cloud, WeChat ecosystem, business collaboration, ads and growth, payments, or games and content.
- If the user mixes several surfaces, split the answer into separate workstreams instead of pretending one Tencent path covers all of them.
- Most bad recommendations happen because "Tencent" was left vague.

### 2. Make Region and Audience Explicit
- Every Tencent recommendation must state whether it targets mainland China, Hong Kong, Singapore, or broader international users.
- Also state the audience: consumers, enterprise teams, developers, advertisers, merchants, or operations.
- Product availability, docs, onboarding, payments, and compliance differ sharply by region and audience.

### 3. Prefer Official Sources, Then Reconcile Translations
- For product behavior, limits, pricing, regulatory statements, SDK support, or launch requirements, start from Tencent-owned documentation and product pages.
- If English and Chinese sources diverge, record the mismatch and prefer the fresher or more specific original source.
- Never present translated summaries as stronger evidence than the original product documentation.

### 4. Translate Business Goals Into Product Decisions
- Convert vague asks like "We need Tencent for China" into a concrete job: messaging, identity, payments, compute, object storage, ads, distribution, or local operations.
- Use the matrix in `decision-framework.md` before naming tools.
- Do not dump product lists when the user really needs a decision.

### 5. Treat Tencent Cloud as Its Own Platform
- Map workloads using Tencent Cloud services and operational realities, not AWS names pasted onto a different console.
- Call out region support, account boundaries, observability gaps, and managed-service tradeoffs before recommending architecture.
- If a workload depends on mainland data residency, ICP, or cross-border traffic, say so up front.

### 6. Separate Research Guidance From Execution Rights
- Planning and verification are safe defaults.
- Any step that would log in, change cloud resources, submit app assets, or touch payments must wait for explicit user approval and the correct account context.
- Never assume the same operator owns Tencent Cloud, WeChat OA, WeCom, ads, and payments.

### 7. End With a Decision Record
- Finish every non-trivial task with a concise decision record: chosen path, rejected paths, assumptions, hard blockers, and what still needs human confirmation.
- Save only that durable decision state under `~/tencent/`.
- This keeps future Tencent work consistent instead of repeating the same ambiguity.

## Common Traps

- Treating Tencent, Tencent Cloud, WeChat, WeCom, and QQ as one interchangeable product family -> wrong routing and wrong owners
- Assuming international docs are complete mirrors of mainland documentation -> missing limits, onboarding steps, or pricing details
- Recommending Tencent Cloud by AWS analogy alone -> service names may look familiar while operations differ materially
- Ignoring mainland-versus-global rollout constraints until the end -> late blockers around residency, ICP, language, or payments
- Using unofficial English blog posts as primary evidence -> outdated or simplified guidance becomes product truth
- Assuming one enterprise account can approve all Tencent surfaces -> ownership and permissions are usually fragmented

## External Endpoints

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| https://www.tencent.com | Query text and page requests | Corporate and product-overview verification |
| https://cloud.tencent.com | Query text and page requests | Mainland Tencent Cloud documentation and pricing |
| https://www.tencentcloud.com | Query text and page requests | International Tencent Cloud documentation and product availability |
| https://developers.weixin.qq.com | Query text and page requests | WeChat Mini Program and ecosystem developer documentation |
| https://work.weixin.qq.com | Query text and page requests | WeCom product and admin documentation |

No other endpoints should be used unless the user explicitly approves additional sources or account-specific execution.

## Security & Privacy

Data that may leave your machine:
- search terms and page requests sent to Tencent-owned documentation or product sites
- optional notes sent to user-approved comparison sources when official docs are incomplete

Data that stays local:
- activation preferences and Tencent work history under `~/tencent/`
- account labels, region defaults, and decision records saved in local markdown files
- trusted-source notes and rollout constraints

This skill does NOT:
- store secrets in local markdown files
- claim a product is available everywhere without checking region
- log into Tencent surfaces without explicit user approval
- rewrite its own skill definition files

## Trust

This skill depends on Tencent-owned sites and any approved supporting sources used for verification.
Only install and use it if you trust those services with your research queries and planning workflow.

## Scope

This skill ONLY:
- routes Tencent-related requests to the correct product family
- compares Tencent options using official-source verification
- plans Tencent Cloud, WeChat ecosystem, and region-sensitive rollouts
- keeps lightweight local memory in `~/tencent/`

This skill NEVER:
- invent product capabilities or region availability
- treat unofficial summaries as final evidence
- request passwords, QR login tokens, cookies, or raw secrets
- execute account-changing actions without explicit user approval

## Related Skills
Install with `clawhub install <slug>` if user confirms:

- `cloud` - General cloud architecture and platform tradeoff guidance
- `cloud-storage` - Object storage design, migration, and operations patterns
- `payments` - Payment flow design, merchant risk checks, and launch discipline
- `in-depth-research` - Broader market and source-comparison workflows
- `market-research` - Competitive and market-level framing beyond product routing

## Feedback

- If useful: `clawhub star tencent`
- Stay updated: `clawhub sync`
