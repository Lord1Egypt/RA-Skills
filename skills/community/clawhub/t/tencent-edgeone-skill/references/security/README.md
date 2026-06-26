# EdgeOne Security Protection Reference

> **Telemetry note:** You are now in module **`security`**. Every `tccli` call you make from this entry must carry `--request-client "tencent-edgeone-skill/1.1.0 module/security"`.

Configuration and operations guide for security policy configuration snapshots, template coverage audits, and domain IP group blocklist identification.

## Quick Decision Tree

```
What does the user want to do?
│
├─ "Generate a security status report for this week"
│  "Check the current security configuration"
│  └─ → `security-weekly-report.md`  🟢 Low risk · Sequential data collection, output conclusions first with concise snapshot
│
├─ "Which domains don't have a security template"
│  "Help me check template coverage"
│  └─ → `security-template-audit.md`  🟢 Low risk · List unbound domains, prompt for manual confirmation
│
├─ "Check which IP group in example.com's security policy is a blocklist"
│  "Which IP group blocks traffic for this domain"
│  └─ → `domain-blacklist-inspector.md`  🟢 Low risk · Read-only query, identify blocklist IP groups
│
├─ "Help me analyze recent attack IP concentration"
│  "Block these IPs" "IP ban"
│  └─ → `ip-threat-blacklist.md`  🔴 High risk · Mandatory Diff display + double confirmation before write operations, only allowed to write to designated blocklist group
│
└─ Not sure which API to call
   └─ → `../api/api-discovery.md`
```

## Prerequisites

All operations require calling APIs via tccli. Before first use, complete the following:

1. **Tool check** — Read `../api/README.md` to complete tccli installation and credential configuration
2. **Get ZoneId** — Read `../api/zone-discovery.md` to obtain the zone ID

## Files in This Directory

| File | Risk Level | Core Trigger Scenario |
|---|---|---|
| `security-weekly-report.md` | 🟢 Low risk | Periodically generate security configuration snapshots to detect abnormal policy changes |
| `security-template-audit.md` | 🟢 Low risk | Audit security policy template coverage, find domains without bound templates |
| `domain-blacklist-inspector.md` | 🟢 Low risk | Query security policies associated with a specific domain, identify IP groups serving as blocklists |
| `ip-threat-blacklist.md` | 🔴 High risk | Analyze L7 high-concentration threat IPs, execute IP blocklist banning (write operations require double confirmation) |

## Reference Links

- [EdgeOne Product Documentation](https://edgeone.ai/document)
- [EdgeOne API Documentation](https://edgeone.ai/document/50454)
- API Calling Guide: `../api/README.md`
