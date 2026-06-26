---
name: skill-guardian
description: Safely manage your AI skill collection with trust scoring, security vetting, delayed auto-updates, and pending periods for new skills. Use when adding new skills, monitoring skill security, tracking versions, or preventing risky automatic updates. Features intelligent update rules (high-trust skills update immediately, others wait 10 days) and 5-10 day pending period for new skill additions. Perfect for users who want a curated, secure skill library without surprises.
---

# Skill Guardian 🛡️

**Your AI skill security guard** — Track, vet, and safely update your skill collection.

**Tags:** `security` `skill-management` `trust-scoring` `auto-update` `cron-ready` `safety` `version-control` `curation` `vetting` `guardian`

## Why Use Skill Guardian?

🔒 **Security First** — Auto-scans every skill before adding  
📊 **Trust Scores** — Know which skills are safe at a glance  
⏰ **Smart Updates** — High-trust skills (≥90) update immediately, others wait 10 days  
📝 **Pending Period** — New skills wait 5-10 days before activation  
🤖 **Auto-Scheduled** — Runs 1-2 times daily automatically  

## Quick Start

### 1. Install & Setup

```bash
# Install the skill
clawhub install skill-guardian

# Set up automated monitoring (recommended)
# See "Automated Scheduling" section below
```

### 2. Add a Skill Safely

```bash
python3 scripts/add_skill.py --name summarize --source clawhub
```

Skill Guardian will:
- ✅ Run security checks
- ✅ Assign trust score (0-100)
- ✅ Add to **pending queue** (5-10 days)
- ✅ Auto-promote after waiting period

### 3. View Your Collection

```bash
python3 scripts/list_skills.py          # Active skills
python3 scripts/show_skill.py summarize # Detailed info
```

### 4. Smart Updates

Check for updates:
```bash
python3 scripts/check_updates.py
```

Apply updates (intelligent rules):
```bash
python3 scripts/apply_updates.py --all
```

**Update Rules:**
- 🌟 Trust ≥90: Immediate update
- ⏳ Trust 70-89: 10-day grace period
- 🛑 Trust <70: Manual approval required

Override for urgent updates:
```bash
python3 scripts/apply_updates.py summarize --force
```

### 5. Process Pending Skills

Manually check pending queue:
```bash
python3 scripts/process_pending.py
```

## Automated Scheduling ⏰ (Recommended)

Skill Guardian works best when run automatically 1-2 times daily.

### Option 1: System Cron

Add to crontab for morning (8am) and evening (8pm) runs:

```bash
# Edit crontab
crontab -e

# Add these lines
0 8 * * * cd /path/to/workspace && python3 skills/skill-guardian/scripts/auto_run.py
0 20 * * * cd /path/to/workspace && python3 skills/skill-guardian/scripts/auto_run.py
```

### Option 2: Single Daily Run

```bash
# Once daily at 9am
0 9 * * * cd /path/to/workspace && python3 skills/skill-guardian/scripts/auto_run.py
```

### Option 3: Manual Execution

If you prefer manual control:

```bash
# Full auto-run workflow
python3 skills/skill-guardian/scripts/auto_run.py

# Or step by step:
python3 scripts/process_pending.py      # Promote pending skills
python3 scripts/check_updates.py        # Check for updates
python3 scripts/apply_updates.py --all  # Apply updates
```

### What Auto-Run Does

Each execution performs:

1. 🔍 **Process Pending** — Promote skills that passed 5-10 day waiting period
2. 📦 **Check Updates** — Detect new versions of all skills
3. 🔄 **Apply Updates** — High-trust (≥90) update immediately, others queued
4. 📊 **Report Status** — Show current registry state

## Trust Score Explained

| Score | Level | Update Behavior | Badge |
|-------|-------|-----------------|-------|
| 90-100 | 🟢 Verified | Immediate auto-update | 🌟 |
| 70-89 | 🟡 Trusted | 10-day grace period | ⏳ |
| 50-69 | 🟠 Caution | Manual approval required | ⚠️ |
| <50 | 🔴 Risky | Blocked from auto-add | 🛑 |

### Included Trusted Skills

| Skill | Trust | Source | Purpose |
|-------|-------|--------|---------|
| jax-skill-security-scanner | 92 | clawhub | Advanced security scanning |
| skill-vetter | 95 | clawhub | Security vetting |
| find-skills | 90 | clawhub | Discover skills |
| skill-creator | 85 | clawhub | Create new skills |

## New Skill Workflow

```
User/Auto-detect finds skill
        ↓
   Security vetting
        ↓
   PENDING queue (5-10 days)
        ↓
   Waiting period
        ↓
   Auto-promoted ✓
```

## Update Workflow

```
Check detects new version
        ↓
   Trust ≥90? ──→ Immediate update
        ↓ No
   10-day delay
        ↓
   Auto-apply
```

## Advanced

- [Registry format](references/registry-format.md)
- [Trust calculation](references/trust-ratings.md)
- [Cron setup guide](references/cron-setup.md)

## Requirements

- Python 3.8+
- clawhub CLI installed
- skill-vetter (for security scanning)
- Cron (optional, for automation)

## License

MIT