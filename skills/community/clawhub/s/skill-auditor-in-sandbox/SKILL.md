---
name: skill-auditor-in-sandbox
description: "Launch a NovitaClaw (OpenClaw) sandbox, install a specified skill, and generate an installation & security audit report. Use when: (1) You want to test a community skill before installing it locally, (2) You need a security audit of a skill's code, hooks, and dependencies, (3) You want to verify a skill from ClawHub or GitHub in an isolated environment."
argument-hint: "<skill-name>"
metadata:
  source: https://github.com/freecodewu/skill-auditor-in-sandbox
  homepage: https://github.com/freecodewu/skill-auditor-in-sandbox
---

# Skill Auditor in Sandbox

Test and audit Claude Code skills in an isolated [NovitaClaw](https://novita.ai/docs/guides/novitaclaw) (OpenClaw) sandbox before installing them locally. The skill launches a sandbox, installs the target skill, runs a security scan, and generates a structured risk report.

## Quick Reference

| Situation | Action |
|-----------|--------|
| Test a ClawHub skill | `/skill-auditor-in-sandbox owner/skill-name` |
| Test a GitHub skill | `/skill-auditor-in-sandbox owner/repo-name` |
| Review the report | Check risk level, suspicious patterns, URLs, external paths |
| After review | Pause or stop the sandbox to save costs |

## Prerequisites

- `NOVITA_API_KEY` must be set. If not, ask the user to register at https://novita.ai/?utm_source=OpenClaw&utm_medium=Dev_Rel&utm_campaign=Claw-30 and get an API key from https://novita.ai/settings/key-management, then:
  `export NOVITA_API_KEY=<key>`
- `novitaclaw` CLI must be installed. If not found:
  `curl -fsSL https://novitaclaw.novita.ai/install.sh | bash`
- `novita-sandbox` npm package must be available. If not:
  `npm install novita-sandbox`

## Usage

You are given a skill name (or identifier) as `$ARGUMENTS`. Your job is to launch a sandbox, install the skill, run a security audit, and generate a report.

### Step 1: Launch Sandbox

```bash
novitaclaw launch --json
```

Parse the JSON output and extract `sandbox_id` and `webui`. Save these for the report.

If launch fails, check `error_code` and `remediation` fields:
- `MISSING_API_KEY` → ask user for API key
- `SANDBOX_TIMEOUT` → retry with `--timeout 300`

### Step 2: Install Skill

Run the install script from the project root:

```bash
SANDBOX_ID=<sandbox_id> SKILL_NAME="$ARGUMENTS" node scripts/install-skill.mjs
```

The script outputs JSON: `{ success, method, skillDir, files, error? }`.
- If `success` is false, show the error and stop.
- Note the `method` used (clawhub / git-github / git-clawhub) for the report.

### Step 3: Security Audit

Run the audit script:

```bash
SANDBOX_ID=<sandbox_id> SKILL_NAME="$ARGUMENTS" node scripts/audit-skill.mjs
```

The script outputs JSON:
- `suspicious[]` — lines matching risky code patterns (dynamic execution, shell spawning, encoding, etc.)
- `urls[]` — all URL references found in skill files
- `externalPaths[]` — references to paths outside the skill directory (system dirs, dotfiles, temp dirs)
- `dependencies` — contents of requirements.txt or package.json if present
- `fileContents[]` — full contents of all text files for manual review

### Step 4: Assess Risk

Based on audit results, assign a risk level:

| Risk Level | Criteria |
|------------|----------|
| LOW | No suspicious patterns, URLs are legitimate (GitHub, docs), no external paths |
| MEDIUM | Some suspicious patterns but explainable (e.g., `fetch()` for legitimate API calls) |
| HIGH | Unexplained network calls, access to sensitive paths, obfuscated code |
| CRITICAL | Credential harvesting, mining indicators, command injection patterns |

### Step 5: Generate Report

Output a structured report:

```
## Skill Installation Report

**Skill:** <skill-name>
**Sandbox ID:** <sandbox_id>
**Web UI:** <webui_url>
**Timestamp:** <current time>

### Installation Status
- **Result:** SUCCESS / FAILED
- **Method:** <clawhub / git-github / git-clawhub>
- **Files Installed:** <count> files

### Installed Files
<table of files and their purpose>

### Security Analysis
- **Risk Level:** LOW / MEDIUM / HIGH / CRITICAL

### Suspicious Patterns Found
| File | Line | Pattern | Severity |
|------|------|---------|----------|
(or "None found")

### URL References
| File | URL | Context |
|------|-----|---------|
(list all URLs and whether they look legitimate)

### External Path References
(list any, or "None found")

### Dependencies
(list any, or "No external dependencies")

### Recommendations
- <recommendation based on findings>

### Sandbox Management
- To access: <webui_url>
- To pause (save costs): `novitaclaw pause <sandbox_id>`
- To stop (permanent): `novitaclaw stop <sandbox_id>`
```

After generating the report, automatically pause the sandbox to save costs:

```bash
novitaclaw pause <sandbox_id> --json
```

Then inform the user that the sandbox has been paused and can be resumed or stopped:
- To resume: `novitaclaw resume <sandbox_id>`
- To stop (permanent): `novitaclaw stop <sandbox_id>`

## What Gets Scanned

| Category | Patterns |
|----------|----------|
| Suspicious code | Shell spawning, dynamic code execution, encoding functions, mining indicators |
| Network calls | All URL references found in skill files |
| External paths | System directories, user home dotfiles, temp directories |
| Dependencies | `requirements.txt`, `package.json` |
| File contents | Full text of all `.md`, `.txt`, `.json`, `.py`, `.js`, `.ts`, `.sh`, `.yaml`, `.yml` files |

## Important Notes

- Always use `--json` flag with novitaclaw commands.
- The sandbox auto-terminates based on `keep_alive`. Suggest pause to save costs.
- Prefer `pause` over `stop` — stop is irreversible. Confirm before stopping.

## Attribution

- Source: https://github.com/freecodewu/skill-auditor-in-sandbox
- Powered by [NovitaClaw](https://novita.ai/docs/guides/novitaclaw) sandbox infrastructure
