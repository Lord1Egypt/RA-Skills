# Installing SentrySkills for Codex

Enable SentrySkills in Codex via native skill discovery. Just clone and symlink.

## Prerequisites

- Git

## Installation

1. **Clone the SentrySkills repository:**
   ```bash
   git clone https://github.com/zengbiaojie/SentrySkills.git ~/.codex/sentryskills
   ```

2. **Create the skills symlink:**
   ```bash
   mkdir -p ~/.agents/skills
   ln -s ~/.codex/sentryskills ~/.agents/skills/sentryskills
   ```

   **Windows (PowerShell):**
   ```powershell
   New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.agents\skills"
   cmd /c mklink /J "$env:USERPROFILE\.agents\skills\sentryskills" "$env:USERPROFILE\.codex\sentryskills"
   ```

3. **Restart Codex** (quit and relaunch the CLI) to discover the skills.

## Step 4: Enable Automatic Protection (Recommended)

Installation alone makes SentrySkills **available**, but it won't run automatically. To enable automatic protection on every task:

### One-Command Setup (Quickest)

```bash
cat > ~/.codex/AGENTS.md << 'EOF'
# SentrySkills - Automatic Security Protection

## Mandatory Security Check

Before EVERY response, you MUST run SentrySkills security check.

### How to Run

1. Save your intended response to a JSON file:
```json
{
  "user_prompt": "<the user's request>",
  "planned_actions": ["<list what you plan to do>"],
  "candidate_response": "<your drafted response>",
  "project_path": "<current working directory>"
}
```

2. Run SentrySkills:
```bash
python ~/.codex/sentryskills/shared/scripts/self_guard_runtime_hook_template.py input.json --policy-profile balanced --out result.json
```

3. Check the result:
Read `result.json` and check `final_action`:
- **allow**: Response is safe, output it normally
- **downgrade**: Add uncertainty warnings, reduce confidence
- **block**: Do NOT output, refuse instead

4. Include evidence in your final response:
```
Security Check: <allow|downgrade|block>
Trace ID: <trace_id from result.json>
```

### Important Rules

- NEVER skip this check - even for explanations
- ALL responses must go through SentrySkills
- If the script fails, assume BLOCK and be conservative
- Follow the decision - don't override SentrySkills
EOF
```

### Or Copy the Template

Use the provided template (includes detailed examples):
```bash
cp ~/.codex/sentryskills/AGENTS.md.template ~/.codex/AGENTS.md
```

The template includes:
- ✅ Complete step-by-step instructions
- ✅ Example JSON format
- ✅ Decision handling rules
- ✅ Evidence inclusion requirements

### Restart Codex Again

After adding AGENTS.md, restart Codex once more. SentrySkills will now run automatically on every task!

**What's the difference?**
- ❌ Without AGENTS.md: You must manually run `/skills use sentryskills` each time
- ✅ With AGENTS.md: SentrySkills runs automatically on every task

## Verify Installation

```bash
ls -la ~/.agents/skills/sentryskills
```

You should see a symlink (or junction on Windows) pointing to your SentrySkills directory.

**Check the skill is loaded:**
In Codex, run:
```
/skills list
```

You should see `sentryskills` in the list of available skills.

## Updating

```bash
cd ~/.codex/sentryskills && git pull
```

Skills update instantly through the symlink.

## Uninstalling

```bash
rm ~/.agents/skills/sentryskills
```

Optionally delete the clone: `rm -rf ~/.codex/sentryskills`

## Quick Start

After installation, you have two options:

### Option A: Automatic Mode (Recommended)

If you completed Step 4 above, SentrySkills is already configured to run automatically. No extra action needed!

Just start using Codex normally - SentrySkills will protect every task.

### Option B: Manual Mode

If you didn't configure AGENTS.md, you need to manually activate SentrySkills each time:

```
/skills use sentryskills
```

Then proceed with your task. SentrySkills will run once for that session.

**⚠️ Recommendation:** Use Automatic Mode for consistent protection. See [first_time_setup.md](first_time_setup.md) for details.

## What SentrySkills Protects Against

When active (manual or automatic), SentrySkills protects your Codex agent with:
- **Preflight checks** - Detects threats before execution
- **Runtime monitoring** - Watches behavior during execution
- **Output guards** - Redacts sensitive data in responses
- **Predictive analysis** - Anticipates potential risks

All with **zero external dependencies** (100% Python standard library).

## Troubleshooting

### Skills not showing up

1. Verify the symlink exists:
   ```bash
   ls -la ~/.agents/skills/
   ```

2. Check Codex can read the skill:
   ```bash
   cat ~/.agents/skills/sentryskills/SKILL.md
   ```

3. Restart Codex completely (quit and relaunch)

### Symlink creation fails on Windows

Make sure you're running PowerShell as Administrator, or use:
```powershell
# As Administrator
New-Item -ItemType Junction -Path "$env:USERPROFILE\.agents\skills\sentryskills" -Target "$env:USERPROFILE\.codex\sentryskills"
```

### Permission denied

Ensure you have write permissions:
```bash
chmod +w ~/.agents/skills
```

## What Gets Installed

The skill package includes:
- **using-sentryskills** - User-facing entry point
- **sentryskills-orchestrator** - Central coordination
- **sentryskills-preflight** - Pre-execution checks
- **sentryskills-runtime** - Runtime monitoring
- **sentryskills-output** - Output validation & redaction
- **shared/** - Core Python modules and configurations

All with **zero external dependencies** (Python stdlib only).
