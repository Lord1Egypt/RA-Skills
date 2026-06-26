---
name: tool-connector
description: Connect OpenClaw to tools like Slack, GitHub, Jira, Confluence, Grafana, Datadog, PagerDuty, Outlook, and Google Drive with minimal input — just paste a URL and the skill figures out the rest. Everything stays local; no credentials or data leave your machine. Uses your own identity (no OAuth apps, no IT tickets). Also teaches how to add brand-new tool connections from scratch (10xProductivity methodology). Use when the user wants to connect to a tool, set up credentials, access a service API, add a new integration, or ask "how do I give my agent access to X". CAUTION: SSO tools use Python Playwright browser automation to capture session tokens from a headed Chromium window; credentials are stored in ~/.openclaw/openclaw.json under skills.entries.tool-connector only. Review scripts/playwright_sso.py and scripts/openclaw_sync.py before use.
metadata:
  {
    "openclaw":
      {
        "emoji": "🔌",
        "requires": { "bins": ["python3", "pip"] },
        "install":
          [
            {
              "id": "python-playwright",
              "kind": "pip",
              "package": "playwright",
              "post_install": "playwright install chromium",
              "label": "Install Python Playwright + Chromium (required for SSO tools: Slack, Outlook, Teams, Google Drive, Grafana)"
            }
          ],
        "env":
          {
            "provided":
              [
                { "key": "GITHUB_TOKEN",        "tool": "GitHub",             "kind": "api-token",   "lifetime": "long-lived" },
                { "key": "JIRA_API_TOKEN",       "tool": "Jira",               "kind": "api-token",   "lifetime": "long-lived" },
                { "key": "JIRA_EMAIL",           "tool": "Jira",               "kind": "config",      "lifetime": "permanent"  },
                { "key": "CONFLUENCE_TOKEN",     "tool": "Confluence",         "kind": "api-token",   "lifetime": "long-lived" },
                { "key": "CONFLUENCE_EMAIL",     "tool": "Confluence",         "kind": "config",      "lifetime": "permanent"  },
                { "key": "DATADOG_API_KEY",      "tool": "Datadog",            "kind": "api-token",   "lifetime": "long-lived" },
                { "key": "PAGERDUTY_TOKEN",      "tool": "PagerDuty",          "kind": "api-token",   "lifetime": "long-lived" },
                { "key": "JENKINS_API_TOKEN",    "tool": "Jenkins",            "kind": "api-token",   "lifetime": "long-lived" },
                { "key": "ARTIFACTORY_TOKEN",    "tool": "Artifactory",        "kind": "api-token",   "lifetime": "long-lived" },
                { "key": "BACKSTAGE_TOKEN",      "tool": "Backstage",          "kind": "api-token",   "lifetime": "long-lived" },
                { "key": "BITBUCKET_TOKEN",      "tool": "Bitbucket Server",   "kind": "api-token",   "lifetime": "long-lived" },
                { "key": "GRAFANA_SESSION",      "tool": "Grafana",            "kind": "sso-cookie",  "lifetime": "~8h"        },
                { "key": "SLACK_XOXC",           "tool": "Slack",              "kind": "sso-token",   "lifetime": "~8h"        },
                { "key": "SLACK_D_COOKIE",       "tool": "Slack",              "kind": "sso-cookie",  "lifetime": "~8h"        },
                { "key": "GDRIVE_COOKIES",       "tool": "Google Drive",       "kind": "sso-cookies", "lifetime": "days-weeks" },
                { "key": "GDRIVE_SAPISID",       "tool": "Google Drive",       "kind": "sso-token",   "lifetime": "days-weeks" },
                { "key": "TEAMS_SKYPETOKEN",     "tool": "Microsoft Teams",    "kind": "sso-token",   "lifetime": "~24h"       },
                { "key": "TEAMS_SESSION_ID",     "tool": "Microsoft Teams",    "kind": "sso-session", "lifetime": "~24h"       },
                { "key": "GRAPH_ACCESS_TOKEN",   "tool": "Outlook / M365",     "kind": "bearer-jwt",  "lifetime": "~1h"        },
                { "key": "OWA_ACCESS_TOKEN",     "tool": "Outlook / M365",     "kind": "bearer-jwt",  "lifetime": "~1h"        }
              ]
          }
      }
  }
---

# Tool Connector

> **Everything stays local — no data leaves your machine.** Credentials are written only to `~/.openclaw/openclaw.json` on your own filesystem. Nothing is uploaded, proxied, or shared with any cloud service, including OpenClaw's servers. The agent connects directly from your machine to the target tool using your own identity.
>
> **Minimal input by design.** Just paste a URL from the tool — the skill infers the base URL, auth method, and API shape from it. No IT tickets, no OAuth app registration, no config files to hand-edit.
>
> **SSO tools** (Slack, Outlook, Teams, Google Drive, Grafana) use **Python Playwright** (`pip install playwright && playwright install chromium`) to open a headed Chromium window you can see, completing SSO the same way you would manually. The script captures session cookies/tokens from `localStorage` and network headers. **Review `{baseDir}/scripts/shared_utils/playwright_sso.py` before running any SSO flow.**
>
> **Credential storage scope:** All credentials are written into `~/.openclaw/openclaw.json` under `skills.entries.tool-connector.env` **only** — the sync script does not read or modify any other key in that file. SSO tokens are also cached in `~/.openclaw/tool-connector.env` (plain-text, never committed to git). OpenClaw injects them as env vars at the start of each agent session; only store tokens for tools you actively use.
>
> **Full list of credentials this skill may store** (see `metadata.env.provided` above for tool, kind, and lifetime):
> API tokens (long-lived): `GITHUB_TOKEN`, `JIRA_API_TOKEN`, `CONFLUENCE_TOKEN`, `DATADOG_API_KEY`, `PAGERDUTY_TOKEN`, `JENKINS_API_TOKEN`, `ARTIFACTORY_TOKEN`, `BACKSTAGE_TOKEN`, `BITBUCKET_TOKEN`
> SSO tokens (short-lived, refreshed by Playwright): `GRAFANA_SESSION` (~8h), `SLACK_XOXC`/`SLACK_D_COOKIE` (~8h), `GDRIVE_COOKIES`/`GDRIVE_SAPISID` (days–weeks), `TEAMS_SKYPETOKEN`/`TEAMS_SESSION_ID` (~24h), `GRAPH_ACCESS_TOKEN`/`OWA_ACCESS_TOKEN` (~1h)

