---
name: tracebit-canaries
description: >
  Use when the user wants to protect their workspace from credential theft, prompt injection, or data exfiltration — even if they don't mention "canaries" or "honeytokens" directly. Covers deploying Tracebit security canary tokens (fake decoy credentials that alert on use), detecting when they're triggered via the user's pre-authorized email tool, and human-supervised incident response. Also use when investigating a suspected compromise, hardening an agent's environment, or setting up tripwires to catch unauthorized access to sensitive files.
metadata: {"openclaw":{"emoji":"🐦","homepage":"https://community.tracebit.com","primaryEnv":"TRACEBIT_API_TOKEN","requires":{"bins":["bash","python3","curl","jq","openclaw"]},"permissions":["email:read (via plugins.email — read-only search for Tracebit alert emails; requires user's pre-authorized email account)","messaging:send (via plugins.messaging — sends notifications to user's own channel only)","fs:write memory/security-incidents.md (append-only incident log during canary alert investigation)","fs:write /tmp/tracebit-setup-creds (temporary signup password with chmod 600; deleted after use)","fs:read memory/* (agent memory files during incident investigation; requires human confirmation before each read)"],"keywords":["canary","honeytokens","security","incident-response","credential-theft","prompt-injection","tripwire"]},"creator":{"org":"Tracebit","source":"https://github.com/tracebit-com/tracebit-community-cli"},"safety":{"posture":"human-gated-deployment","red_lines":["no-autonomous-writes-to-credential-locations","no-credential-exfiltration","no-messages-to-external-recipients","no-remediation-without-human-approval","no-checksum-bypass"],"runtime_constraints":{"all-access-requires-upfront-user-consent":true,"canary-deployment-requires-human-confirmation":true,"canary-rotation-requires-human-acknowledgement":true,"credential-files-written-only-by-cli-not-skill":true,"email-access-read-only":true,"email-and-messaging-require-upfront-consent":true,"memory-file-review-requires-human-confirmation":true,"investigation-read-only-except-append-only-incident-log":true,"notifications-to-user-channel-only":true,"signup-password-never-in-conversation-output":true,"sha256-verification-mandatory":true}}}
---

# Tracebit Canaries Skill

End-to-end security canary coverage — from signup to human-supervised incident response. You (the agent) perform setup steps yourself, with human confirmation at key decision points.

The Tracebit CLI runs a lightweight background service that refreshes canary token expiry — no other network calls or file access. When the heartbeat inbox check detects a canary alert email, you notify the human, investigate (read-only), and report.

Tracebit Community Edition is free at https://community.tracebit.com

---

## Security & Transparency

This skill is user-initiated, user-supervised, and fully reversible. For full details — including file traceability, enforcement model, and removal — see `references/security-compliance.md`.

**Skill file writes** (created by agent instructions in SKILL.md, not by shell scripts):
- `/tmp/tracebit-setup-creds` — temporary signup password (Step 1, chmod 600, deleted after use)
- `HEARTBEAT.md` — canary alert check block (Step 6, append)
- `memory/security-incidents.md` — incident log (playbook Phase 2.2, append-only, only on alert)

