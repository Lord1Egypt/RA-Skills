## Release Notes — Tasker v1.2.0

**Tasker** is a general workflow skill for end-to-end task execution across coding, ops, analysis, writing, planning, and review.

---

### 🔖 Version Info

| Field | Value |
|-------|-------|
| **Version** | `v1.2.0` |
| **Previous** | `v1.1.1` |
| **Semver** | `minor` (backward-compatible feature additions) |
| **Author** | `tealun` |
| **Platforms** | ClawHub / SkillHub (Tencent) |
| **License** | MIT-0 |

---

### 🎯 What's New in v1.2.0

This release introduces **7 production-hardening features** that transform Tasker from a linear execution checklist into a **resilient, adaptive, and multi-agent-ready workflow framework**.

#### 1. Bidirectional State Machine with Retreat
- **Before:** `intake → clarify → plan → confirm → execute → verify → close` (one-way, no way back)
- **Now:** Any stage can **retreat** to the previous stage with a stated reason. `execute` failures roll back to `plan`; `verify` gaps roll back to `execute`.
- **Guardrail:** Retreat 3 times → auto-upgrade the task level (S→M, M→L) and require human-in-the-loop before retry.

#### 2. Time Budget & Timeout Protection
- Added per-step timeouts (`S: 60s`, `M: 300s`, `L: 900s`) and total transition budgets (`S: 3`, `M: 8`, `L: 15`).
- Budget exceeded → graceful close with `[budget-exceeded]` status and decomposition recommendation.
- Prevents infinite execution loops and runaway tasks.

#### 3. Context-Aware Risk Sizing (Intent + Modifiers)
- **Base:** Keyword-weighted S/M/L scoring (unchanged).
- **New modifiers:** `Session Context` (parent task level, prior failures), `Path Modifier` (sensitive directories like `config/`, `.env/`, `ssh/`), and `User Modifier` (production mentions, user downgrades).
- Reduces false positives (e.g., "modify login page color" was L, now correctly manageable) and catches hidden risks (e.g., "view this file" pointing to `/etc/passwd`).

#### 4. Dissatisfaction Root-Cause Classification & Improvement Tracking
- **5 dissatisfaction classes:** Result Error, Process Error, Comprehension Error, Communication Error, Performance Error.
- **6 root-cause tags:** `hallucination`, `omission`, `misread`, `tool-failure`, `user-ambiguity`, `logic-flaw`.
- **Proactive safeguard:** If the same root cause appears 2+ times in a session, the next task automatically applies the corresponding protection (e.g., stricter PTV after hallucination, file-listing before execution after omission).

#### 5. Extended Output Modes (Multi-File & Pagination)
- Added `multi-file` mode with **Artifact Map** (role, path, status per file).
- Added `pagination` mode for outputs exceeding 2000 tokens (auto-split with `[Part N/M]` and table of contents).
- Added **Risk & Residual** disclosure section (unverified assumptions, edge cases, follow-up recommendations).

#### 6. Built-In Execution Depth Control (Replaces External PUA Dependency)
- **3 depth levels** mapped to S/M/L: file-read depth, test coverage, boundary checks, documentation, and rollback preparation.
- PUA is now an **optional style layer** (tone/verbosity) rather than a required control layer.
- Tasker is self-sufficient when PUA is unavailable.

#### 7. Multi-Agent Handoff Protocol
- **Escalation triggers:** Large tasks auto-suggest delegation to `swarm-coding`, `batch-download`, `deep-research-swarm`, or `cron`.
- **Handoff file:** Structured `tasker_handoff.md` written to workspace, containing parent goal, scope, forbidden paths, done definition, and validation method.
- **State pass-through:** Other skills consume the handoff file as "established facts" to avoid repeated clarification.

---

### 🔄 Upgrade Notes

- **Backward Compatible:** All v1.1.1 behaviors are preserved. New features are additive.
- **No new credentials or binaries required.**
- **PUA users:** If you use `pua`, it continues to work as a style layer. No breaking changes.

---

### 🚀 Quick Start

```bash
# Install (new)
openclaw skills install tealun/tasker

# Or upgrade from v1.1.1
openclaw skills update tealun/tasker

# Lightweight entry
/tasker

# Typical usage
"Debug why this Python script fails when reading CSV files with Chinese characters"
```

---

### 🛡️ Safety & Audit

- **Security scan:** Passed (Tencent SkillHub: 科恩实验室 + 云鼎实验室 dual verification).
- **Risk profile:** Low — instruction-only, no credentials, no network access, no binary execution.
- **Instruction scope:** Flow control, gates, and output boundaries only. No external side effects initiated by the skill itself.

---

### 📋 Compatibility Matrix

| Platform | Version | Status |
|----------|---------|--------|
| OpenClaw | 2026.2+ | ✅ Verified |
| Clawdbot | 2.x+ | ✅ Verified |
| SkillHub (Tencent) | v1+ | ✅ Verified |
| Claude Code | 1.x+ | ✅ Compatible |
| Cursor | 0.4x+ | ✅ Compatible |

---

### 📝 Changelog (v1.1.1 → v1.2.0)

| Category | Changes |
|----------|---------|
| **Architecture** | Bidirectional state machine with retreat rules and retry caps |
| **Reliability** | Time budgets, step timeouts, and transition limits |
| **Risk Model** | Context-aware sizing with session/path/user modifiers |
| **Quality** | Root-cause tagging and proactive improvement tracking |
| **Output** | Multi-file artifact map, pagination, and risk disclosure |
| **Depth Control** | Built-in depth levels (1/2/3) decoupled from external PUA |
| **Interoperability** | Multi-agent handoff protocol with `tasker_handoff.md` |

---

### 🔗 Links

- **ClawHub:** `https://clawhub.ai/tealun/tasker`
- **SkillHub:** `https://skillhub.cloud.tencent.com/skills/tasker`
- **Project:** `https://github.com/tanweai/pua` (optional PUA layer)

---

*Tasker v1.2.0 — Execute with discipline. Retreat with reason. Escalate with clarity.*
