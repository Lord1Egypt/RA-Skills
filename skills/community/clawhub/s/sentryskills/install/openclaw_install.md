# Installing SentrySkills for OpenClaw

Install SentrySkills via ClawHub CLI for OpenClaw/Claude Code environments.

## Prerequisites

- Node.js and npm
- OpenClaw or Claude Code

## Installation

### Step 1: Install ClawHub CLI

```bash
npm i -g clawhub
clawhub --version
```

### Step 2: Search and Install SentrySkills

```bash
# Search for SentrySkills
clawhub search "sentry skills security"

# Install SentrySkills
clawhub install sentryskills
```

By default, ClawHub installs skills to `./skills/` in your current working directory.

If you have configured an OpenClaw workspace, ClawHub will use that workspace location unless you override it with `--workdir` or the `CLAWHUB_WORKDIR` environment variable.

### Step 3: Restart OpenClaw

```bash
# Start a new session
openclaw chat
```

The skill will be automatically loaded in the new session.

## Enable Automatic Protection (Recommended)

After installation, configure SentrySkills to run automatically on every task:

### One-Command Setup

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
python ./skills/sentry-skills/shared/scripts/self_guard_runtime_hook_template.py input.json --policy-profile balanced --out result.json
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

Or copy the template:
```bash
cp ./skills/sentry-skills/AGENTS.md.template ~/.codex/AGENTS.md
```

### Step 4: Restart Again

Restart OpenClaw once more after adding AGENTS.md. SentrySkills will now protect every task!

## Installation Location

Default installation path: `./skills/sentry-skills/`

OpenClaw loads skills from: `<workspace>/skills/`

## Verify Installation

```bash
# Check skill directory
ls -la ./skills/sentry-skills/

# Verify main skill file
cat ./skills/sentry-skills/SKILL.md
```

## Updating

```bash
clawhub update sentryskills
```

Or reinstall:
```bash
clawhub install sentryskills --force
```

## Uninstalling

```bash
clawhub uninstall sentryskills
```

Optionally remove AGENTS.md configuration:
```bash
rm ~/.codex/AGENTS.md
```

## What SentrySkills Protects Against

When active, SentrySkills provides:
- **Preflight checks** - Detects threats before execution
- **Runtime monitoring** - Watches behavior during execution
- **Output guards** - Redacts sensitive data in responses
- **Predictive analysis** - Anticipates potential risks

All with **zero external dependencies** (100% Python standard library).

## Troubleshooting

### ClawHub command not found

Ensure npm global bin is in your PATH:
```bash
npm config get prefix
# Add <prefix>/bin to your PATH
```

### Skill not loading after installation

1. Verify the skill directory exists:
   ```bash
   ls -la ./skills/sentry-skills/
   ```

2. Check SKILL.md is present:
   ```bash
   cat ./skills/sentry-skills/SKILL.md
   ```

3. Restart OpenClaw completely

### Automatic mode not working

If SentrySkills doesn't run automatically:

1. Verify AGENTS.md exists:
   ```bash
   cat ~/.codex/AGENTS.md
   ```

2. Check the path to the runtime hook is correct:
   ```bash
   python ./skills/sentry-skills/shared/scripts/self_guard_runtime_hook_template.py --help
   ```

3. Restart OpenClaw again

## Manual Mode

If you didn't configure AGENTS.md, you can manually invoke SentrySkills:

```
/skills use sentry-skills
```

Then proceed with your task. SentrySkills will run once for that session.

**⚠️ Recommendation:** Use Automatic Mode for consistent protection.

## Package Contents

The skill package includes:
- **using-sentry-skills** - User-facing entry point
- **sentry-skills-orchestrator** - Central coordination
- **sentry-skills-preflight** - Pre-execution checks
- **sentry-skills-runtime** - Runtime monitoring
- **sentry-skills-output** - Output validation & redaction
- **shared/** - Core Python modules and configurations

All with **zero external dependencies** (Python stdlib only).