**CLI writes** — `tracebit deploy` places decoy tokens in standard credential locations, only after human confirmation. The CLI is [open-source](https://github.com/tracebit-com/tracebit-community-cli). No real credentials are read or modified.

**CLI installation** — SHA256-verified from official GitHub Releases only. No elevated privileges; macOS uses the standard system installer dialog.

**Email** — read-only search for Tracebit alerts via `plugins.email.accounts`. No emails sent, deleted, or modified.

**Memory reads** — `memory/*` files read during investigation only, gated on human confirmation (playbook Phase 2.4).

**Background service** — refreshes canary token expiry only. Runs as current user. Fully removable.

---

## Execution Principles

**You are the operator. The human is the owner.**

- **Confirm with the human** before: starting deployment, writing credentials to disk, and rotating/remediating after incidents.
- **Browser steps**: use the OpenClaw managed `browser` tool — verify availability first:
  ```bash
  openclaw browser --browser-profile openclaw status
  ```
- **Ask the human for**: 2FA codes, unreadable CAPTCHAs, or missing tool configuration

---

## Definition of Done

**Not done until every item is checked:**

```
[ ] Step 1: Tracebit account created — dashboard confirmed via browser snapshot
[ ] Step 2: CLI installed — `tracebit --version` returns a version
[ ] Step 3: CLI authenticated — `tracebit auth status` shows valid credentials
[ ] Step 4: All 5 canary types deployed
[ ] Step 5: `tracebit show` confirms all 5 active
[ ] Step 6: Heartbeat alert check block added to HEARTBEAT.md
```

Canaries without alert detection (Step 6) provide no protection. Do not skip it.

---

## Setup Steps

### Step 1: Sign Up

Use the `browser` tool — not any system-installed browser.

```
1. Get your email address from the configured email provider
2. Generate a strong random password (20+ chars, mixed case, digits, symbols) and write it to a temp file — never include it in conversation output:
   ```bash
   python3 -c "import secrets, string; chars = string.ascii_letters + string.digits + '!@#\$%^&*'; print(''.join(secrets.choice(chars) for _ in range(24)))" > /tmp/tracebit-setup-creds && chmod 600 /tmp/tracebit-setup-creds
   ```
   Tell the human the file path so they can retrieve it later.
3. browser navigate https://community.tracebit.com
4. browser snapshot — inspect the page
5. If a cookie consent banner appears, dismiss it before proceeding
6. Click "Sign up with email" (NOT "Sign in with Google" — avoids OAuth loops)
7. Type email and password into the form using refs from the snapshot
8. Submit — redirected to "Confirm your account" page
9. Retrieve confirmation code from inbox using your email provider's skill/tool
10. Type the code and submit
11. browser snapshot — confirm Tracebit dashboard loaded
```

**Error cases:**
- **Email already registered**: skip to Step 3
- **CAPTCHA**: `browser screenshot`, read it yourself, type it in. Ask human only if unreadable.
- **Code not arriving**: check spam folder, wait 20s, click "Resend code"

### Step 2: Install the CLI

```bash
bash scripts/install-tracebit.sh
```

Verify: `tracebit --version`

If the script fails, see `references/troubleshooting.md`. For manual installation, download the appropriate package from the [CLI releases page](https://github.com/tracebit-com/tracebit-community-cli/releases/latest):
- **Linux**: download `install-tracebit-linux` and run `bash install-tracebit-linux`
- **macOS arm64**: download `install-tracebit-osx-arm.pkg` and open it — the standard macOS installer dialog will guide the user through installation
- **macOS x64**: download `install-tracebit-osx-x64.pkg` and open it — the standard macOS installer dialog will guide the user through installation

### Step 3: Authenticate the CLI

`tracebit auth` starts a listener on `localhost:5442` and waits for an OAuth callback.

```bash
tracebit auth > /tmp/tracebit-auth.log 2>&1 &
TRACEBIT_PID=$!
sleep 3
cat /tmp/tracebit-auth.log
```

Then:
1. `browser navigate https://community.tracebit.com/cli-login`
2. `browser snapshot` — find the "Authorise" button
3. Click **Authorise** using the ref from the snapshot
4. Callback completes automatically — log shows `Successfully logged into Tracebit`

Verify: `tracebit auth status`

**Fallback** (if OAuth callback fails): `browser navigate https://community.tracebit.com` → Settings → API Keys → Create token → `tracebit auth --token`

### Step 4: Deploy All Canaries

```bash
tracebit deploy all      # ⚠️ will exit with an error on the username-password prompt — this is expected
tracebit deploy email    # email canary is NOT included in deploy all
```

The username-password credential is issued before the prompt fires. The error exit is a known CLI quirk. Just continue — `tracebit show` will confirm it's there.

Deploys 5 types: **aws**, **ssh**, **cookie**, **username-password**, **email**. See `references/canary-types.md` for details on each.

### Step 5: Verify Deployment

```bash
tracebit show
bash scripts/check-canaries.sh
```

All 5 types must appear active.

### Step 6: Configure Heartbeat Alert Detection

> **Not optional.** Without this, canaries fire silently.

Append to `HEARTBEAT.md` (create if needed):

```markdown
## Tracebit Canary Alert Check (every heartbeat, ~30 min)

Search (read-only) for new Tracebit canary alert emails since the last heartbeat.
Using your email provider's skill/tool, search for emails from `notifications@community.tracebit.com` with subject containing "Tracebit Canary Triggered" from the last hour. No emails are sent, deleted, or modified.

If any alert emails are found:
1. **Immediately notify the human via their configured messaging channel** — read `references/incident-response-playbook.md`
2. **Investigate** — follow the playbook phases
3. **Send a follow-up report** within 5 minutes
```

Also add this weekly check:

```markdown
## Tracebit Canary Health (weekly)
- Run: tracebit show
- If expired or missing: tracebit deploy all && tracebit deploy email
```

Use a 1-hour search window to avoid missing alerts across heartbeat timing jitter.

---

## Completion Report

Include verbatim when reporting to the human:

```
## Tracebit Canary Setup — Completion Report

[ ] Step 1 — Account: <confirmed / failed: reason>
[ ] Step 2 — CLI install: <tracebit version X.Y.Z / failed: reason>
[ ] Step 3 — Auth: <credentials valid / failed: reason>
[ ] Step 4 — Deploy: <5 canaries deployed / failed: reason>
[ ] Step 5 — Verify: <all active / issues: list>
[ ] Step 6 — Heartbeat: <HEARTBEAT.md updated / failed: reason>

Overall: COMPLETE ✅  /  INCOMPLETE ❌ (blocked on: <step>)

## Credentials
Tracebit account: <email address>
Tracebit password: saved to /tmp/tracebit-setup-creds (chmod 600)
⚠️ Store the password in your password manager, then delete the temp file.
⚠️ Change this password in Tracebit account settings.
```

**Password handling:** After generating the password, write it to a temp file — never include it in conversation output:
```bash
echo "<generated-password>" > /tmp/tracebit-setup-creds && chmod 600 /tmp/tracebit-setup-creds
```
Tell the human the file path and instruct them to save the password to their password manager, then delete the file.

---

## When a Canary Fires

Read and follow `references/incident-response-playbook.md` immediately. The playbook covers:
1. **Notify** the human via their configured messaging channel within seconds
2. **Investigate** — check canary status and log the incident (one append-only write to `memory/security-incidents.md`); reading memory files requires human confirmation
3. **Report** findings to the human within 5 minutes
4. **Rotate** canaries only **after human acknowledgement**: `tracebit deploy all && tracebit deploy email`

## Removal

To fully remove all Tracebit components, see `references/security-compliance.md` — includes a cleanup script and manual removal steps.

---

## Gotchas

- `tracebit deploy all` does **not** include the email canary — always run `tracebit deploy email` separately
- The **username-password canary** prompts "Have you saved this in your password manager? [y/n]" which fails non-interactively. The credential is issued before the prompt — check `tracebit show`. If missing: `tracebit deploy username-password --json-output`
- **Email canary tracking pixel**: opening/previewing the canary email fires the alert. This is by design — the email is the bait.
- **Canary credentials are fake** — never use them for real workloads
- **CLI token** stored at the standard Tracebit config location — do not expose in logs or shared contexts
- **Do not log canary credential values** — they become attack vectors if exposed

---

## Reference Files

| File | When to Read |
|------|-------------|
| `references/incident-response-playbook.md` | **When a canary fires** — full IR procedure |
| `references/canary-types.md` | Understanding each canary type and placement |
| `references/attack-patterns.md` | Real-world attacks canaries detect |
| `references/security-compliance.md` | Safety posture, credential handling, messaging rules, **full removal** |
| `references/api-reference.md` | **Only if CLI unavailable** — API fallback |
| `references/troubleshooting.md` | When something isn't working |
