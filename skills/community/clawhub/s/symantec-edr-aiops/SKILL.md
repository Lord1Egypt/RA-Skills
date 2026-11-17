---
name: symantec-edr-aiops
slug: symantec-edr-aiops
displayName: "Symantec Endpoint Detection and Response (on-premises) AIops"
summary: "Audited on-prem EDR investigation, threat-feed and sandbox-result operations."
license: MIT
homepage: https://github.com/AIops-tools/Symantec-EDR-AIops
tags: [aiops, mcp, governance, symantec, edr]
description: >
  Use for read-only on-premises Symantec EDR appliance, incidents, events, entities, threat feeds, policy lists and sandbox results.
installer:
  kind: uv
  package: symantec-edr-aiops
argument-hint: "[resource ID or time range]"
allowed-tools:
  - Bash
metadata: {"openclaw":{"requires":{"anyBins":["uvx"]},"optional":{"env":["SYMANTEC_EDR_URL", "SYMANTEC_EDR_CLIENT_ID", "SYMANTEC_EDR_CLIENT_SECRET"]},"homepage":"https://github.com/AIops-tools/Symantec-EDR-AIops","emoji":"🔐","os":["macos","linux","windows"]}}
---

# Symantec Endpoint Detection and Response (on-premises) AIops

Start with `symantec-edr-aiops appliances`. Search incidents and events over at most 30 days, audit events over at most seven days; use the returned opaque next cursor for pagination. No configuration writes are exposed. Read the [verification status](../../docs/VERIFICATION.md) before interpreting an empty or incomplete response.

See the [operations catalog](../../docs/OPERATIONS.md) for every tool and its verification limits.
