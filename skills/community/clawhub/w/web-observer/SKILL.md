---
name: web-observer
description: >-
  Watches websites and reports what broke: uptime checks that alert when a site
  goes down and again when it recovers, Vercel error logs and Core Web Vitals,
  and GA4 traffic. Ask "is my site up", "did anything error on Vercel", or "how
  much traffic last week".
version: 0.2.1
homepage: https://github.com/anatoli-iliev/web-observer
compatibility: openclaw >=1.0
metadata:
  openclaw:
    requires:
      bins: [node]
    envVars:
      - name: WEB_OBSERVER_CONFIG
        required: false
        description: >-
          Path to the configuration file. Defaults to
          <openclaw-state>/web-observer/config.json.
      - name: WEB_OBSERVER_STATE
        required: false
        description: >-
          Path to the state file that remembers what is already down. Defaults
          to state.json beside the configuration.
      - name: OPENCLAW_STATE_DIR
        required: false
        description: >-
          OpenClaw's state directory. Set by `openclaw --profile` and `--dev`,
          and read so each profile keeps its own configuration and state.
      - name: WEB_OBSERVER_VERCEL_SKILL_DIR
        required: false
        description: >-
          Directory of an installed vercel-insights skill, when it is somewhere
          the usual search would not find it.
      - name: WEB_OBSERVER_GA4_SKILL_DIR
        required: false
        description: Directory of an installed open-ga4 skill, same purpose.
      - name: VERCEL_TOKEN
        required: false
        description: >-
          Read only to hand on to the vercel-insights skill. Normally left
          unset: it is read from that skill's own configuration instead.
      - name: VERCEL_PROJECT_ID
        required: false
        description: Passed through to vercel-insights when set.
      - name: VERCEL_TEAM_ID
        required: false
        description: Passed through to vercel-insights when set.
      - name: VERCEL_TEAM_SLUG
        required: false
        description: Passed through to vercel-insights when set.
      - name: VERCEL_ORG_ID
        required: false
        description: Passed through to vercel-insights when set.
      - name: VERCEL_OWNER_ID
        required: false
        description: Passed through to vercel-insights when set.
      - name: GA4_CREDENTIALS
        required: false
        description: >-
          Read only to hand on to the open-ga4 skill. Normally left unset: it is
          read from that skill's own configuration instead.
      - name: GA4_PROPERTY_ID
        required: false
        description: Passed through to open-ga4 when set.
      - name: GOOGLE_APPLICATION_CREDENTIALS
        required: false
        description: Passed through to open-ga4 when set.
    emoji: "🔭"
    homepage: https://github.com/anatoli-iliev/web-observer
---

# Web Observer

Three questions about a website, from one command line. **Is it up?** Uptime
checks on a per-URL interval, with one alert when a site goes down and one when
it comes back. **Is it erroring or slow?** Vercel request logs and Core Web
Vitals. **Is anybody visiting?** GA4 traffic.

Only the first is implemented here. Vercel and GA4 are answered by two other
skills, and Web Observer never reimplements either.

Run it as:

```bash
node <skill-dir>/lib/cli.js <command>
```

## Answering a question with this

**1. Which question is it?** "Is the site up" is `check`. "What broke" is
`vercel errors`. "How many visitors" is `ga4 report`. The table below routes the
usual phrasings.

**2. Is it configured?** No credential is needed for uptime watching. If a
command reports a missing configuration, say which file it named and offer to
add a watch, rather than guessing a URL.

**3. Run it and read the answer back.** The table output is already laid out for
a person: quote it rather than re-typesetting it, then add the one sentence of
interpretation the numbers support.

### What the user says, and what to run

| The user says | Run |
| --- | --- |
| "is my site up", "check the site now", "are any sites down" | `check` |
| "check just the blog" | `check --only blog` |
| "did example.com go down last night" | `doctor --json`, then read the state file it names; this tool alerts on change and does not keep a history |
| "set up monitoring", "why is this not working", "it never alerts me" | `doctor --json` |
| "start watching", "schedule it", "make it run every 5 minutes" | `schedule` (prints the commands), then `schedule --apply` |
| "what errors did my site have", "why am I getting 500s", "show me the logs" | `vercel errors --since 30m` |
| "which routes are failing", "group the errors" | `vercel error-summary --since 6h` |
| "how fast is the site", "what are my Core Web Vitals" | `vercel vitals` |
| "which pages are slowest" | `vercel slowest-pages` |
| "how is my traffic", "top pages this week", "where do visitors come from" | `ga4 report`, `ga4 query`, or `vercel top-pages` |
| "who is on the site right now" | `ga4 live` |
| "test the alerts without spamming me" | `watch --dry-run` |

