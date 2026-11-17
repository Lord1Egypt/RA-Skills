---
name: symantec-ztna-aiops
slug: symantec-ztna-aiops
displayName: "Symantec ZTNA AIops"
summary: "Audited ZTNA connectivity, access, identity, DNS and integration operations."
license: MIT
homepage: https://github.com/AIops-tools/Symantec-ZTNA-AIops
tags: [aiops, mcp, governance, symantec, ztna]
description: >
  Use for read-only Symantec ZTNA site and connector health, applications, access policies, collections, DNS, identities, cloud integrations and audit logs.
installer:
  kind: uv
  package: symantec-ztna-aiops
argument-hint: "[site, connector, application or policy ID]"
allowed-tools:
  - Bash
metadata: {"openclaw":{"requires":{"anyBins":["uvx"]},"optional":{"env":["SYMANTEC_ZTNA_URL","SYMANTEC_ZTNA_CLIENT_ID","SYMANTEC_ZTNA_CLIENT_SECRET"]},"homepage":"https://github.com/AIops-tools/Symantec-ZTNA-AIops","emoji":"🔐","os":["macos","linux","windows"]}}
---

# Symantec ZTNA AIops

Start with `symantec-ztna-aiops health-sample`, then inspect a site with `site-status`, its connectors, and affected applications with `application-status`. Use `policies` and `application-policies` to trace configured access. `audit-logs` searches a bounded time window; follow its cursor only when `truncated` is true. A sample is not full tenant coverage.

Set the tenant API origin, client ID and client secret as described in the [README](../../README.md). No write operations are exposed. See [agent guardrails](references/agent-guardrails.md) and [verification](../../docs/VERIFICATION.md).

See the [operations catalog](../../docs/OPERATIONS.md) for every tool and its verification limits.
