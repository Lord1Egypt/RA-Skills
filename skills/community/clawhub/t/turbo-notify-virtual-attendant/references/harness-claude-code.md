# Claude Code

Claude Code can run the attendant two ways: **unattended** (a program in a terminal, no model while nothing arrives) or **in session** (you stay in Claude Code and it polls on a loop). Unattended is the one to recommend for a business that wants answers around the clock.

## Install and keep it current

```
claude plugin marketplace add turbo-notify/agent-skills#v1
claude plugin install turbo-notify@turbo-notify
```

`#v1` keeps you on the 1.x line: a change that breaks things (2.0) never arrives by itself. Third-party marketplaces do not update on their own. Turn it on in `/plugin`, tab **Marketplaces**, **Enable auto-update**, or pre-register the marketplace with `autoUpdate` set to true in the settings. Without it, the cycle tells the administrators when a new version exists and gives the two commands ([update.md](update.md)).

## Connect Turbo Notify

- To sign in with your account: the plugin already declares the server, so type `/mcp`, pick `turbo-notify` and sign in. A server you added by hand with the same name or address keeps priority over the plugin's. Without the plugin (a copy of the skill alone): `claude mcp add --transport http turbo-notify https://mcp.turbonotify.com` and then `/mcp`.
- For anything that runs alone, use an API key made with the **AI agent (MCP)** template (the dashboard page "API Keys"). The key is a company-wide credential: treat it as a password.

## Unattended (recommended)

The runner polls the Turbo Notify API with the key, and starts a fresh `claude -p` process only when there is something to do. A customer's process has no tools at all and no access to your files, your instructions or the key.

```
export TURBO_NOTIFY_API_KEY=tn_live_…
export TN_ASSIST_BASE=~/.turbo-notify/attendant TN_ASSIST_ORG=org_… TN_ASSIST_NUMBER=num_…
python3 <skill folder>/scripts/tn_assist run --harness claude-code
```

- Needs: Claude Code logged in on this machine, Python 3.9 or newer, the computer on and online.
- It checks every 20 seconds (`--interval`). Idle cycles cost no model tokens. Each customer message costs one short model turn (and a second one now and then to summarize a long conversation).
- To keep it running after you close the terminal, use what your system offers (`tmux`, `launchd`, `systemd`, a service manager). Logs with ids and counts (never message text) are in `<workspace>/logs/runner.jsonl`.
- To stop: Ctrl+C. Nothing is lost: the next start catches up, as long as it is within the plan's retention (1 hour by default, so restart quickly).
- A second runner on the same workspace does nothing.

## In session

You stay in Claude Code and it polls on a loop; every cycle is a model turn, so it costs tokens even when nothing arrives. Start it with:

```
/loop 1m /turbo-notify:virtual-attendant run one cycle
```

Follow [tick.md](tick.md) for each cycle. For each customer use the `contact-attendant` agent of this plugin (it has no tools) as described in [contact-turn.md](contact-turn.md). Close the session and the attendant stops answering.

## What it cannot do

- It does not run when the computer is off or Claude Code is closed. A message that arrives meanwhile is read when you start again, if within the retention.
- The in-session mode shares your session's tools and memory with the attendant's work. Prefer the unattended runner for a business.