Gives your OpenClaw agent the ability to connect to tools and services using the [10xProductivity](https://github.com/ZhixiangLuo/10xProductivity) methodology: your agent authenticates *as you*, using the same surfaces you use as a human — no OAuth apps, no cloud middleware, no IT tickets.

## Bundled tool recipes

Verified connection recipes are in `{baseDir}/references/tool_connections/`:

| Tool | Auth method | Reference |
|------|-------------|-----------|
| Artifactory | API token | `tool_connections/artifactory/` |
| Backstage | API token | `tool_connections/backstage/` |
| Bitbucket Server | API token | `tool_connections/bitbucket-server/` |
| Confluence | API token | `tool_connections/confluence/` |
| Datadog | API token | `tool_connections/datadog/` |
| GitHub | API token | `tool_connections/github/` |
| Google Drive | SSO (Playwright) | `tool_connections/google-drive/` |
| Grafana | API token / SSO | `tool_connections/grafana/` |
| Jenkins | API token | `tool_connections/jenkins/` |
| Jira | API token | `tool_connections/jira/` |
| Microsoft Teams | SSO (Playwright) | `tool_connections/microsoft-teams/` |
| Outlook | SSO (Playwright) | `tool_connections/outlook/` |
| PagerDuty | API token | `tool_connections/pagerduty/` |
| Slack | SSO (Playwright) | `tool_connections/slack/` |

For more tools, clone https://github.com/ZhixiangLuo/10xProductivity and run through `setup.md`.

## Which reference to read

**Setting up a connection to a tool already in the list above:**
Read `{baseDir}/references/setup.md` for UX principles, then read the matching `{baseDir}/references/tool_connections/<tool>/setup.md` and `connection-*.md`.

**Adding a brand-new tool not in the list:**
Read `{baseDir}/references/add-new-tool.md` — it walks through the full methodology: research auth, identify base URL, capture credentials, validate against a live instance, and write a reusable recipe.

**SSO-based tools (Slack, Outlook, Google Drive, Teams, Grafana):**
These use **Python Playwright** to open a headed Chromium window, capture a session token, and write it to `~/.openclaw/tool-connector.env`. The script is at `{baseDir}/scripts/shared_utils/playwright_sso.py`. Install once with `pip install playwright && playwright install chromium`; run when a token expires. Session lifetimes vary by tool (see the caution block above).

## Credential storage (OpenClaw standard)

All credentials — both API tokens and SSO session tokens — are stored in `~/.openclaw/openclaw.json` under `skills.entries.tool-connector.env`. OpenClaw injects them automatically as environment variables at the start of each agent run. No manual `source .env` needed.

**API tokens** (long-lived) — add directly to `~/.openclaw/openclaw.json`:

```json5
// ~/.openclaw/openclaw.json
{
  skills: {
    entries: {
      "tool-connector": {
        env: {
          GITHUB_TOKEN: "ghp_...",
          JIRA_API_TOKEN: "...",
          JIRA_EMAIL: "you@example.com",
        }
      }
    }
  }
}
```

**SSO session tokens** (short-lived: Slack ~8h, M365 ~1h, Teams ~24h) — captured by Playwright and synced automatically into `~/.openclaw/openclaw.json` via the sync script:

```bash
# Refresh Slack SSO and sync into openclaw.json
python3 {baseDir}/scripts/openclaw_sync.py --refresh-slack

# Refresh Outlook/M365 SSO and sync
python3 {baseDir}/scripts/openclaw_sync.py --refresh-outlook

# Refresh all SSO sessions and sync
python3 {baseDir}/scripts/openclaw_sync.py --refresh-all

# Sync already-captured tokens (no browser) — useful after manual SSO run
python3 {baseDir}/scripts/openclaw_sync.py
```

SSO tokens are cached in `~/.openclaw/tool-connector.env` (never in git). The sync script reads that file and patches `~/.openclaw/openclaw.json` so OpenClaw picks them up on the next session.

**Never store credentials in the skill directory itself.**

## Core principles (from 10xProductivity)

- **Ask for a URL first** — any link from the tool reveals the base URL, variant, and proves access
- **Infer auth from the URL** — do not ask the user to explain their auth setup
- **Run before you write** — every snippet must be code you actually executed against a live instance
- **Zero friction** — no OAuth app creation, no IT tickets, no new cloud services
- **Agent acts as you** — your identity, your audit trail, your credentials
