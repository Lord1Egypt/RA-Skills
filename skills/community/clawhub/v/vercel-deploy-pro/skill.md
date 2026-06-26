---
name: vercel-deploy
description: Deploy to Vercel. Auto-activates for any Vercel task — editing a landing page, deploying, aliasing, updating a site.
---

# Skill: Vercel Deploy

## When to activate (automatically, without prompting)

- any mention of Vercel, landing page, or site on vercel.app
- task "update site", "deploy", "fix landing"
- editing an HTML file in a project folder with `.vercel/project.json`

---

## Auth flow (before anything else)

```bash
vercel whoami 2>&1
```

**Authorized → proceed.**

**Not authorized → one-time setup:**

→ In Claude Code (has a browser):
```bash
vercel login
```

→ In OpenClaw or any headless agent:
1. Tell the user:
   > "Open vercel.com/account/tokens → Create Token → copy it and send it here. You only need to do this once."
2. Once received, verify:
```bash
export VERCEL_TOKEN=<token>
vercel whoami
```
3. Store securely — do NOT write the token to `~/.zshrc` or any file. Keep it in env for this session only, or ask the user to add it to their secrets manager.

---

## Creating or editing HTML files

**CRITICAL: Never output HTML in the response text.**

Always write directly to a file using the Write/Edit tool:
- ✅ Write tool → `index.html` → deploy
- ❌ Print HTML in response → copy-paste → deploy

Reason: large HTML files exceed the 32k output token limit and Claude hangs mid-generation. Writing to a file has no such limit.

If the file is very large (>300 lines), build it in logical sections using Edit tool rather than rewriting from scratch.

---

## Pre-deploy checklist (required)

### 1. Make ALL changes first
❌ ANTI-PATTERN: deploy after each individual edit
✅ Rule: all edits in file first → one deploy

### 2. Check for `.vercel/project.json`

```bash
ls .vercel/project.json
```

**File exists → proceed to deploy.**

**File does not exist → first deploy, Vercel will create the project automatically:**
```bash
vercel deploy --yes --prod
# Vercel creates the project and .vercel/project.json on first run
```

### 3. Verify changes are actually in the file
```bash
grep -c "expected string" index.html
```

---

## Deploy recipe

```bash
# Deploy (run from project folder)
vercel deploy --yes --prod 2>&1 | grep -E "https://|Error"

# If custom alias was not assigned automatically — set it manually:
# For personal accounts (no --scope needed):
vercel alias set <deploy-url> <alias>.vercel.app

# For team accounts only:
vercel alias set <deploy-url> <alias>.vercel.app --scope YOUR_TEAM_SCOPE
```

Note: `script -q /dev/null` suppresses interactive prompts on macOS but breaks on Linux. Use plain `vercel deploy` instead — `--yes` flag handles prompts cross-platform.

### Post-deploy verification (required)
```bash
curl -s https://<alias>.vercel.app | grep "expected string"
# 200 + expected string = ✅ done
```

---

## Removing SSO (if site is locked behind auth)

```bash
PROJECT_ID=$(python3 -c "import json; print(json.load(open('.vercel/project.json'))['projectId'])")
TOKEN=$(python3 -c "import json; print(json.load(open('$HOME/Library/Application Support/com.vercel.cli/auth.json'))['token'])")

# For personal accounts:
curl -s -X PATCH "https://api.vercel.com/v9/projects/$PROJECT_ID" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"ssoProtection":null,"passwordProtection":null,"trustedIps":null}'

# For team accounts — add teamId:
curl -s -X PATCH "https://api.vercel.com/v9/projects/$PROJECT_ID?teamId=YOUR_TEAM_ID" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"ssoProtection":null,"passwordProtection":null,"trustedIps":null}'
```

---

## Final output (always)

After a successful deploy, the last message to the user must be the public URL — nothing else:

```
✅ https://<alias>.vercel.app
```

---

## ❌ Anti-patterns (from practice)

| What went wrong | How to do it right |
|---|---|
| Generated HTML in response text (hit 32k token limit) | Always write HTML directly to file using Write/Edit tool |
| Deployed from home directory (wrong CWD) | Always deploy from the project folder with `.vercel/project.json` |
| Multiple deploys for separate edits | All edits → one deploy |
| Didn't verify file actually changed before deploying | `grep` before deploying |
| Didn't verify after deploy | `curl` on the live URL after every deploy |
| Used `--scope` on a personal account | `--scope` is for team accounts only |
| Used `script -q /dev/null` on Linux | Use plain `vercel deploy --yes` instead |
| Stored token in `~/.zshrc` | Keep token in env only, never write to files |
| Started with partial understanding | Read source fully first, make a diff, then apply all edits |

## Gotchas
- `--name` is deprecated — don't use it
- `vercel project rm` doesn't support `--yes` — interactive only
- `vercelAuthentication` is NOT supported in API v9 — use `ssoProtection: null`
- After `vercel deploy --prod` the default alias is assigned automatically, custom alias is not (always verify)
- First deploy on a new project: no `.vercel/project.json` yet — just run `vercel deploy --yes --prod`, it creates the project automatically
