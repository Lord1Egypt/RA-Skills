---
name: upgrade-openclaw
description: |
  Upgrade OpenClaw and comprehensively discover new features, config options, hooks, and improvements.
  Use when: user says "upgrade openclaw", "update openclaw", "check for openclaw updates",
  "what's new in openclaw", or "/skills upgrade_openclaw". Runs the update, diffs the changelog
  against enabled channels/plugins, performs config schema gap analysis, audits hooks and doctor
  recommendations, and presents ALL findings for user approval before applying.
metadata:
  {
    "openclaw":
      {
        "emoji": "🚀",
        "author": "decentraliser",
        "requires": { "bins": ["openclaw", "curl", "clawhub"] }
      }
  }
---

# Upgrade OpenClaw

Update, diff, audit, propose. Every new feature surfaced. Nothing missed.

## Settings

On first run, check `settings.json` in this skill's directory. If `subagentModel` not set, ask:

> "Which model for upgrade sub-agents? (e.g., `claude-sonnet-4-6`, `deepseek-chat`). Note: external providers will receive config data."

Save to `settings.json`:
```json
{ "subagentModel": "anthropic/claude-sonnet-4-6" }
```

## Procedure

### 1. Record Pre-Update State

Before touching anything:

```bash
PRE_VERSION=$(openclaw --version | grep -oP '\d{4}\.\d+\.\d+')
echo "$PRE_VERSION"
```

Save `PRE_VERSION` — needed for changelog diffing in Step 3.

### 2. Run Update

```bash
openclaw update
```

If dirty working tree, stash first:
```bash
cd "$(openclaw --version 2>&1 | grep -oP '(?<=\().*?(?=\))' || echo ~/openclaw)" 
git stash --include-untracked -m "pre-update stash" && openclaw update
```

Record new version:
```bash
POST_VERSION=$(openclaw --version | grep -oP '\d{4}\.\d+\.\d+')
```

If `PRE_VERSION == POST_VERSION`, report "Already up to date" and skip to Step 5 (audit only).

### 3. Extract Delta Changelog

The changelog lives locally at `~/openclaw/CHANGELOG.md` after update. Versions delimited by `## YYYY.x.x` headers.

Extract only entries between old and new version:

```bash
awk "/^## $POST_VERSION/,/^## $PRE_VERSION/" ~/openclaw/CHANGELOG.md
```

Then **filter by relevance** to this setup:

1. Read current config via `gateway config.get` to identify enabled channels/plugins
2. From the changelog delta, **keep** entries matching:
   - Enabled channels (e.g., Telegram — skip LINE/Discord/Feishu/etc. unless enabled)
   - Core agent/gateway/cron/tools/memory/security changes (always relevant)
   - ACP/sessions/subagent changes (if ACP enabled)
   - Breaking changes (always relevant)
3. **Discard** entries for disabled channels, iOS/macOS app changes, and platforms not in use
4. **Categorize** kept entries into: Features | Fixes | Security | Breaking Changes

### 4. Config Schema Gap Analysis

Fetch the live schema and current config:

- Schema: `gateway config.schema`
- Current: `gateway config.get`

Compare systematically:

1. Walk schema `properties` tree recursively
2. For each schema key path, check if it exists in current config
3. **New/unset options** = schema keys not present in current config (excluding keys with sensible defaults)
4. Focus on actionable fields — ones where setting a non-default value provides clear benefit
5. Flag fields from the changelog delta (new in this version) separately as "New in this release"

Present as a table:
```
| Config Path | Type | Default | Description | New? |
```

### 5. Audit Current Setup

```bash
openclaw hooks list --json
openclaw doctor --non-interactive
clawhub update --all --dry-run 2>&1
```

Collect:
- **Hooks**: any hooks available but not enabled
- **Doctor**: all warnings and recommendations
- **Skills**: any ClawHub updates available

### 6. Present Comprehensive Report

Structure the report exactly like this:

```markdown
## 🔍 Post-Upgrade Report: {PRE_VERSION} → {POST_VERSION}

### 🆕 New Features (Relevant to Your Setup)
- [Feature]: What it does, why it matters for you
  - Config: `path.to.setting` (if applicable)

### 🔧 Notable Fixes
- [Fix]: What was broken, now fixed

### 🔐 Security Updates
- [Security]: What was patched

### ⚠️ Breaking Changes
- [Breaking]: What changed, migration needed

### 📋 New Config Options Available
| Config Path | Type | Default | Why Enable |
|-------------|------|---------|------------|

### 🪝 Hooks Status
- [hook]: enabled/available/new

### 🏥 Doctor Recommendations
- [Item]: severity + action

### 📦 Skill Updates Available
- [skill]: current → available version

---
**Apply these improvements?** Reply with:
- "yes" / "all" — apply everything
- "select" — I'll list numbered items to pick from
- specific items by name
```

**Critical**: Do NOT present a thin report. Every changelog entry that survived the relevance filter in Step 3 MUST appear. Every new config option from Step 4 MUST appear. Every doctor finding from Step 5 MUST appear. The user triggered this skill to see EVERYTHING.

### 7. Apply with Approval

**Never apply without explicit user approval.**

On approval, apply changes via:
- Config changes: `gateway config.patch`
- Hook enablement: `openclaw hooks enable <hook>`
- Skill installs: `clawhub install <skill>`

After applying, pop any git stash:
```bash
cd ~/openclaw && git stash list | grep -q "pre-update stash" && git stash pop
```

### 8. Persist State

Write upgrade state to `state.json` in this skill's directory:

```json
{
  "lastUpgrade": {
    "from": "2026.3.2",
    "to": "2026.3.3",
    "timestamp": "2026-03-05T06:50:00Z",
    "featuresProposed": ["telegram-streaming", "pdf-tool", ...],
    "featuresApplied": ["telegram-streaming", ...],
    "doctorApplied": ["entrypoint-fix", ...]
  }
}
```

This prevents re-proposing on repeated runs and enables "what changed since last upgrade" queries.