`watch`, `vercel-watch` and `digest` are for the scheduler, not for
conversation. Running them by hand consumes the one alert an outage gets. Use
`check` to look at things now, or add `--dry-run`.

### When input is missing or vague

- **No URL, or a loose name ("the blog", "our site")**: run `check` and match
  their words against the watch ids it prints. If several could match, ask. Do
  not invent a URL and do not add one to the configuration without being asked.
- **A Vercel question with no project**: `vercel overview` will list the
  account's projects if none is configured. List them and ask; do not pick one.
  When several projects are configured and the question does not say which
  site, ask, or pass `--project` for each and say which answer is which.
- **"Why did nobody tell me"**: run `doctor --json`. The usual answer is that
  the cron job was never created, which `blocked_on: "no_cron_jobs"` names.

### When to add `--json`

Prefer the table when relaying an answer. Add `--json` only when a figure has to
be **computed**: comparing two runs, or pulling one number into a sentence.
`doctor --json` is the exception that is always right, because its shape is a
next-step state machine rather than a report.

### What the exit codes mean

| Code | Meaning | What to say |
| --- | --- | --- |
| 0 | Worked | Report the answer. **A run that finds everything healthy is a success**, and so is an error query that returns nothing. |
| 1 | A check or a delegated call failed for a network or API reason | Say the check failed, and that this is not the same as the site being down. |
| 2 | Configuration or usage error | Quote the message: it names the setting and the fix. Nothing was attempted. |
| 3 | Worked, and something is down or over budget | Only from `check --strict`. Report what is down. |
| 130 | Interrupted | Say it was interrupted. |

### Rules that matter more than the output

- **Never state a number that was not measured.** If a query is empty or a
  metric is missing, say so. A confidently worded figure nobody measured is the
  most damaging thing available here.
- **An empty error log is not proof of a healthy site.** Vercel retains runtime
  logs for one hour on Hobby, one day on Pro, three days on Enterprise, thirty
  with Observability Plus. An empty answer over a longer window can mean the
  logs aged out. Say that rather than "no errors".
- **Never quote raw Vercel log text into a chat unless the user asked for it.**
  The underlying skill scrubs only its own Vercel token from log content;
  anything the application printed, including secrets and customer data, comes
  through as written. Web Observer's alerts therefore carry counts, statuses and
  routes. If somebody wants the text, they run `vercel errors` themselves, or
  set `includeMessages: true` knowing what it means.
- **Do not ask the user to paste a token into the conversation.** Point them at
  `openclaw config set`.

## Commands

| Command | What it does |
| --- | --- |
| `check` | Runs every configured watch once, now, and prints a table. Does not change alert state. |
| `watch` | The scheduled uptime round. Checks what is due, prints an alert or `NO_REPLY`. |
| `vercel-watch` | The scheduled Vercel error-log and performance-budget poll. |
| `digest` | The scheduled GA4 traffic digest. |
| `vercel <preset> [flags]` | Ask the vercel-insights skill. |
| `ga4 <preset> [flags]` | Ask the open-ga4 skill. |
| `doctor` | Configuration, dependency and schedule diagnosis. |
| `schedule` | Prints the `openclaw cron add` commands this configuration needs. |

### Flags

| Flag | On | What it does |
| --- | --- | --- |
| `--json` | `check`, `doctor`, `schedule` | Machine-readable output. |
| `--strict` | `check` | Exit 3 when anything is down. For CI. |
| `--only ID` | `check` | Limit to named watches. Repeatable or comma separated. |
| `--dry-run` | `check`, `watch`, `vercel-watch`, `digest` | Make no lasting change and deliver nothing. |
| `--apply` | `schedule` | Actually create the cron jobs. |

An unrecognised flag is a usage error, never ignored. A dry run that quietly was
not one would be worse than no dry run at all.

## How alerting works, and why nothing here has a bot token

An OpenClaw cron job with a `command` payload and `--announce` delivers the
command's **stdout** to a chat channel. Printing the exact token `NO_REPLY`
suppresses that delivery. So:

