# Web Observer

An OpenClaw skill that watches your websites and messages you when something
breaks. Node and TypeScript, **zero runtime dependencies**, MIT-0.

```
🔴 api is DOWN: https://example.com/v1/orders
- Reason: unexpected status (returned 404, expected 200)
- Confirmed over 1 consecutive check, 1 request on the last one
- At: 2026-08-19 09:00:39 +03:00
```

You get that once. Not every five minutes until you mute it. When the site comes
back you get one more message, and then silence again:

```
🟢 api is back up: https://example.com/
- Down for about 22 minutes, since 2026-08-19 08:39:41 +03:00
- Now returning 200 in 90 ms
- At: 2026-08-19 09:01:42 +03:00
```

Alerts arrive on whatever chat channel OpenClaw already uses. Web Observer holds
no bot token of its own.

**Contents**

[What it watches](#what-it-watches) · [Quick start](#quick-start) ·
[Checking by hand](#checking-by-hand) · [Commands](#commands) ·
[Configuration](#configuration) · [Uptime](#uptime) · [Vercel](#vercel) ·
[GA4](#ga4) · [How the alerting works](#how-the-alerting-works) ·
[What it contacts](#what-it-contacts) · [Credentials](#credentials) ·
[Development](#development)

## What it watches

Three things. Each is **independent**: switch on one, two, or all three.

| Module | Answers | Needs |
| --- | --- | --- |
| **Uptime** | Is the site up? Is it returning the right status, and the right page? | nothing |
| **Vercel** | What is erroring? How fast does it feel? | [openclaw-vercel-insights](https://github.com/anatoli-iliev/openclaw-vercel-insights) |
| **GA4** | Who is visiting, and from where? | [open-ga4](https://github.com/anatoli-iliev/open-ga4) |

Uptime needs no credentials at all, so a Web Observer installed only to watch a
URL works the moment it is installed. The Vercel and GA4 work is handed to those
two skills; nothing about either API is reimplemented here. If one is not
installed, only the commands that needed it say so.

## Quick start

**1. Install.**

```bash
openclaw skills install git:https://github.com/anatoli-iliev/web-observer --as web-observer
```

**2. Save yourself some typing.** Every example below uses `wo`:

```bash
alias wo='node ~/.openclaw/workspace/skills/web-observer/lib/cli.js'
```

**3. Copy the example configuration and edit it.**

```bash
mkdir -p ~/.openclaw/web-observer
cp ~/.openclaw/workspace/skills/web-observer/examples/config.json \
   ~/.openclaw/web-observer/config.json
```

Change the URLs to yours, and set `notify.to` to the chat OpenClaw already
messages you on. `openclaw cron list` shows it in the Delivery column, as
`telegram:123456789`.

**4. Try it, then schedule it.**

```bash
wo check              # test everything right now
wo schedule           # show the cron commands this config needs
wo schedule --apply   # create them
wo doctor             # confirm nothing is left to do
```

That is the whole setup. [SETUP.md](SETUP.md) is the click-by-click version, with
a troubleshooting table for when a step does not go to plan.

## Checking by hand

`wo check` tests every URL immediately, whatever the schedule says, and prints
what it found:

```
Web Observer check at 2026-08-19 09:00:38 +03:00

watch   state  status  took    tries  detail
------  -----  ------  ------  -----  ------------------------------------------------------------------------------------------------
site    up     200     353 ms  1
health  DOWN   200     150 ms  1      body did not match: returned 200 but the body does not contain "status ok" (559 characters read)
api     DOWN   404     123 ms  1      unexpected status: returned 404, expected 200

1 up, 2 down
```

Note the middle row: `health` returned **200 and is still broken**, because the
page did not contain what it should. A status code alone would have called that
healthy.

`check` never changes anything, so run it as often as you like. It will not use
up the one alert a real outage is entitled to.

## Commands

| Command | What it does |
| --- | --- |
| `wo check` | Test every URL now and print a table. `--strict` exits 3 if anything is down. |
| `wo doctor` | What is configured, what is missing, and the single next thing to do. |
| `wo schedule` | Print the cron commands this configuration needs. `--apply` creates them. |
| `wo vercel <preset>` | Ask about Vercel: `errors`, `error-summary`, `vitals`, `top-pages`, … |
| `wo ga4 <preset>` | Ask about traffic: `report`, `compare`, `live`, `query`, … |
| `wo watch` | The scheduled uptime round. For cron, not for you. |
| `wo vercel-watch` | The scheduled Vercel error and speed poll. For cron. |
| `wo digest` | The scheduled traffic digest. For cron. |

The bottom three are what the cron jobs run. Running them by hand consumes an
alert, so use `check`, or add `--dry-run`.

Everything that would send a request or a message takes `--dry-run`.

## Configuration

One JSON file at `~/.openclaw/web-observer/config.json`. The smallest version
that does something useful:

```json
{
  "notify": { "channel": "telegram", "to": "telegram:123456789" },
  "uptime": {
    "watches": [
      { "id": "site", "url": "https://example.com", "intervalMinutes": 5 }
    ]
  }
}
```

The settings you are most likely to want:

| Setting | Default | What it does |
| --- | --- | --- |
| `intervalMinutes` | 5 | How often to check this URL. |
| `expectStatus` | `[200]` | A code, a class (`"2xx"`), or a range (`[200, 399]`). |
| `expectBody` | none | Text the page must contain. Catches a 200 that renders an error. |
| `failureThreshold` | 2 | Failed checks in a row before you are told. |
| `timeoutMs` | 10000 | How long to wait for a response. |
| `enabled` | true | Set false to keep a watch without running it. |

Every setting is listed in [SKILL.md](SKILL.md#a-watch). An unrecognised key is
**refused**, not ignored, and the error suggests the closest real one, because a
silently dropped setting would leave a default running with nothing to say so.

`notify` is used only when generating the cron commands. Nothing in this skill
sends anything itself.

## Uptime

### One scheduled job, many intervals

A marketing page and a payment webhook want different cadences, but one cron job
per URL would wake the gateway constantly. So a single job runs every
`tickMinutes`, and each round checks only the URLs that have come due.

An interval is therefore honoured to within one tick. `wo doctor` warns if an
interval is shorter than the tick, or not a multiple of it, because the real
cadence would otherwise quietly differ from the one you wrote down.

### Two thresholds, for two kinds of blip

- **`attempts`** (default 2) retries within one round, ten seconds later. This
  catches a dropped packet.
- **`failureThreshold`** (default 2) counts failed rounds, minutes apart. This
  catches a flaky minute.

Together, the defaults mean four failed requests over about five minutes before
anybody is woken up.

## Vercel

Errors, request logs, and Core Web Vitals against a budget.

> [!IMPORTANT]
> **TODO: re-pin this dependency.** Error-log support currently lives on the
> [`logs-surface` branch](https://github.com/anatoli-iliev/openclaw-vercel-insights/tree/logs-surface)
> of openclaw-vercel-insights (version 1.1.0) and should merge to `main` in time.
> When it does, set `REQUIRED_LOGS_REF` in `src/bridge/vercel.ts` to `"main"` or a
> release tag, and drop `#logs-surface` from the command below and in SETUP.md.
> Nothing else changes: every log call already goes through that one module, and
> the capability check looks for the presence of `vercel_insights/logs.py` rather
> than a version number, so it keeps working either way.

Traffic and speed work with any version. Errors need that branch:

```bash
openclaw skills install "git:https://github.com/anatoli-iliev/openclaw-vercel-insights#logs-surface" --as vercel-insights --force
```

An older copy is not a mystery failure: Web Observer names the version it found,
where it found it, and this command, and the traffic and speed presets keep
working.

```json
{
  "vercel": {
    "enabled": true,
    "project": "my-project",
    "errors": { "intervalMinutes": 15, "windowMinutes": 20, "threshold": 0, "includeMessages": false },
    "budget": { "intervalMinutes": 360, "metrics": { "lcp": 2500, "inp": 200, "cls": 0.1 } }
  }
}
```

Every fifteen minutes it asks for the last twenty. The five-minute overlap
matters: without it, an error arriving while a poll is in flight can fall into
the gap between two windows and never be reported. The overlap is free because
errors are deduplicated by request id, and if a poll is missed the window widens
to cover the gap.

To watch several sites, name them all with `projects` instead of `project`, for
example `"projects": ["my-project", "my-other-project"]`. Each project is polled
with its own query and keeps its own alert state, so errors on one site neither
raise nor clear an alert for another, and every alert names its project. The
`errors` and `budget` settings apply to all of them, and one account- or
team-scoped token covers them all.

`threshold` is how many new errors a poll tolerates before alerting; `0` alerts
on any. Errors below the threshold are deliberately **not** remembered, so a slow
trickle still adds up to an alert instead of being forgotten one poll at a time.

### What an error alert says

An alert names the project and its domain, then lists each **distinct** error
once: how many times it happened, on which routes, with what status, whether it was an
HTTP failure or only counts because it logged an error line,
and one request id to look up in the Vercel dashboard. Twenty-four copies of one
warning read as one line with a count.

```
🟠 my-project (example.com): 25 new errors on Vercel in the last 20 minutes, 2 distinct:
1. 24 x "(node:6) [DEP0005] DeprecationWarning: Buffer() is deprecated…"
   on GET / (13), /api/cron/cleanup (5), /products/[slug] (5) and 1 more; status 200; not an HTTP failure; counted because it logged at error level
   e.g. request fra1::abcde-1791…
2. 1 x "order sync failed: 503 upstream timeout"
   on POST /api/orders; status 303; not an HTTP failure; counted because it logged at error level
   e.g. request fra1::fghij-1791…
At: 2026-10-14 18:25:45 +03:00
```

The quoted messages appear only with `includeMessages` on. Without it, errors
are told apart by method, route and status instead.

### Your application's log text is not forwarded by default

By default, alerts carry counts, statuses and affected routes, not the log
messages your code printed.

That is because the underlying skill scrubs only its own Vercel token from log
content: anything else your application wrote, which may include secrets, tokens
and customer data, arrives exactly as written. So the message text is dropped at
the bridge rather than at the formatter. With `includeMessages` off, it is never
copied out of `src/bridge/vercel.ts` at all, and no downstream mistake can leak
it.

Turn it on only having decided that is fine for your logs. When it is on, only
the first line of each message is sent, capped at 200 characters, with the usual
shapes of secrets replaced by `[redacted]`: `key=value` pairs whose key names a
secret, bearer and basic credentials, email addresses, JWTs, credentials in a
URL, and long runs of letters and digits such as API keys. That is pattern
matching, not a guarantee, which is why it stays opt-in.

## GA4

```json
{
  "ga4": {
    "enabled": true,
    "property": "123456789",
    "digest": { "cron": "0 9 * * 1", "since": "7d" }
  }
}
```

For several sites, use `"properties": ["123456789", "987654321"]` instead of
`property`. The digest then has one section per property, and a property that
fails is reported in the run log without holding back the others.

Needs [open-ga4](https://github.com/anatoli-iliev/open-ga4):

```bash
openclaw skills install git:https://github.com/anatoli-iliev/open-ga4 --as open-ga4
```

Without it, the two GA4 commands say so and exit 2. Uptime and Vercel are
unaffected.

## How the alerting works

Worth two minutes, because it explains why there is no bot token to configure.

OpenClaw's scheduler can run a command and deliver that command's **stdout** to a
chat channel. Printing the exact token `NO_REPLY` suppresses the delivery.

So an alert is a scheduled command printing text, and silence is the same command
printing `NO_REPLY`. Nothing here opens a connection to Telegram: alerts travel
over the channel the cron job names, which is the one OpenClaw already has.

`wo schedule` writes those cron jobs for you, because a skill manifest has no
field for scheduling. It sets an explicit `--timeout-seconds`, since cron's
30-second default is shorter than a single watch's worst case: two ten-second
attempts with a ten-second pause between them reaches exactly 30 seconds.

Two consequences, if you plan to change the code:

- **Anything a scheduled run prints is sent to you, stderr included.** OpenClaw
  stays silent only when the whole output is exactly `NO_REPLY`; any stderr is
  delivered with it under a `stderr:` heading. So `watch`, `vercel-watch` and
  `digest` hold their notes back and, when the run succeeds, append them to
  `web-observer.log` beside the state file instead. A failed run still writes
  them to stderr, because then they explain the failure.
- **A scheduled run exits 0 even when it alerts.** An alert is the tool working. A
  non-zero exit would also trigger OpenClaw's own cron failure notification, so
  one outage would reach you twice by two different routes.

### If OpenClaw's cron is unavailable

Running with `cron.enabled: false` or `OPENCLAW_SKIP_CRON=1`? There is a systemd
unit and timer in [`examples/`](examples/web-observer-monitor.service). Prefer
cron when you have it, since that is what delivers an alert without this skill
holding any credential.

## What it contacts

Exactly the URLs you configured, and nothing else. That is enforced in code, not
just promised here:

- The allowlist is built from your watch URLs by one function with no other
  input, and no flag extends it.
- The host is checked before every request **and again on every redirect hop**. A
  redirect leaving the allowlist fails the check, naming the host, and is never
  followed. `fetch` is never allowed to follow a redirect itself, so the
  allowlist binds every hop rather than only the first.
- A redirect from https to http is refused, even on the same host, so a
  configured header never travels in the clear.
- Configured headers go only to the watch's own host, never to another watch's
  host that a redirect lands on.
- Only `GET`, `HEAD` and `OPTIONS` are ever sent.
- A response body is measured, never quoted into an alert, and at most 1 MiB of
  it is read.

Everything Vercel and GA4 runs as a subprocess, invoked as an argument vector
with no shell, using those skills' own allowlists.

## Credentials

Web Observer has no credential of its own, and declares no `primaryEnv`, because
there is no key to save.

The two delegated skills do have credentials, and a scheduled run cannot inherit
them: an OpenClaw cron job runs with the **Gateway's** environment, which does
not carry a skill's configured variables. So Web Observer reads what the
delegated skill is already configured with, from `skills.entries.<slug>` in
`openclaw.json`, and passes it to that same skill in its subprocess environment.
Your secret keeps living in exactly one place.

It is never put on a command line, never printed, and never written to a file.
`wo doctor` reports only where a value came from.

A `SecretRef` cannot be resolved outside the Gateway. Web Observer says so rather
than guessing, and suggests giving it its own copy:

```bash
openclaw config set skills.entries.web-observer.env.VERCEL_TOKEN \
  --ref-provider default --ref-source env --ref-id VERCEL_TOKEN
```

<details>
<summary><b>Three facts about Vercel's log API that shaped this design</b></summary>

All three were measured against a live account, not read from a document.

**A window that ends in the past can fail.** With `--until` more than about an
hour ago, the API answers `HTTP 400 ExceedsBillingLimitError`. With the end left
at now, every `--since` succeeds, from 30 minutes to 7 days. So the poller never
specifies an end, which removes the failure mode rather than handling it.

**An empty answer is a success, not a clean bill of health.** Runtime logs are
retained for 1 hour on Hobby, 1 day on Pro, 3 days on Enterprise, and 30 days
with Observability Plus. An empty result over a longer window can mean the logs
aged out, and the alert says so rather than claiming the site is fine.

**There is no live tail** that a request/response client can use, so this is a
polling loop by necessity rather than by preference.

</details>

## Development

```bash
npm install
npm run check     # typecheck, test, rebuild lib/
```

`lib/` is committed, because no install route runs a build: ClawHub copies files,
`openclaw skills install git:…` clones, and a local install is a directory copy.
`npm run check:lib` fails if the committed output no longer matches `src/`.

Tests include a set that fail when the documentation stops describing the code:
the declared environment variables against those actually read, the documented
exit codes against those returned, the flag table against the parser, and each
security claim above against the code enforcing it.

[CONTRIBUTING.md](CONTRIBUTING.md) covers the decisions worth reading before
changing the behaviour they describe.

## Licence

MIT-0. See [LICENSE](LICENSE). Do what you like with it; no attribution needed.
