---
name: upgrade-guardian
description: A cognitive protocol for safely managing and auditing OpenClaw application upgrades. Analyzes configuration-level risks (schema, defaults) and runtime-level behavioral shifts (routing, sessions, streaming) using semantic changelog analysis to prevent silent breaking changes.
---

# Cognitive Protocol: The Upgrade Guardian

This skill defines a formal, multi-phase cognitive protocol for an agent to execute when tasked with managing an application upgrade. Its purpose is to transcend simple, static checks and provide a dynamic, intelligent analysis that prevents "silent breaking change" incidents.

**This is not a script.** It is a directive for higher-order reasoning.

## Core Principle

An application upgrade is a high-stakes event. The agent must not trust that the upgrade is safe. The agent must assume that any change can have unintended consequences on a stable system. The goal is to make implicit environmental assumptions explicit and resilient before they break.

## Protocol Activation

This protocol is activated when a human operator declares their intent to upgrade the application (e.g., "We are planning to upgrade OpenClaw from vA to vB").

## Analysis Scope

Upgrade Guardian covers **two categories of risks**:

1. **Configuration-level risks**: Changes that affect `openclaw.json` or static config files
   - Breaking changes in schema or validation
   - Deprecated config fields
   - New required config options
   - Default value changes

2. **Runtime-level risks**: Changes that affect behavior without config modifications
   - Behavioral shifts in session handling, routing, or delivery
   - Logic changes in compaction, memory, or agents
   - Protocol-level changes (streaming, API compatibility)
   - CLI UX changes (e.g., `/new` behavior)

See `references/RISK_CATEGORIES.md` for detailed taxonomy.

## Phase 1: Information Gathering & Semantic Analysis

1. **Ingest Release Notes**: Fetch the `CHANGELOG` or release notes for the target version range.
2. **Semantic Analysis**: Perform semantic analysis using patterns in `references/changelog_analysis_patterns.md`.
   - Do not just search for "breaking change"
   - Look for behavioral shift indicators (refactor, unify, improve handling, etc.)
   - Identify both config-affecting and runtime-only changes
3. **Cross-Reference with Environment**:
   - **For config risks**: Load `openclaw.json` and identify dependencies on implicit behaviors
   - **For runtime risks**: Identify active workflows (cron jobs, TUI usage, session routing patterns) that may be affected

## Phase 2: Risk Assessment & Scenario Planning

### 2.1 Formulate "What-If" Scenarios

For each identified change, generate concrete, testable failure scenarios:

**Config-level examples:**
- *Scenario A*: "What if 'improved session handling' means a new, destructive default for unconfigured session types? → Data loss."
- *Scenario B*: "What if 'refactored security policy' means the `allowlist` now requires explicit IP ranges? → Plugin executions fail."

**Runtime-level examples:**
- *Scenario C*: "What if 'duplicate reply suppression' changes session routing logic? → Bot stops responding in some groups."
- *Scenario D*: "What if `/new` now creates independent sessions instead of resetting shared session? → User workflow disrupted."
- *Scenario E*: "What if 'streaming compatibility fix' breaks non-native OpenAI-compatible providers? → Long responses fail mid-stream."

### 2.2 Quantify Risk

Assign a risk score based on:
- **Impact**: data loss > service outage > UX friction > cosmetic
- **Likelihood**: direct config/workflow overlap > tangential relation > theoretical

### 2.3 Generate Audit Report

Present findings to the operator using the template in `references/AUDIT_REPORT_TEMPLATE.md`.

**Key sections:**
- Configuration risks (with jq paths and explicit mitigations)
- Runtime risks (with behavioral descriptions and verification tests)
- Risk prioritization (High/Medium/Low)

## Phase 3: Mitigation & Verification

### 3.1 Proactive Mitigation

**For config risks**: Propose specific `openclaw.json` changes to make implicit assumptions explicit. Do not execute without operator approval.

**For runtime risks**: Document expected behavioral changes and suggest workflow adjustments if needed.

### 3.2 Verification Plan

Define clear, simple tests for each risk:

**Config verification examples:**
- "Run `openclaw doctor` and confirm no validation errors"
- "Check `gateway.err.log` for auth mode complaints"

**Runtime verification examples:**
- "Send test message in group chat, verify bot responds"
- "Open TUI, run `/new`, confirm it creates independent session"
- "Trigger long completion from streaming provider, verify no mid-stream failure"

### 3.3 Post-Upgrade Audit

After the operator confirms upgrade is complete:
1. Execute verification plan
2. Report results systematically
3. Recommend rollback if critical failures detected

### 3.4 Archive Upgrade Artifacts (relative to workspace)

Save the upgrade write-ups and check results **inside the agent workspace** so they remain discoverable and portable.

**Write locations (relative paths):**
- Pre-upgrade analysis report → `kb/logs/upgrade-reports/YYYY-MM-DD_<from>-to-<to>_upgrade-analysis.md`
- Post-upgrade verification report → `kb/logs/upgrade-verifications/YYYY-MM-DD_post-upgrade-verification.txt`

Notes:
- Prefer **workspace-relative paths** in reports (avoid hard-coded absolute home paths).
- If `kb/` is a symlink in a particular deployment, still refer to it as `kb/...` in the protocol/report; the filesystem mapping is an implementation detail.

## References

- `references/changelog_analysis_patterns.md` - Semantic analysis patterns
- `references/RISK_CATEGORIES.md` - Detailed risk taxonomy
- `references/AUDIT_REPORT_TEMPLATE.md` - Report structure
- `references/VERIFICATION_CHECKLIST.md` - Common verification tests

## Notes

- This protocol is designed to be **conservative**. It's better to flag a false positive than miss a silent breaking change.
- Runtime risks are often harder to detect than config risks. Pay extra attention to behavioral keywords like "improve", "fix", "refactor" in areas you actively use (sessions, routing, streaming).
- When in doubt, ask the operator about their workflow patterns before deeming a risk "Low" priority.
