---
name: symantec-clouddlp-aiops
slug: symantec-clouddlp-aiops
displayName: "Symantec Cloud DLP AIops"
summary: "Audited Cloud DLP incident, profile, pattern and index operations."
license: MIT
homepage: https://github.com/AIops-tools/Symantec-CloudDLP-AIops
tags: [aiops, mcp, governance, symantec, clouddlp]
description: >
  Use for read-only Symantec Cloud DLP incidents, profile and detection content, custom groups, data identifiers and index health.
installer:
  kind: uv
  package: symantec-clouddlp-aiops
argument-hint: "[resource ID or time range]"
allowed-tools:
  - Bash
metadata: {"openclaw":{"requires":{"anyBins":["uvx"]},"optional":{"env":["SYMANTEC_CLOUDDLP_URL", "SYMANTEC_CLOUDDLP_KEY_ID", "SYMANTEC_CLOUDDLP_KEY_SECRET", "SYMANTEC_CLOUDDLP_TENANT"]},"homepage":"https://github.com/AIops-tools/Symantec-CloudDLP-AIops","emoji":"🔐","os":["macos","linux","windows"]}}
---

# Symantec Cloud DLP AIops

Start with `symantec-clouddlp-aiops profiles`. Search incidents in a bounded time window and follow the search-after cursor. Profile API response schemas are weakly specified, so raw response shape is surfaced explicitly. No configuration writes are exposed. Read the [verification status](../../docs/VERIFICATION.md) before interpreting an empty or incomplete response.

See the [operations catalog](../../docs/OPERATIONS.md) for every tool and its verification limits.
