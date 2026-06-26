# Security Checkup Report Template

Use this structure for the full audit report.

---

## Header

```markdown
# 🔒 OpenClaw Security Audit

**Time**: {datetime}
**Host**: {hostname}
**Level**: {beginner|intermediate|expert}
```

## Summary Table

```markdown
## 📊 Summary

| Severity | Count |
|----------|-------|
| 🔴 Critical | {count} |
| 🟠 High | {count} |
| 🟡 Medium | {count} |
| 🟢 Low | {count} |
| ⚪ Info | {count} |

**Status**: {🟢 Good / 🟡 Needs Attention / 🔴 Action Required}
```

## Findings by Category

**IMPORTANT**: Organize findings by category, not severity.
Within each category, show findings with their severity icons.

```markdown
## ⚡ Runtime

{List all RUNTIME findings with severity icons}
- 🟡 Running on bare metal with sudo available
- ⚪ Tailscale VPN active ✅

## 🤖 Agents

{List all AGENT findings}
- 🟢 Agent 'molty' has exec but critical tools denied ✅
- 🟢 8 agent directories have open permissions

## 📁 Workspace

{List all WORKSPACE findings}
- (none or findings)

## 🧩 Skills

{List all SKILL findings}
- 🟡 4 skills access sensitive paths
- 🟡 2 skills use base64 encoding

## 📢 Channels

{List all CHANNEL findings}
- (none or findings)

## 🌐 Network

{List all NETWORK findings}
- (none or findings)
```

## Quick Summary Box

At the end, provide a quick reference:

```markdown
## 📋 Quick Status

| Category | Status |
|----------|--------|
| VPN | ✅ Tailscale |
| Container | ❌ Bare metal |
| Root | ✅ Not root |
| Sudo | ⚠️ Available |
| Exposed | ⚠️ Yes (but VPN) |
```

## Recommendations

Group by urgency:

```markdown
## ✅ Recommended Actions

### Do Now (Quick Fixes)
1. `chmod 700 ~/.openclaw/agents/*`

### Review Later
1. Check which skills access sensitive paths
2. Review base64 usage in skills

### No Action Needed
- VPN is active, network exposure is mitigated
```

## User-Level Adaptations

### Beginner
- Use analogies (🏠 집, 🔑 열쇠, 🚪 문)
- Simple language, no jargon
- Focus on "what to do"
- One-liner explanations

### Intermediate  
- Technical details with config examples
- Explain the "why"
- Reference commands

### Expert
- Attack vectors and exploitation paths
- Edge cases
- Defense-in-depth options

## Dashboard Auto-Open

After text report, run:
```bash
bash ~/.openclaw/skills/secucheck/scripts/serve_dashboard.sh
```

Then tell user:
```
📊 Dashboard: http://localhost:8766/secucheck-report.html
```

## Footer

```markdown
---

**Next Steps**:
- Review recommendations above
- Tell me if you want to apply any fixes
- "상세 분석" - Detailed analysis of specific item
- "이거 적용해줘" - Apply recommended fix
```
