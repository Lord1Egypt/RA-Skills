---
name: skill-upgrade-checker
description: "Check all installed skills for available upgrades, interpret version changes and risk, and execute upgrades with user confirmation. | 检查所有已安装技能的可用升级，解读版本变更与风险，经用户确认后执行升级"
---

# Skill Upgrade Checker

**Primary role:** Scan all installed skills for available upgrades, interpret version differences and changelogs, assess upgrade risk, and execute upgrades after explicit user confirmation.

**主要职责：** 扫描所有已安装技能的可用升级，解读版本差异与变更日志，评估升级风险，经用户明确确认后执行升级。

## Prerequisites

Before this skill can operate, confirm the following:

- **`clawhub` CLI is installed** and available in the agent's `PATH`. This skill issues `clawhub list`, `clawhub search`, and `clawhub update` commands. If the binary is absent, all operations will fail.
- **Authentication:** Run `clawhub login` in advance. The clawhub CLI stores credentials in its own default config path (managed by the CLI, not by this skill). No additional environment variables are required by this skill.
- **Permissions in scope:** This skill will only:
  1. Read the installed skill list via `clawhub list` (read-only).
  2. Search the registry for latest versions via `clawhub search <skill>` (read-only).
  3. Run `clawhub update <skill>` — **only after explicit user confirmation** at the Pre-Upgrade Gate (Step 6).
  It will not access other system files, credentials, or APIs beyond the clawhub CLI.

## Workflow

### 0) Inventory Installed Skills

Run `clawhub list` and parse the output to build a table of all installed skills with their local version numbers.

Additionally, read each skill's `_meta.json` (at `skills/<skill-slug>/_meta.json`) if accessible locally, to get the precise semver from the `version` field.

Output: a list of installed skills with their local versions.

### 1) Query Registry for Latest Versions

For each installed skill, run:
```
clawhub search <skill-slug>
```

Build a comparison table with columns:
- Skill name
- Local version
- Registry version
- Upgrade available (yes / no / unknown)

If `clawhub search` does not return version info for a particular skill (e.g., it is a local-only skill not published to any registry), mark it as **"version unknown — skipped"**.

### 2) Version Comparison and Classification

Apply semver comparison to each skill where an upgrade is available. Classify into:

- **Patch** (e.g., 0.2.1 → 0.2.2): bug fixes only, low risk
- **Minor** (e.g., 0.2.x → 0.3.0): new features, backward-compatible, medium risk
- **Major** (e.g., 0.x → 1.0 or 1.x → 2.0): potential breaking changes, high risk

Edge cases:
- Local version higher than registry → mark as **"local version ahead"** and skip
- Versions equal → mark as **"up to date"**

Present a summary table sorted by risk level (major first).

### 3) Changelog and Diff Interpretation

For each skill with an available upgrade, gather change information in this priority order:

1. **Project-level CHANGELOG:** Check `skills/CHANGELOG.md` for entries between the current and latest version.
2. **Per-skill CHANGELOG:** Check `skills/<skill-slug>/CHANGELOG.md` if it exists (more specific).
3. **Description diff:** Compare the `description` field in local `_meta.json` with the description returned by `clawhub search`. Changes in description may hint at capability changes.
4. **Fallback:** If no changelog data is available from any source, state: "No changelog available — manual review recommended before upgrade."

Summarize changes per skill:
- **Added:** new capabilities
- **Changed:** behavior modifications
- **Fixed:** bug fixes
- **Breaking:** incompatible changes (flag prominently)

### 4) Risk Assessment

For each upgradeable skill, produce a risk rating using these criteria:

| Dimension | LOW | MEDIUM | HIGH | CRITICAL |
|-----------|-----|--------|------|----------|
| Version jump | Patch only | Minor | Major | Major with breaking keywords |
| Breaking change signals | None found | "changed", "refactored" | "deprecated" | "breaking", "removed", "incompatible" |
| Dependency impact | No other skill depends on it | 1 skill depends | 2+ skills depend | Core dependency for many skills |
| Version staleness | < 1 month behind | 1–3 months | 3–6 months | > 6 months behind |
| Adoption signals | High install count | Moderate | Low (< 10) | Very new (< 2 weeks) or unknown |

Combine dimensions into an overall rating: **LOW / MEDIUM / HIGH / CRITICAL**.

### 5) Upgrade Recommendations

Present a prioritized recommendation list, grouped into four tiers:

- **Recommended to upgrade now** (推荐立即升级): low-risk patches and well-established minor updates
- **Upgrade with caution** (谨慎升级): minor updates with some risk signals
- **Review before upgrade** (升级前需审查): major updates or high-risk changes
- **Skip** (跳过): not worth upgrading, risk outweighs benefit, or local version ahead

Include a one-line rationale per skill.

### 6) Pre-Upgrade Confirmation Gate (required)

Before executing any upgrade, present a confirmation summary listing:

- Each skill to be upgraded
- From-version → to-version
- Upgrade type (patch / minor / major)
- Risk rating
- One-line change summary
- The exact `clawhub update <skill>` command to be run

Then ask:

> "Planned action: upgrade **N** skill(s). Confirm which to proceed with — respond with skill names, 'all', or 'none'."

**Major upgrade extra gate:** Even if the user responds with "all", major-version upgrades require **individual confirmation** per skill. Re-prompt for each major upgrade separately with a clear warning about potential breaking changes.

### 7) Execute Upgrades and Post-Upgrade Report

For each confirmed skill, in sequence:

1. Run `clawhub update <skill-slug>`
2. Verify success by re-running `clawhub list` and checking the new version
3. If any upgrade **fails**, stop and report the failure — do not continue blindly

Final output:

**Upgrade Results Table:**

| Skill | Old Version | New Version | Status |
|-------|-------------|-------------|--------|
| ... | ... | ... | Success / Failed |

**Post-Upgrade Summary:**
- Updated skill inventory (full list with current versions)
- Any failures with error details and suggested next steps
- Follow-up suggestion: "Re-run this check periodically to stay current."

## Output Format

### Upgrade Overview Table
| Skill | Local Version | Latest Version | Upgrade Type | Risk Level |
|-------|---------------|----------------|--------------|------------|

### Change Summary (per skill)
- **Added:** ...
- **Changed:** ...
- **Fixed:** ...
- **Breaking:** ...

### Recommendation List
Grouped by tier (Recommended / Caution / Review / Skip) with one-line rationale.

### Pre-Upgrade Confirmation
"Planned action: upgrade <N> skill(s). Source: clawhub. Risks: <summary>. Proceed with: <skill list / all / none>?"

### Upgrade Results
| Skill | Old Version | New Version | Status |

## Guardrails

- Never upgrade without explicit user confirmation.
- Major-version upgrades require individual confirmation even if user says "all".
- If an upgrade fails, stop and report — do not continue blindly.
- Audit first, act second — Steps 0–5 are entirely read-only.
- If local version is ahead of registry, skip and note it — never downgrade.
- If no changelog is available, recommend manual review before proceeding.
- Prefer conservative risk ratings — when uncertain, rate higher rather than lower.