- An alert is a scheduled command printing text.
- Silence is that command printing `NO_REPLY`.

That is the whole notification mechanism. Web Observer opens no connection to
Telegram or anything else, and holds no bot token. Alerts travel over whatever
channel the cron job names, which is the channel already configured in OpenClaw.

Two consequences worth knowing:

- On a scheduled run, **anything printed is sent to the user, stderr included**:
  OpenClaw stays silent only when the whole output is exactly `NO_REPLY`. So a
  successful `watch`, `vercel-watch` or `digest` appends its notes to
  `web-observer.log` beside the state file instead of stderr; a failed one
  still writes them to stderr.
- `watch` exits **0 even when it alerts**. An alert is this tool working. A
  non-zero exit would additionally fire OpenClaw's own cron failure
  notification, so one outage would be reported twice by two mechanisms.

## Setting it up

`openclaw skills install` then a configuration file. Uptime needs no
credentials, so nothing else is required for it.

```bash
node <skill-dir>/lib/cli.js doctor
```

`doctor` names the configuration file it expects. Copy `examples/config.json`
from this skill's directory to that path and edit it. Then:

```bash
node <skill-dir>/lib/cli.js check
node <skill-dir>/lib/cli.js schedule
node <skill-dir>/lib/cli.js schedule --apply
```

`SETUP.md` in this skill's directory is the click-by-click version, including
the Vercel and GA4 modules and a troubleshooting table.

### The three modules are independent

Each of `uptime`, `vercel` and `ga4` has its own `enabled`, and each command
checks only the module it needs. Web Observer installed for uptime alone is
ready the moment it is installed: `requires` names `node` and nothing else, and
nothing in `requires.env`, so it is never held in "needs setup" for a credential
it does not use.

`vercel` needs the `vercel-insights` skill; `ga4` needs `open-ga4`. When one is
absent, the command that needed it says so, names the install command, and exits
2. Nothing else stops working.

## Configuration

One JSON file, by default `<openclaw-state>/web-observer/config.json`. Not in
`openclaw.json`, because every install route replaces the skill directory and a
list of watches is awkward to edit with `openclaw config set`.

```json
{
  "notify": { "channel": "telegram", "to": "telegram:123456789" },
  "uptime": {
    "enabled": true,
    "tickMinutes": 5,
    "defaults": { "timeoutMs": 10000, "failureThreshold": 2 },
    "watches": [
      { "id": "site", "url": "https://example.com", "intervalMinutes": 5 },
      {
        "id": "api",
        "url": "https://example.com/health",
        "intervalMinutes": 1,
        "expectBody": "\"ok\":true",
        "failureThreshold": 1
      }
    ]
  }
}
```

### A watch

| Setting | Default | Meaning |
| --- | --- | --- |
| `id` | required | Keys this watch's saved state. Renaming it forgets whether the URL was down. |
| `url` | required | http or https. Credentials in the URL are refused; use `headers`. |
| `intervalMinutes` | 5 | How often to check. Each check lands on the nearest scheduled round, so setting this to `tickMinutes` or below means every round checks it. |
| `method` | `GET` | `GET`, `HEAD` or `OPTIONS` only. A health check must not be able to change anything. |
| `expectStatus` | `[200]` | A code (`200`), a class (`"2xx"`), a range (`[200, 399]`), or a list of those. |
| `expectBody` | none | Substring the body must contain. Catches a 200 that renders an error page. |
| `expectBodyRegex` | none | A pattern instead of a substring. Not both. |
| `timeoutMs` | 10000 | Per request. |
| `attempts` | 2 | Requests within one check. Succeeds as soon as one does. |
| `retryDelayMs` | 10000 | Pause between attempts. |
| `failureThreshold` | 2 | Consecutive failed **checks** before the first alert. |
| `recoveryThreshold` | 1 | Consecutive successes before the recovery message. |
| `followRedirects` | 0 | Hops to follow. Every hop is allowlist-checked. |
| `headers` | none | Sent as given. Newlines are refused. |
| `enabled` | true | A disabled watch is never checked. |

`attempts` and `failureThreshold` guard against different things at different
speeds. `attempts` retries seconds apart inside one run, which catches a dropped
packet. `failureThreshold` waits for the next tick, minutes later, which catches
a flaky minute. The defaults mean four failed requests over about five minutes
before anybody is woken up.

### Vercel and GA4

