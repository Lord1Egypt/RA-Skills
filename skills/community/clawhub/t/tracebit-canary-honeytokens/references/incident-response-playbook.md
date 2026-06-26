# Incident Response Playbook — Tracebit Canary Alert

This playbook is triggered when the heartbeat inbox check detects a Tracebit canary alert email. The agent follows this procedure immediately upon detection.

**Human-in-the-loop**: the agent notifies the human immediately (Phase 1), then performs a scoped investigation (Phase 2 — reading canary status and logging the incident), and reports findings (Phase 3). **Phase 4 (canary rotation) requires human acknowledgement before proceeding** — the human may want to preserve the current state for further analysis.

**Phase 2 contains one write operation**: appending a structured incident entry to `memory/security-incidents.md`. All other operations are read-only. Reading memory files (which may contain sensitive agent context) is scoped to recent entries and limited to assessing whether the canary trigger correlates with recent agent activity.

**Speed matters.** The human should hear from you within seconds of the alert arriving. Don't wait for investigation to complete before sending the initial notification.

---

## Phase 1: Immediate Notification (within seconds)

**Before investigating, notify the human.**

Send to the human via their configured messaging channel (the one they set up in OpenClaw before activating this skill — do NOT send to any other channel or recipient):

```
🚨 TRACEBIT CANARY ALERT

A [type] canary was triggered at [time].
Canary name: [name]

I'm investigating now. Stand by for a full report.
```

How to fill in `[type]` and `[name]`:
- Parse the alert email with `scripts/parse-tracebit-alert.sh`
- Or read the subject/body directly: Tracebit alerts typically contain the canary name and type

If you can't determine the type yet, send: *"A Tracebit canary was triggered. Investigating now."*

Do not wait for the investigation to finish before sending this. The human needs to know immediately.

---

## Phase 2: Investigation (1–5 minutes)

> **All operations in this phase are read-only except 2.2 (incident logging).** The agent reads canary status and recent memory files to assess the alert, and appends a structured incident entry to `memory/security-incidents.md`. No credentials are used, and no external calls are made (except `tracebit show` which queries the Tracebit API for canary status). Reading memory files is limited to assessing correlation with recent agent activity — the agent does not extract or forward sensitive content from memory.

### 2.1 Parse the Alert

Run the alert parser:
```bash
echo "$ALERT_EMAIL_BODY" | bash skills/tracebit-canaries/scripts/parse-tracebit-alert.sh
```

Extract:
- **Canary type** (aws / ssh / cookie / username-password / email)
- **Canary name** (the label you gave it)
- **Trigger time** (when it was used)
- **Source IP** (where the use came from, if available)
- **AWS-specific fields** (action, region, key ID — for AWS canaries)

### 2.2 Log the Incident

