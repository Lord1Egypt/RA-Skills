# Safe Self-Improvement Agent

> A security-hardened self-improvement skill for [OpenClaw](https://github.com/openclaw/openclaw) with mandatory human-approval, automated sanitization, audit tooling, and promotion rate-limiting.

## Why This Exists

The popular [Self-Improving Agent](https://github.com/peterskoett/self-improving-agent) skill solves a real problem: AI agents forget everything between sessions. But it carries significant security risks — auto-modifying core files, hook scripts reading output, no secret redaction enforcement.

This skill preserves the best parts while closing every risk vector, and adds automated tooling to make the protections real rather than advisory.

## What It Does

### Core Features

- 📝 **Structured logging** — Errors, learnings, feature requests in `.learnings/` with standardized formats and IDs
- 🔍 **Automatic trigger detection** — Logs on corrections, failures, knowledge gaps, better approaches
- 📈 **Recurring pattern detection** — Links related entries, tracks recurrence count, bumps priority
- 🚀 **Learning promotion** — Recurring learnings (≥3 in 30 days, ≥2 tasks) proposed for promotion
- 📋 **Periodic audit** — Automated checks for sensitive data, format consistency, orphaned links
- 🔒 **Promotion rate-limiting** — Max 3 promotions per 24h, 6h cooldown between batches

### Security Hardening

| Risk | Original | Safe Version |
|------|----------|-------------|
| Auto-modify core files | ✅ Auto | ✅ Human-approval gate |
| Hook scripts read output | ✅ Yes | ❌ Removed |
| Secrets in logs | ⚠️ Soft | ✅ **Script-enforced sanitization** |
| Bulk promotion abuse | ❌ Unchecked | ✅ **Rate-limiting + cooldown period** |
| No self-audit | ❌ None | ✅ **Automated audit.sh** |
| High-security use | ❌ No warning | ✅ **Explicit disclaimer** |
| Dynamic payload fetching | ⚠️ Risk | ✅ **Explicitly forbidden** |

## Installation

```bash
git clone https://github.com/gateswell/safe-self-improvement-agent.git ~/.openclaw/skills/safe-self-improvement
```

Or copy the `skills/safe-self-improvement/` directory to your OpenClaw skills directory. OpenClaw auto-loads on next session.

## Quick Start

On first use, the skill creates `.learnings/` in your workspace:

```
~/.openclaw/workspace/.learnings/
├── LEARNINGS.md
├── ERRORS.md
└── FEATURE_REQUESTS.md
```

### Logging Example

```
You: No, we use pnpm not npm.
→ ./scripts/sanitize.sh "pnpm not npm"
   ✅ Passed → Logged to .learnings/LEARNINGS.md as LRN-20260428-001
```

### Promotion Flow

```
Agent: Learning LRN-20260428-001 recurred 3 times.
       Propose adding to TOOLS.md: "Use pnpm, not npm"
       Approve?

You: yes
→ ./scripts/promotion-gate.sh approve LRN-20260428-001
   ✅ Approved → Agent modifies TOOLS.md → marks entry "promoted"
```

### Audit

```bash
./scripts/audit.sh
# Checks: sensitive data | format consistency | orphaned links | file sizes
# Output: CLEAN / PASSED with warnings / FAILED
```

## File Structure

```
safe-self-improvement/
├── SKILL.md                    # Core skill instructions (required)
├── README.md                   # This file
├── LICENSE                     # MIT
└── scripts/
    ├── sanitize.sh             # Block sensitive data before logging
    ├── audit.sh                # Full learnings directory audit
    └── promotion-gate.sh       # Rate-limit + cooldown enforcement
```

## Security Limitations

**⚠️ This skill's protections are based on AI instruction adherence, not hardware-level isolation.**

- In high-security environments (financial, medical, critical infrastructure): **do not use**
- For teams: set `.learnings/` to read-only (`chmod 555`) and make writable only during approved promotions
- The sanitization script provides a strong defense layer but cannot block 100% of edge cases

## Comparison with Original

| Feature | Self-Improving Agent | Safe Self-Improvement |
|---------|----------------------|-----------------------|
| Structured logging | ✅ | ✅ |
| Auto trigger detection | ✅ | ✅ |
| Recurring pattern detection | ✅ | ✅ |
| Learning promotion | ✅ Auto | ✅ Human gate |
| Hook scripts | ✅ | ❌ Removed |
| Secret sanitization | ⚠️ Soft | ✅ **Script-enforced** |
| Audit tooling | ❌ | ✅ **audit.sh** |
| Promotion rate-limiting | ❌ | ✅ **promotion-gate.sh** |
| Security disclaimer | ❌ | ✅ |
| Size | ~500 lines | ~280 lines (SKILL.md) |

## Credits

Based on [peterskoett/self-improving-agent](https://github.com/peterskoett/self-improving-agent), remade from [pskoett/pskoett-ai-skills](https://github.com/pskoett/pskoett-ai-skills).

This project reimagines that work with security-first engineering. The core improvement workflow is preserved; risky automation is replaced with human-in-the-loop controls and automated tooling.

## License

MIT