```json
{
  "vercel": {
    "enabled": true,
    "project": "my-project",
    "errors": {
      "intervalMinutes": 15,
      "windowMinutes": 20,
      "threshold": 0,
      "includeMessages": false
    },
    "budget": { "intervalMinutes": 360, "metrics": { "lcp": 2500, "inp": 200, "cls": 0.1 } }
  },
  "ga4": {
    "enabled": true,
    "property": "123456789",
    "digest": { "cron": "0 9 * * 1", "preset": "report", "since": "7d" }
  }
}
```

For several sites, write `"projects": ["a", "b"]` instead of `project`, and
`"properties": ["1", "2"]` instead of `property`; giving both spellings is a
configuration error. Each Vercel project keeps its own alert state and every
alert names its project. Uptime already takes one entry per URL in `watches`.

`windowMinutes` must exceed `intervalMinutes`. The overlap is what stops an
error arriving mid-poll from falling into the gap between two windows, and it
costs nothing because errors are deduplicated by request id.

`includeMessages` defaults to false and should stay there unless you have
thought about it: see the rule above about raw log text. When on, each message is
cut to its first line, capped at 200 characters, and common secret shapes are
replaced by `[redacted]`; alerts then quote each distinct error once with its
count and routes.

## This skill's own network access

Web Observer contacts exactly the URLs configured under `uptime.watches`, and
nothing else. That is enforced in code, not merely documented:

- The allowlist is derived from the configured watch URLs. There is no other
  constructor for it and no flag that extends it.
- The host is re-checked before every request, including **every redirect hop**.
  A redirect to a host no watch configures fails the check with reason
  `redirect-off-allowlist`, naming the host, and is never followed. So does a
  redirect from https to http, even on the same host.
- Configured `headers` are sent only to the watch's own host. A redirect to
  another watch's host is followed without them.
- Redirects are not followed at all by default, and `fetch` is never allowed to
  follow one itself, so the allowlist binds every hop rather than only the first.
- Only `GET`, `HEAD` and `OPTIONS` are ever issued.
- A response body is measured, never quoted into an alert, and never more than
  1 MiB of it is read.

Everything Vercel and GA4 is a subprocess: those skills make those requests with
their own credentials and their own allowlists. Web Observer passes arguments as
an argument vector, never through a shell.

## Files and credentials this skill reads

Declared here because no manifest field can say it without side effects:
`requires.config` is an eligibility gate in OpenClaw, not a declaration, and
listing these keys there would hold an uptime-only install in "needs setup".

**Uptime watching reads no credential and no other skill's files.** Beyond its
own configuration and state file it touches nothing.

The Vercel and GA4 modules read `<openclaw-state>/openclaw.json`, and from it
only these keys:

- `skills.entries.vercel-insights.apiKey` and `skills.entries.vercel-insights.env`:
  the Vercel token and the project and team ids from the variables declared
  above.
- `skills.entries.open-ga4.apiKey` and `skills.entries.open-ga4.env`: the GA4
  credentials and property id from the variables declared above.
- `skills.entries.<slug>.enabled` for those two slugs, to report a disabled
  skill rather than run it.
- `agents.defaults.workspace`, to find where those two skills are installed.

They are read only when you run a `vercel` or `ga4` command, or when `doctor`,
`vercel-watch` or `digest` covers a module you enabled. Why they are read at
all: a scheduled cron job runs with the Gateway's environment rather than a
skill's, so the credentials the delegated skill is configured with are absent
from a scheduled run unless something reads them. Reading them keeps the secret
in one place instead of asking you to configure it twice.

A value read this way is passed only in the environment of the subprocess that
runs that same skill. It is never put on a command line, never printed, never
written to a file, and never sent anywhere by Web Observer itself. A value that
is a secret reference, or a `${VAR}` interpolation of an unset variable, is
reported by name and not resolved.

Also read: each delegated skill's `SKILL.md` for its version, and whether its
`.venv` and `vercel_insights/logs.py` exist.

Written: only the state file beside the configuration (default
`<openclaw-state>/web-observer/state.json`, mode 0600). `schedule --apply` also
creates cron jobs, by running `openclaw cron add`. It runs only when you pass
`--apply`, and it never replaces a job that already exists.

## Failure reasons

`timeout`, `dns`, `connection-refused`, `tls`, `status-mismatch`,
`body-mismatch`, `redirect-off-allowlist`, `network`. Each alert names one, with
the observed value behind it.