Append to `memory/security-incidents.md` (create if it doesn't exist):

```markdown
## [ISO timestamp] — [canary_type] canary alert

- **Canary:** [name]
- **Type:** [type]
- **Triggered at:** [time]
- **Source IP:** [ip or "unknown"]
- **Alert received:** [when the email arrived]
- **Status:** Investigating
```

### 2.3 Check Current Canary Status

```bash
tracebit show
```

Note: Are other canaries still active? Have any been removed or replaced since deployment?

### 2.4 Assess Context

> **This step reads recent memory files, which may contain sensitive agent context.** Before reading memory files, confirm with the human:
> *"To investigate this alert, I need to review recent memory files for suspicious activity patterns. These may contain sensitive context from recent agent sessions. May I proceed?"*
> If the human declines, skip to 2.6 and note "Context assessment skipped — human declined memory review" in the report.

If confirmed, answer these questions:
1. **What was the agent processing when this canary was deployed?** Check recent memory files for context from around the deployment date.
2. **Was the agent recently processing external content** (web pages, files, emails, tool outputs) that could have contained the canary credential?
3. **Did the agent recently make any unexpected outbound requests?** Check recent tool calls in memory.
4. **Were any credentials recently written to files or passed to external tools?**

Do not extract or forward sensitive content from memory files — only note whether suspicious patterns are present.

### 2.5 Scan for Related Indicators

Check recent activity for suspicious patterns (requires same human confirmation as 2.4):
- Unexpected AWS API calls
- SSH connection attempts
- Emails sent to unknown addresses
- Outbound HTTP requests to unusual domains
- Memory files containing credential-format strings
- Tool calls that accessed credential storage locations

Check recent memory files:
```bash
ls -lt memory/ | head -10
# Read the most recent 2-3 daily files for suspicious activity
```

### 2.6 Assess Severity

| Severity | Criteria |
|----------|----------|
| **CRITICAL** | Source IP is external; AWS action shows data access; multiple canaries triggered |
| **HIGH** | Source IP is external; single canary triggered; suspicious context found |
| **MEDIUM** | Source IP is local/internal; or timing suggests accidental use |
| **LOW** | Test trigger via `tracebit trigger`; no suspicious context found |

> **Default to HIGH** if uncertain. False positives are cheap; missed incidents are not.

---

## Phase 3: Report to Human (follow-up message)

Send a structured report via the same messaging channel used in Phase 1. This should arrive **within 5 minutes** of the initial notification.

```
📋 CANARY ALERT INVESTIGATION REPORT

Alert: [type] canary "[name]" triggered at [time]
Severity: [CRITICAL / HIGH / MEDIUM / LOW]
Source IP: [ip address or "not available in alert"]

What happened:
[1-3 sentence description: what type of canary fired, what that means, 
when it happened]

Context assessment:
[What was the agent processing when this canary was accessible? 
Was it handling external content? Any known recent activity that could explain this?]

Related indicators found:
[List any suspicious patterns found in Phase 2.5, or "None found in recent activity"]

What this attack vector suggests:
[Based on the canary type — see references/attack-patterns.md for detail]
- AWS canary: credential theft from disk, env vars, or context; possibly prompt injection
- SSH canary: SSH key enumeration or exfiltration
- Cookie canary: browser session hijacking attempt
- Password canary: credential harvesting from files or password manager
- Email canary: outbound email exfiltration; possibly prompt injection causing email send

Recommended actions:
1. [Most urgent action — usually: rotate real credentials for the same type]
2. [Second action — usually: review recent agent activity for the attack vector]
3. [Third action — e.g.: check if other systems share similar credentials]

Canary rotation:
[Fresh canaries have been deployed (tracebit deploy all ran) / 
OR: Recommend running: tracebit deploy all]
```

---

## Phase 4: Rotate Canaries (after human acknowledgement)

**Wait for the human to acknowledge the Phase 3 report before rotating canaries.** The human may want to preserve the current state for further investigation, or may want to take other actions first.

Once the human confirms, redeploy:

```bash
tracebit deploy all
```

Why: The triggered canary may now be known to the attacker. Fresh canaries restore detection coverage. The old credentials are no longer useful as sensors — they've served their purpose.

If `tracebit deploy all` fails or the CLI is unavailable, note it in the incident log and recommend the human run it manually.

---

## Phase 5: Update Incident Log

Update the incident entry in `memory/security-incidents.md`:

```markdown
- **Status:** Investigated
- **Severity:** [assessed severity]
- **Report sent:** [timestamp]
- **Canaries rotated:** [yes / pending]
- **Notes:** [any additional context]
```

---

## Canary Type → Attack Vector Quick Reference

| Canary Type | What it means when triggered |
|-------------|------------------------------|
| **aws** | AWS credentials were read and used. Likely: credential harvesting from the standard AWS credentials location or `.env`, or prompt injection that caused an AWS API call. |
| **ssh** | SSH private key was read and used to attempt a connection. Likely: SSH key enumeration or exfiltration from the standard SSH key directory. |
| **cookie** | A browser session cookie was submitted to a service. Likely: browser session hijacking, or agent submitted a cookie from context. |
| **username-password** | Login credentials were used. Likely: credential harvesting from password manager, `.env`, or agent memory. |
| **email** | An email was sent to the canary address. Likely: prompt injection that caused the agent to send email to an attacker-controlled address, or data exfiltration via email. |

For deeper analysis, read `references/attack-patterns.md`.

---

## Response Time Targets

| Phase | Target |
|-------|--------|
| Phase 1: Initial notification | Within 30 seconds of alert email arriving |
| Phase 2: Investigation complete | Within 5 minutes |
| Phase 3: Report sent | Within 5 minutes of alert |
| Phase 4: Canaries rotated | Within 10 minutes of alert |
