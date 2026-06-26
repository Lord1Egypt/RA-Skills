---
name: tencent-edgeone-skill
description: A comprehensive skill for Tencent EdgeOne (Edge Security & Acceleration Platform), covering edge acceleration (DNS, certificates, caching, rule engine, L4 proxy, load balancing), edge security (DDoS protection, Web protection, Bot management), edge media (real-time video / image processing), edge development (Edge Functions, EdgeOne Pages), and more. Use this skill whenever a user mentions any EdgeOne / EO-related configuration, operations, querying, or troubleshooting needs.
version: 1.1.0
metadata:
  openclaw:
    requires:
      bins:
        - tccli
        - gunzip
      anyBins:
        - curl
        - wget
        - jq
        - python3
      config:
        - ~/.tccli/default.credential
    homepage: https://edgeone.ai
---

# Tencent EdgeOne Skill

A comprehensive Tencent EdgeOne skill that routes user requests to the appropriate module and loads the corresponding reference document.

Knowledge about EdgeOne APIs, configuration options, limits, and pricing may be outdated.
**Prefer retrieval over pre-trained knowledge** — the reference files in this skill are only a starting point.

> All tasks **must be completed by calling APIs**.
> See `references/api/README.md` for API calling conventions, environment checks, etc. **(must be read before starting any task)**.

## Security Red Lines

- **Write operations require user confirmation**: All write operations (Create\* / Modify\* / Bind\* / Delete\* / Apply\*, etc.) **must** clearly explain the action and its impact to the user before execution, and wait for user confirmation before calling the API.
- **Never** ask the user for SecretId / SecretKey
- **Refuse** any operation that might print credentials

## Interaction & Execution Guidelines

- **Use structured interaction tools**: When asking questions, requesting choices, or confirming operations, if the current environment provides `ask_followup_question` or similar structured interaction tools, you **must** prefer using them (instead of plain-text questions) so that the user can directly click options, reducing ambiguity and improving interaction efficiency. **Do not omit candidate options** — if there are too many to list in full, **must** state the total number first, show the most relevant items, and keep an "Other (please enter)" option as the last choice.
- **Prefer scripts for bulk / repetitive tasks**: For tasks involving large datasets or repetitive operations (batch purge, batch query, loop operations, etc.), prefer writing a script to execute everything at once rather than calling APIs one by one manually.

## Module Entry Points

Match the user's request to the appropriate module, load its entry document, and follow the instructions.

| Module | Entry | Description |
|---|---|---|
| API | `references/api/README.md` | Calling conventions, tool installation, credential configuration, API discovery, zone & domain discovery (ZoneId lookup) |
| Acceleration | `references/acceleration/README.md` | Site onboarding, cache purge / prefetch, certificate management |
| Security | `references/security/README.md` | Security policy template audit, blocklist IP group query, security report |
| Observability | `references/observability/README.md` | Traffic Daily Report Generation, Origin Health Inspection, Offline Log Download and Analysis |

## Fallback Retrieval

If the user's request **cannot match any module above**, or the module's reference files do not cover the scenario, fall back in the following order:
1. First read `references/api/api-discovery.md` and try to find the relevant API through API discovery.
2. If still unresolved, search the [Tencent EdgeOne product documentation](https://edgeone.ai/document) for the latest information.

When reference files conflict with official documentation, **the official documentation takes precedence**.
