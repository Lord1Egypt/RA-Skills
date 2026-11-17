# vercel-insights

What broke, how many people came, and how fast it felt: answered in one command
line.

```console
$ vercel-insights vitals

metric                        p75  target  verdict
-------------------------  ------  ------  ------------
Largest Contentful Paint    2.9 s   2.5 s  over target
Interaction to Next Paint  184 ms  200 ms  meets target
Cumulative Layout Shift     0.128   0.100  over target
First Contentful Paint      1.6 s   1.8 s  meets target
Time to First Byte         412 ms  800 ms  meets target
```

Three Vercel APIs, one CLI: request logs for what is failing right now, Web
Analytics for how many people came and where from, and Speed Insights for how
fast the site felt when they got there.

## Start here

Two ways in. Pick the one that sounds like you.

- **"I use OpenClaw and I just want to ask it questions."** Start with
  [Set it up in OpenClaw](#set-it-up-in-openclaw), just below. No programming
  needed. About five minutes, mostly waiting for downloads.
- **"I want a command line tool."** Skip to
  [Use it from a terminal](#use-it-from-a-terminal).

### Set it up in OpenClaw

Four steps. Copy each grey block whole, paste it into your terminal, press
Enter. After each one there is a line telling you what you should see, so you
always know whether it worked before moving on.

#### Step 1: install it

```bash
clawhub install vercel-insights
```

**You should see:** `Installed vercel-insights v1.1.1 -> ...`

#### Step 2: make it runnable

One time only. Two things need fixing that the installer cannot do for you: it
cannot mark the program as runnable, and this tool needs one Python library
called `requests`.

```bash
SKILL=~/.openclaw/workspace/skills/vercel-insights
chmod +x "$SKILL/bin/vercel-insights"
python3 -m venv "$SKILL/.venv"
"$SKILL/.venv/bin/python" -m pip install requests
"$SKILL/bin/vercel-insights" --version
```

**You should see:** `vercel-insights 1.1.1` on the last line. Anything installed
here goes inside the skill's own folder and touches nothing else on your
computer.

#### Step 3: give it a Vercel token

A token is a password that lets this skill read your Vercel data. Make one at
**<https://vercel.com/account/tokens>**.

When Vercel asks about **scope**, choose your **account** or your **team**. Do
not choose a single project. This matters more than it sounds like it does, and
[the note below](#the-one-thing-that-trips-people-up) explains why. Read access
is all this skill ever needs; it cannot change anything. So take the narrowest
read scope Vercel will give you and nothing wider: what the token can reach is
what an accident with it can reach.

Vercel shows the token once, so copy it before closing the page. Now pick how to
hand it over. The first route keeps the secret out of your OpenClaw config file,
and it is the one to prefer.

**Best: keep the token in an environment variable and point the config at it.**

```bash
openclaw config set skills.entries.vercel-insights.apiKey \
  --ref-provider default --ref-source env --ref-id VERCEL_TOKEN
```

No secret appears on that line, so none reaches your shell history. What it
saves is a *reference*: OpenClaw reads the token out of `VERCEL_TOKEN` when it
needs one, and `~/.openclaw/openclaw.json` never holds the token itself. The
catch is that `VERCEL_TOKEN` has to be set wherever the OpenClaw gateway starts,
not only in the terminal you are typing in, so this route is for you if you know
where that is.

**Simpler, and less safe: save the token itself.**

```bash
openclaw config set skills.entries.vercel-insights.apiKey PASTE_YOUR_TOKEN_HERE
```

> **What that costs, so you can decide on purpose.** A token typed after
> `config set` is written to your shell history file, and is readable in a
> process listing for as long as the command runs. It is then stored in
> plaintext in `~/.openclaw/openclaw.json`, and `config set` copies the previous
> contents to `~/.openclaw/openclaw.json.bak` on every change, so a second copy
> lives there too. Keep both files readable by your user alone
> (`chmod 600 ~/.openclaw/openclaw.json*`), keep them out of backups and synced
> folders, and rotate the token at <https://vercel.com/account/tokens> if either
> file has been anywhere less private. Prefer clicking to typing?
> `openclaw dashboard` opens the Control UI, where
> **Skills, vercel-insights, Save key** saves the same value without it passing
> through a command line, though it still lands in the config file.

Either way, check it:

```bash
openclaw skills check
```

**You should see:** `vercel-insights` listed as ready, not under "Missing
requirements".

If your Vercel projects belong to a **team** rather than to you personally, add
this one extra line (find the ID under Team Settings, General):

```bash
openclaw config set skills.entries.vercel-insights.env.VERCEL_TEAM_ID team_xxxxxxxx
```

#### Step 4: ask your agent something

That is the whole setup. Now talk to OpenClaw normally:

> **What errors did my site have in the last 30 minutes?**
>
> **How's my site traffic this week?**
>
> **Is my site fast?**
>
> **Which pages are slowest?**
>
> **Where is my traffic coming from?**

If you have more than one Vercel project, the agent will list them and ask which
one you mean rather than guessing. You can also just say **"which Vercel
projects do I have?"**

#### If something went wrong

| What you saw | What to do |
| --- | --- |
| `Permission denied` | Step 2 was skipped. Run it. |
| `'requests' is not importable by this interpreter` | Step 2 was skipped, or its last line failed. Run it again and read the output. |
| `openclaw skills check` still says missing | The token did not save. Re-run step 3 and check for a typo in the config path. |
| `404 Observability Data not found.` | Your token is scoped to one project. Make a new account-scoped one, step 3. |
| `403 You don't have permission to access this resource.` on an errors or logs question | Same cause: request logs are scoped by the owning account too. Make an account or team scoped token, step 3. |
| Speed questions work, traffic questions fail with 403 or 404 | The project belongs to a team. Add `VERCEL_TEAM_ID`, end of step 3. |
| Empty results, no error | That project genuinely has no data for that period, or the feature is switched off for it in Vercel. On an errors or logs question the logs may instead have aged out: retention is one hour on Hobby. |

Longer walkthrough, with every failure we actually hit and how to tell them
apart: **[docs/openclaw-setup.md](docs/openclaw-setup.md)**.

### Use it from a terminal

```bash
# 1. Get it
git clone https://github.com/anatoli-iliev/openclaw-vercel-insights.git
cd openclaw-vercel-insights
python3 -m venv .venv && .venv/bin/python -m pip install requests

# 2. A token, from https://vercel.com/account/tokens
#    Scope it to the ACCOUNT or TEAM, not to a single project. See the note below,
#    and take the narrowest read scope offered: this tool never writes.
#    Typed at a prompt rather than pasted into the command line, because a token
#    in an `export VERCEL_TOKEN=...` command is saved to your shell history file
#    and is visible in a process listing while that command runs.
printf 'Vercel token: '; read -rs VERCEL_TOKEN; echo; export VERCEL_TOKEN

# 3. Which project? This lists them, and needs nothing else configured.
.venv/bin/python -m vercel_insights --list-projects

# 4. Ask it something. Use the name or the prj_ id from step 3.
.venv/bin/python -m vercel_insights vitals --project acme-docs
.venv/bin/python -m vercel_insights --project acme-docs        # last 7 days of traffic
```

> <a id="the-one-thing-that-trips-people-up"></a>
> **The one thing that trips people up.** A token scoped to a *single project*
> reads traffic fine but cannot read Speed Insights, because Vercel serves those
> from an account-scoped API. Symptom: `404 Observability Data not found.`, which
> reads like "no data" but means "this token cannot ask". An account or team
> scoped token does both.

Nothing to configure beyond that, and nothing is written to disk. Set
`VERCEL_PROJECT_ID` if you get tired of `--project`. Add `--dry-run` to any
command to see the exact request without sending it, no token required.

**Where to go next**

| I want to | Read |
| --- | --- |
| Find out what is failing right now | [Errors and request logs](#errors-and-request-logs) |
| See what the output looks like, for everything | [examples/example_outputs.md](examples/example_outputs.md) |
| Know which presets exist | [Presets](#presets), or run `--list-presets` |
| Fail a build when the site gets slower | [Guarding performance in CI](#guarding-performance-in-ci) |
| Query something other than traffic and vitals | [Beyond web vitals](#beyond-web-vitals) |
| Understand what this can and cannot reach | [Plans, windows and what is out of reach](#plans-windows-and-what-is-out-of-reach) |
| Check the security posture | [Security and permissions](#security-and-permissions) |
| Set it up as an OpenClaw skill | [Set it up in OpenClaw](#set-it-up-in-openclaw), then [docs/openclaw-setup.md](docs/openclaw-setup.md) for the detail |

## Why not just open the dashboard

Because a dashboard answers one question at a time, and only for the person
looking at it.

- **One line, one answer.** No date picker, no tab switching, no waiting for a
  chart to animate. `trend --since 4w --granularity week` is the whole
  interaction, and so is `vitals`.
- **Rankings the dashboard will not give you.** The Speed Insights dashboard
  shows a route list, but it cannot sort your routes by P75 LCP worst-first and
  hand you the top ten. `slowest-pages` is exactly that query, and
  `fastest-pages` is its mirror.
- **Comparison across projects.** A dashboard is one project per tab. On the
  Speed Insights presets, `--all` queries every project in the team in one go.
  It is a Speed Insights option only: on a traffic preset it is a configuration
  error, so compare traffic by running the same command once per `--project`
  and diffing the `--json`.
- **Diffable between deploys.** Yesterday's CSV against today's CSV is a real
  answer to "did that ship make the site slower". Two screenshots are not. Put
  `vitals-trend --granularity 1d --csv` in a nightly job and the regression
  shows up as a line in a file, not as a feeling.
- **Scriptable.** Cron job, CI step, Makefile. Exit codes are meaningful: 0 for
  success (an empty result included), 1 for an API failure, 2 for a bad command,
  and 3 for a `--budget` that was exceeded.
- **Pipeable.** `--json` feeds `jq`, `--csv` feeds a spreadsheet or `duckdb`. The
  raw API payload is preserved under `raw` in the JSON output, so nothing is
  lost in translation.
- **Agent-native.** It ships as an OpenClaw skill, so "how did the blog do this
  week" or "which pages are slowest on mobile" inside a conversation becomes a
  real query with a real table, not a guess.
- **Safe by construction.** Read-only against a six-endpoint allowlist, and
  the token never leaves the `Authorization` header. See
  [Security and permissions](#security-and-permissions).

## Setup in detail

The quick start above is the whole of it for most people. This section covers
the parts that vary.

### Running it from anywhere

`bin/vercel-insights` works from any directory and prefers a `.venv` beside the
checkout, so an installed copy needs no `PATH` or working-directory setup:

```bash
/path/to/openclaw-vercel-insights/bin/vercel-insights vitals
```

`python3 -m vercel_insights` is equivalent from inside the checkout.

### Installing

From ClawHub, which is the shortest route and the one
[Set it up in OpenClaw](#set-it-up-in-openclaw) walks through step by step:

```bash
clawhub install vercel-insights
```

It lands in `~/.openclaw/workspace/skills/vercel-insights`. Two things the
installer cannot do for you, both one-time:

```bash
SKILL=~/.openclaw/workspace/skills/vercel-insights
chmod +x "$SKILL/bin/vercel-insights"                       # the exec bit is not preserved
python3 -m venv "$SKILL/.venv" && "$SKILL/.venv/bin/python" -m pip install requests
```

From a local checkout instead, which does preserve the exec bit:

```bash
openclaw skills install /path/to/openclaw-vercel-insights --as vercel-insights
```

Either way, save the token where the gateway reads it rather than exporting
anything:

```bash
openclaw config set skills.entries.vercel-insights.apiKey YOUR_TOKEN
openclaw skills check          # confirms the requirement resolved
```

The Control UI does the same thing under Skills, vercel-insights, Save key, and
`openclaw skills info vercel-insights` prints both routes.

Full walkthrough, including every failure worth recognising and how to tell them
apart: **[docs/openclaw-setup.md](docs/openclaw-setup.md)**.

The gateway runs as its own process, so a variable exported in an interactive
shell may not reach it. `openclaw configure` writes it where the gateway reads
it. To keep the token out of the config file entirely:

```bash
openclaw config set skills.entries.vercel-insights.apiKey \
  --ref-provider default --ref-source env --ref-id VERCEL_TOKEN
```

Python 3.10 or newer, and `requests` is the only thing outside the standard
library. The virtualenv in the quick start is not ceremony: Debian 12+, Ubuntu
23.04+, Fedora and Homebrew Python all mark the system interpreter as externally
managed (PEP 668), so a bare `pip install requests` there stops with
`error: externally-managed-environment` before installing anything. If you would
rather not keep a `.venv`, `pip install --user requests` works where user
installs are still permitted, as does your distribution's own package
(`apt install python3-requests`).

Already have `requests` importable? `python3 -m vercel_insights` works from the
repository root as is. From anywhere else,
`python3 /abs/path/to/vercel_insights/__main__.py` works too: the entry point
repairs `sys.path` before importing. And `pip install -e .` adds a
`vercel-insights` console script on `PATH`, which is the same entry point.

### The token, and why its scope matters

Create one at <https://vercel.com/account/tokens>. Read scope is enough; this
tool never writes.

Vercel's three APIs scope differently, and a project scoped token silently
reaches only one of them:

| Preset family | API scoped by | Project scoped token |
| --- | --- | --- |
| Web Analytics (`overview`, `top-pages`, `events`, ...) | `projectId` | works |
| Speed Insights (`vitals`, `slowest-pages`, ...) | account | `404 Observability Data not found.` |
| Request logs (`logs`, `errors`, `error-summary`) | account, as an `ownerId` parameter | expected to fail with `403`; only an account or team scoped token was available to test |

To see what the current token can actually reach:
`npx vercel@latest metrics schema`.

### Turning the features on

Web Analytics and Speed Insights are two separate per-project switches, each
with its own package in the app: `@vercel/analytics`
(<https://vercel.com/docs/analytics/quickstart>) and `@vercel/speed-insights`
(<https://vercel.com/docs/speed-insights/quickstart>). Data exists only from the
moment each is turned on, and only from deployed builds, not local development.

`--list-projects` reports both per project: `data` collected, `empty` for
enabled but nothing yet, `off` for not enabled.

Request logs need no switch. Any deployed project produces them, which is why the
listing has no third column: there is nothing to enable. It also means an empty
logs answer is never explained by a feature being off, and retention is the thing
to check instead.

### Environment variables

Every one has a matching flag that takes precedence.

```bash
export VERCEL_TOKEN="vercel_tok_xxxxxxxxxxxxxxxxxxxxxxxx"
export VERCEL_PROJECT_ID="prj_XXXXXXXXXXXXXXXX"   # or just use --project
# export VERCEL_TEAM_ID="team_XXXXXXXXXXXXXXXX"   # team-owned projects
# export VERCEL_ORG_ID="team_XXXXXXXXXXXXXXXX"    # written by `vercel link`
```

The first line is the one to be careful with, and only the first: the others are
not secrets. A real token typed after `export` is recorded in your shell history
file and is readable in a process listing while the command runs, so prefer a
prompt, `printf 'Vercel token: '; read -rs VERCEL_TOKEN; echo; export
VERCEL_TOKEN`, or a file that only your user can read.

`.env.example` documents all of them. Nothing is read from or written to a file
by the tool itself, so load them however you like:
`set -a; . ./.env; set +a`. A `.env` holding a real token is a secret at rest:
`chmod 600` it, and keep it out of git, out of container images and out of
backups. Use the least privileged read token Vercel will issue, so that a copy
you lose track of is worth as little as possible.

## What it looks like

Real output from the code, with synthetic data. The full set for every preset is
in [examples/example_outputs.md](examples/example_outputs.md).

### Traffic, at a glance

Bare `vercel-insights` gives you the last 7 days.

```console
$ vercel-insights --since 7d
Vercel Web Analytics: prj_9RkQm2vT7xLpN4dWbYcF3sJz
Range: 2026-08-09T05:23:38Z to 2026-08-16T05:23:38Z (UTC)

  pageviews  48,072
  visitors   32,280
  visitors is a sum of the buckets below, so someone who came on two days counts twice;
  run the total preset for distinct visitors over the window

By day
  2026-08-08  6,120  ██████████████████
  2026-08-09  4,980  ██████████████
  2026-08-10  7,840  ███████████████████████
  2026-08-11  8,310  ████████████████████████
  2026-08-12  7,905  ███████████████████████
  2026-08-13  7,402  █████████████████████
  2026-08-14  5,515  ████████████████

Top pages (top 5)
requestPath            pageviews  visitors  % pageviews
---------------------  ---------  --------  -----------
/                         18,420    11,930        38.3%
/docs/getting-started      9,310     6,845        19.4%
/pricing                   7,204     5,588        15.0%
/blog/shipping-faster      4,126     3,390         8.6%
/changelog                 2,870     2,115         6.0%
Others                     6,142     4,102        12.8%
---------------------  ---------  --------  -----------
TOTAL                     48,072    33,970       100.0%

Others is not a real value: it is every group beyond --limit 5, collapsed by the API into one bucket.

Top referrers (top 5)
referrerHostname      pageviews  visitors  % pageviews
--------------------  ---------  --------  -----------
(none)                   21,044    13,980        43.8%
google.com               14,310     9,720        29.8%
news.ycombinator.com      6,890     6,012        14.3%
github.com                3,402     2,560         7.1%
x.com                     2,426     1,798         5.0%
--------------------  ---------  --------  -----------
TOTAL                    48,072    34,070       100.0%
```

### Your Core Web Vitals against Vercel's targets

```console
$ vercel-insights vitals
Vercel Speed Insights: prj_9RkQm2vT7xLpN4dWbYcF3sJz
Range: 2026-08-08T00:00:00Z to 2026-08-15T00:00:00Z (UTC)

metric                        p75  target  verdict
-------------------------  ------  ------  ------------
Largest Contentful Paint    2.9 s   2.5 s  over target
Interaction to Next Paint  184 ms  200 ms  meets target
Cumulative Layout Shift     0.128   0.100  over target
First Contentful Paint      1.6 s   1.8 s  meets target
Time to First Byte         412 ms  800 ms  meets target

Lower is better for all five metrics.
The target is Vercel's published 'good' threshold, so the verdict is two tier: meets target or over target.
Real Experience Score is not queryable through this API; read it on the Speed Insights dashboard.
```

### Which pages are slow, and for whom

```console
$ vercel-insights slowest-pages
Vercel Speed Insights: prj_9RkQm2vT7xLpN4dWbYcF3sJz (slowest-pages, p75)
Range: 2026-08-08T00:00:00Z to 2026-08-15T00:00:00Z (UTC)

route         p75_lcp
------------  -------
/blog/[slug]    5.0 s
/docs/[slug]    3.2 s
/pricing        2.7 s
/               2.2 s

Metric: vercel.speed_insights.lcp_ms (Largest Contentful Paint)
Target: 2.5 s or less
Lower is better for all five metrics.
The target is Vercel's published 'good' threshold, so the verdict is two tier: meets target or over target.
```
```console
$ vercel-insights vitals-by-device
Vercel Speed Insights: prj_9RkQm2vT7xLpN4dWbYcF3sJz (vitals-by-device, p75)
Range: 2026-08-08T00:00:00Z to 2026-08-15T00:00:00Z (UTC)

device_type  p75_lcp
-----------  -------
mobile         4.1 s
tablet         3.0 s
desktop        2.1 s

Metric: vercel.speed_insights.lcp_ms (Largest Contentful Paint)
Target: 2.5 s or less
Lower is better for all five metrics.
The target is Vercel's published 'good' threshold, so the verdict is two tier: meets target or over target.
```

The device breakdown is usually the answer to "why is the field score worse than
my local numbers".

### Anything else, machine readable

```bash
vercel-insights devices --json | jq '.rows[] | {(.key): .metrics.pageviews}'
vercel-insights trend --granularity week --since 8w --csv > traffic.csv
```

## Errors and request logs

The question nobody asks a dashboard calmly: **what is broken right now.**

```bash
vercel-insights errors --since 30m
```

That is one command against your project's runtime request logs, and it is the
third API this tool talks to. Traffic tells you how many people came, Speed
Insights how fast it felt for them, and request logs what failed while they were
there: the status a request answered, the log lines it printed, the route, the
deployment, the region.

Three presets, all read-only, all against the same endpoint:

- **`errors`** is the headline. It issues two queries, one for `5xx` responses and
  one for `error` and `fatal` log lines, and merges them. That is not
  belt-and-braces: on this API the level filter matches what a request *printed*
  and the status filter matches what it *answered*, so a 500 that crashed
  silently and a 200 whose handler logged a stack trace each show up in exactly
  one of the two. Either query alone gives you half the picture.
- **`logs`** is the same table without the error filter: the most recent requests,
  whatever their status. Use it with `--search`, `--request-id` or
  `--status-code 4xx` when you know what you are looking for.
- **`error-summary`** groups the same errors three ways, by status, by route and
  by exact message, which is the "where is this concentrated" view.

### What a log line can carry

Read this before running a logs command, because it is the one thing about this
feature that cannot be fixed in code.

A log line is whatever your application printed. Applications print API keys,
connection strings, session identifiers, email addresses and customer records
into their logs far more often than anyone intends, and this surface prints those
lines exactly as they were logged.

This tool redacts exactly one secret: the Vercel token it is holding, wherever a
response echoes it back, in every output format including `--json`. That is the
only string it can recognise. It cannot tell your API key from ordinary log text,
so nothing else is redacted and nothing else can usefully be: a pattern matcher
aggressive enough to catch an unknown secret would also mangle the stack traces
this feature exists to show, and a redactor you cannot trust is worse than one
you know the limits of.

So treat log output as sensitive by default:

- **Quote the lines that answer the question**, not the whole table. A screen of
  rows is rarely the answer to anything.
- **Do not forward it.** An issue tracker, a chat channel, a paste service or
  another API is a copy you no longer control, made of text you did not write.
- **`--json` and `--csv` need more care, not less.** They carry the whole row as
  the API sent it, including the fields the table has no column for.
- **The same goes for anything an agent relays.** The guidance in `SKILL.md`
  tells it to quote the minimum and forward nothing, which is worth knowing if
  you are the one reading its summary.

Here is a real run, captured against a live account and then redacted. The
shape, the columns and every note are exactly what it printed; the project id,
the route names and the timestamps were replaced afterwards with fictional
equivalents, because a real account's identifiers do not belong in a published
file. Read your own output the same way before you share it: it carries your
project id, your route names and whatever your application logged.

```console
$ vercel-insights logs --since 30m --limit 5
Vercel request logs: prj_ExampleRedactedProjectId0000 (logs, last 30 minutes)
Range: 2026-08-17T09:18:19Z to 2026-08-17T09:48:19Z (UTC)

time      level  status  method  route                             source                 message
--------  -----  ------  ------  --------------------------------  ---------------------  -------
09:47:59  -         200  GET     /api/teams/[teamId]               serverless
09:47:59  -         401  GET     /api/me                           serverless
09:47:59  -         200  GET     /api/documents/[slug]             serverless
09:47:59  -         200  GET     /robots.txt                       serverless
09:47:59  -         200  GET     /[locale]/t/[teamId]/[documentS…  serverless-middleware

Showing the most recent 5 of more requests that matched in 30 minutes: 4 x 200, 1 x 401.
More rows matched than were shown. Raise --limit (up to 200) or narrow the window.
Add --expand for full messages, or --request-id to pull one request apart.
```

The `level` column is `-` on every row because none of those requests printed
anything, which is the normal case. `--level error` would have matched none of
them, and that is the trap this surface sets: a filter that matches nothing
answers `200` with zero rows, and zero rows reads like a healthy site. Every
vocabulary is therefore checked before the request goes out, so a typo is a
refusal rather than a reassuring lie.

Three details in that footer and table are deliberate. The count says *showing
the most recent 5 of more that matched*, because `--limit 5` cut the table and
five rows are a sample rather than the half hour. There is no "most affected
route" line: all five routes are distinct, so nothing leads, and printing
whichever sorted first would dress up a tie as a finding. And the last route is
too long for its column, so it is cut with an ellipsis; the `source` column shows
`serverless-middleware`, which is the spelling this API *displays* while the
filter that matches those rows is `--source edge-middleware`, a mismatch the tool
resolves for you.

### An empty answer is not a clean bill of health

This is what it looks like when nothing failed, and it is the case most worth
recognising:

```console
$ vercel-insights errors --since 24h
Vercel request logs: prj_ExampleRedactedProjectId0000 (errors, last 24 hours)
Range: 2026-08-16T06:34:31Z to 2026-08-17T06:34:31Z (UTC)
Counted as an error: a 5xx response, a crashed function, or a request that logged an error or fatal line.

No request logs for project prj_ExampleRedactedProjectId0000 between 2026-08-16T06:34:31Z and 2026-08-17T06:34:31Z.

Runtime log retention is 1 hour on Hobby, 1 day on Pro, 3 days on Enterprise and 30 days with Observability Plus, so an empty result over a longer window can mean the logs aged out rather than that nothing failed.
```

Exit code 0: no errors is an answer, not a failure. The last line is there because
runtime logs are kept for far less time than analytics data, so "no errors in the
last 24 hours" can mean "nothing failed" or "the logs for most of that window are
already gone", and the tool will not pretend to know which:

| Plan | Runtime log retention |
| --- | --- |
| Hobby | 1 hour |
| Pro | 1 day |
| Enterprise | 3 days |
| Pro or Enterprise with Observability Plus | 30 days |

That is why the logs presets do not use the 7 day default the rest of the tool
has: `logs` and `errors` look back 1 hour, `error-summary` 6 hours. Widen it with
`--since` when you need to, and read an empty wide window with the retention line
in mind. A 4xx is deliberately not an error here, by the way: a 401 on `/api/me`
is the application working. `logs --status-code 4xx` asks for those by name.

### Why this one reaches a second host

Every other endpoint this tool calls is on `api.vercel.com`. Request logs are on
`vercel.com`, which is worth explaining rather than hiding: it is the endpoint
Vercel's own `vercel logs` command calls, and there is no equivalent on the API
host. The documented streaming endpoint never returns response headers to a
request-and-response client, and counting errors through the metrics API answers
`402 payment_required` without the Observability Plus add-on, while request logs
work without it. So this is the only endpoint here that is absent from Vercel's
published OpenAPI document, and it could change without notice. Every claim this
project makes about it was probed against a live account and is written down, with
its date, in [docs/api-notes.md](docs/api-notes.md).

There is no live tail, for the same reason: the streaming endpoint is unusable
here. A logs command answers one window and exits.

## Beyond web vitals

Speed Insights is one family among many on the same query API. Function
invocations, edge requests, image transformations, ISR operations, firewall
actions and AI gateway usage are all queryable by id:

```console
$ vercel-insights --list-metrics                      # what this account can reach
$ vercel-insights --metric vercel.function_invocation.count --aggregation sum
$ vercel-insights --metric vercel.request.count --group-by route --limit 10
```

Metric ids are not hardcoded here. `--list-metrics` asks the API, which is the
only thing that knows what your account can reach, and it prints each metric's
unit, aggregations and dimensions so you know what to group by.

For a metric outside the five web vitals this tool claims nothing it cannot
know: no unit, so the value is a plain number rather than being labelled seconds
on a guess; no target, so no verdict; and no aggregation is sent unless you name
one, so the server applies the metric's own default rather than a percentile
that may be meaningless for a count.

> **Plan note.** Web Analytics and Speed Insights are queryable on any plan.
> Every other metric requires
> [Observability Plus](https://vercel.com/docs/observability/observability-plus).
> Without it these queries return an error, which is a plan limit rather than
> anything this tool can work around.

> **Scope note, and it is the more important of the two.** These two flags are
> the widest thing here. `--list-metrics` asks the account what it can query and
> `--metric` queries any of it, which was 96 metrics on the account this was
> probed against: functions, edge requests, caching, firewall actions, AI gateway
> usage. It is read-only and it is the same fixed endpoint as `vitals`, but an
> account-scoped token does mean this tool can read **every metric that account
> can see**, not only the web vitals in the section above. If that is wider than
> you want, scope the token narrower and know what it costs: Speed Insights and
> request logs both need account or team scope, so a project-scoped token buys a
> smaller surface at the price of two of the three features. The scope table in
> [The token, and why its scope matters](#the-token-and-why-its-scope-matters)
> lays out which is which.

## Guarding performance in CI

`--budget` turns a measurement into a pass or a fail, so a regression can stop a
build instead of being noticed later:

```console
$ vercel-insights vitals --since 7d --budget lcp=2500 --budget inp=200 --budget cls=0.1

Budgets
  pass    Largest Contentful Paint      2.4 s against 2.5 s
  fail    Interaction to Next Paint    205 ms against 200 ms
at least one budget was exceeded, so this run exits 3
```

Exit **3** means a budget was exceeded, which is deliberately not 1: a failing
budget is a successful run reporting bad news, and a CI step usually wants to
tell that apart from the API being down. A metric with no data does not fail,
because an empty window means the measurement is missing rather than the site
being slower.

A ready-to-copy workflow is in
[`examples/github-action-budget.yml`](examples/github-action-budget.yml). Note
it is scheduled rather than run per commit: these are real user measurements,
so they accumulate from visitors over time and do not change the moment a deploy
lands.

## Presets

`vercel-insights --list-presets` prints this table at any time. The preset is
the optional first positional argument; with no arguments the tool runs
`overview`.

### Web Analytics

| Preset | Dataset | Groups by | Default limit | What it shows |
| --- | --- | --- | --- | --- |
| `overview` (default) | visits | `day`, then `requestPath`, then `referrerHostname` (3 calls) | 5 per table | Totals, a daily trend, top pages and top referrers |
| `trend` | visits | `day` | 100 | Page views over time; change buckets with `--granularity` |
| `top-pages` | visits | `requestPath` | 10 | Most viewed URL paths |
| `top-routes` | visits | `route` | 10 | Most viewed framework routes, for example `/blog/[slug]` |
| `referrers` | visits | `referrerHostname` | 10 | Where the traffic came from |
| `countries` | visits | `country` | 10 | Traffic by country |
| `devices` | visits | `deviceType` | 10 | Traffic by device type |
| `browsers` | visits | `browserName` | 10 | Traffic by browser |
| `operating-systems` | visits | `osName` | 10 | Traffic by operating system |
| `campaigns` | visits | `utmCampaign` | 10 | Traffic by `utm_campaign` (needs Web Analytics Plus) |
| `events` | events | `eventName` | 10 | Custom events; add `--event-property NAME` to break one out |
| `total` | visits | nothing, one ungrouped count | n/a | One total for the window, production only |

### Speed Insights

| Preset | Metric | Groups by | Default limit | What it shows |
| --- | --- | --- | --- | --- |
| `vitals` | all five (5 calls) | nothing | n/a | P75 of every web vital against its published target |
| `slowest-pages` | `lcp` | `route`, worst first | 10 | Routes with the worst P75 LCP |
| `fastest-pages` | `lcp` | `route`, best first | 10 | Routes with the best P75 LCP |
| `vitals-by-country` | `--metric`, default `lcp` | `country` | 10 | Where in the world the site is slow |
| `vitals-by-device` | `--metric`, default `lcp` | `device_type` | 10 | Mobile against desktop against tablet |
| `vitals-trend` | `--metric`, default `lcp` | time, `1d` by default | n/a | Whether it is getting better or worse |
| `data-points` | `<metric>_count` | `route` | 10 | How many measurements each route contributed |

### Request logs

| Preset | Queries | Default window | Default limit | What it shows |
| --- | --- | --- | --- | --- |
| `logs` | 1 call | 1 hour | 50 rows | Recent requests, newest first, whatever their status |
| `errors` | 2 calls, merged | 1 hour | 50 rows | Failing requests: 5xx responses and logged error or fatal lines |
| `error-summary` | the same 2 calls | 6 hours | 200 rows | The same errors tallied by status, by route and by message |

Any explicit flag overrides a preset value, with three exceptions. `overview`
issues its own three queries, so `--group-by`, `--event-property` and `--csv`
are rejected there. `vitals` issues one query per web vital, so `--group-by`,
`--csv` and `--metric` are rejected there. `error-summary` prints three tables, so
`--csv` is rejected there and points at `errors --csv`. All of them exit 2 and
name a preset to use instead.

A preset also fixes which API is queried, and that is enforced rather than
implied, in every direction: a Speed Insights option is a configuration error on a
traffic or a logs preset, a logs option is one on either analytics preset, and so
on. Nothing is silently ignored. The tables below say which surface each flag
belongs to.

On the two analytics surfaces, groups past the limit are never dropped: they roll
into a single `Others` row that still counts toward the total. A logs preset has
no groups, so its limit counts rows, and rows past it are genuinely left out: the
footer says so rather than letting a cut-off table read as complete.

## Flags

### Configuration

| Flag | Env fallback | Default | Notes |
| --- | --- | --- | --- |
| `--token TOKEN` | `VERCEL_TOKEN` | none | Required for real requests, not for `--dry-run`. |
| `--project ID_OR_NAME` | `VERCEL_PROJECT_ID` | none | Project ID or project name. Required, except on a Speed Insights preset run with `--all`. |
| `--team TEAM_ID` | `VERCEL_TEAM_ID` | none | Team-owned projects. Not with `--team-slug`. |
| `--owner-id ID` | `VERCEL_OWNER_ID`, then `VERCEL_ORG_ID` | resolved | Account owning the project, required by a Speed Insights scope and by request logs. A team is its own owner, so `--team` covers it; otherwise the personal account id is read once from the API. |
| `--team-slug SLUG` | `VERCEL_TEAM_SLUG` | none | Sent as `slug`. Not with `--team`. A slug is a name rather than an account id, so on a Speed Insights or logs preset it cannot stand in for the owner and is refused rather than quietly answering for the wrong account. |

### Query shape

| Flag | Surface | Default | Notes |
| --- | --- | --- | --- |
| `--dataset {visits,events}` | Web Analytics only | preset's choice, usually `visits` | `events` for custom events. Not with `--metric`, and a configuration error on a Speed Insights or logs preset, neither of which has datasets. |
| `--group-by DIM`, `--dimension DIM` | traffic and speed | the preset's grouping | Repeatable, maximum 2. Web Analytics: at most one time bucket. The dimension *names* are not portable: a camelCase name on Speed Insights, or a snake_case one on Web Analytics, is a configuration error. Logs are rows rather than groups, so it is an error there and the message points at `error-summary`. |
| `--granularity BUCKET` | traffic and speed | none | `hour`, `1h`, `day`, `1d`, `week`, `month`, `1mo`, `year`. Both vocabularies accepted and translated per API; `week` and `year` are Web Analytics only, and a configuration error on Speed Insights. Any bucket at all is an error on a logs preset. |
| `--since WHEN` | all three | `7d`, or 1 hour on `logs` and `errors` and 6 hours on `error-summary` | `30m`, `24h`, `7d`, `4w`, `now`, `today`, `yesterday`, `2026-08-01`, `2026-08-01T12:00:00Z`, or Unix ms. |
| `--until WHEN` | all three | `now` | Same forms. Must be strictly after `--since`. |
| `--limit N` | all three | preset's, usually 10 | 1 to 100 on the analytics surfaces, checked before the request. On Web Analytics the overflow becomes `Others`; on Speed Insights it bounds grouped results per time bucket. An ungrouped query (`total`, `vitals`) has nothing to limit, so the value is accepted and goes unused. On a logs preset it counts rows instead, 1 to 200, and rows past it are left out rather than rolled up. |
| `--event-property NAME` | Web Analytics, events dataset only | none | Adds `eventData/NAME` as a second grouping dimension next to `eventName`, and each dimension gets its own column. A configuration error on `visits`, on the other two surfaces, and on `overview`. |

### Speed Insights

Every flag in this table is a Speed Insights option. None of them is universal:
on a traffic preset (`overview`, `trend`, `top-pages`, `top-routes`, `referrers`,
`countries`, `devices`, `browsers`, `operating-systems`, `campaigns`, `events`,
`total`) or a logs preset (`logs`, `errors`, `error-summary`) each one exits 2
with a message naming the presets that do accept it. That is enforced in code, not
a convention. `--budget` is in this table too: it compares a measured value
against a threshold, and only Speed Insights measures one.

| Flag | Default | Notes |
| --- | --- | --- |
| `--metric NAME` | the preset's, usually `lcp` | `lcp`, `inp`, `cls`, `fcp`, `ttfb`. The full id (`vercel.speed_insights.lcp_ms`) and the human label are accepted too. Not with `--dataset`, and a configuration error on `vitals`, which reports all five. |
| `--percentile N` | `75` | One of 75, 90, 95, 99. Sugar for `--aggregation p75` and friends. |
| `--aggregation NAME` | the metric's default | Raw passthrough, for example `sum`, `count`, `min`, `max`, `p90`. Not with `--percentile`. |
| `--order-by COLUMN` | `count` | `count` or `value`. Grouped queries only; without a grouping it is an error. |
| `--order DIRECTION` | `desc` | `asc` or `desc`. Grouped queries only. |
| `--bucket-timezone IANA` | none | Aligns `1d` and `1mo` buckets, for example `Europe/Paris`. Timestamps stay UTC; a sub-daily bucket ignores it and the tool warns. |
| `--all` | off | Query every project in the team, instead of one. Mutually exclusive with `--project`, and a configuration error on every Web Analytics and logs preset: there is no team-wide traffic or logs query, so compare those one `--project` at a time. |
| `--data-points` | off | Report the number of measurements instead of the metric value. Defaults the aggregation to `sum`. |
| `--budget NAME=VALUE` | none | Repeatable, for CI. Exit 3 when a vital exceeds VALUE, for example `--budget lcp=2500`. A metric with no data does not fail. See [Guarding performance in CI](#guarding-performance-in-ci). |

### Request logs

Every flag here is meaningful only on `logs`, `errors` or `error-summary`, and on
any other preset each one exits 2 naming those three. Each value is checked before
the request is built, because this API answers an unknown level or source with
HTTP 200 and zero rows, and zero rows reads as "your site is fine".

| Flag | Default | Notes |
| --- | --- | --- |
| `--level LEVEL` | none | `error`, `warning`, `info`, `fatal`, comma separated. Matches **log lines, not responses**: a 500 that printed nothing does not match it. |
| `--status-code CODE` | none | An integer (`500`), a class (`5xx`, `40x`), `None` for a request with no status recorded, or a comma separated mix. No comparisons: `>=500` is refused, quoting the API's own rule. |
| `--source SOURCE` | none | `serverless`, `edge-function`, `edge-middleware`, `static`. The `source` column can display `serverless-middleware`; pass that and it is rewritten to `edge-middleware`, which is the spelling that actually matches those rows. |
| `--method METHOD` | none | One HTTP method, upper-cased for the wire. Anything outside the standard set warns on stderr and is still sent: a custom method is legal, but this API answers a method it never recorded with zero rows rather than an error. |
| `--search TEXT` | none | Free text and nothing more. Not a query syntax, so do not expect `status:500` to filter by status: use `--status-code` for that. |
| `--request-id ID` | none | One request, by the id shown in the table. Pair it with `--expand`. |
| `--branch NAME` | none | Only deployments built from this git branch. |
| `--deployment ID` | none | One deployment, by its `dpl_` id. |
| `--expand` | off | Print every full log line under its row instead of truncating the message to its column. |

### Filters

On the analytics surfaces each adds one OData clause and all clauses are joined
with `and`; a comma-separated value becomes an `in (...)` set, so
`--country US,CA,MX` is one clause. The dimension name compiles to the spelling of
whichever surface is active. On the logs surface these are query parameters
instead, and `--path` and `--route` match exactly, so `--search` is the substring
tool there.

| Flag | On Web Analytics | On Speed Insights | On request logs |
| --- | --- | --- | --- |
| `--path VALUE` | `requestPath eq 'VALUE'` | `request_path eq 'VALUE'` | `requestPath=VALUE`, exact |
| `--route VALUE` | `route eq 'VALUE'` | `route eq 'VALUE'` | `route=VALUE`, exact |
| `--country VALUE` | `country eq 'VALUE'` | `country eq 'VALUE'` | not collected, configuration error |
| `--device VALUE` | `deviceType eq 'VALUE'` | `device_type eq 'VALUE'` | not collected, configuration error |
| `--environment {production,preview}` | `environment eq 'VALUE'` | `environment eq 'VALUE'` | `environment=VALUE` |
| `--browser VALUE` | `browserName eq 'VALUE'` | not collected, configuration error | not collected, configuration error |
| `--os VALUE` | `osName eq 'VALUE'` | not collected, configuration error | not collected, configuration error |
| `--referrer VALUE` | `referrerHostname eq 'VALUE'` | not collected, configuration error | not collected, configuration error |
| `--utm-source VALUE` | `utmSource eq 'VALUE'` | not collected, configuration error | not collected, configuration error |
| `--utm-medium VALUE` | `utmMedium eq 'VALUE'` | not collected, configuration error | not collected, configuration error |
| `--utm-campaign VALUE` | `utmCampaign eq 'VALUE'` | not collected, configuration error | not collected, configuration error |
| `--event-name VALUE` | `eventName eq 'VALUE'`, events dataset only | no custom events, configuration error | no custom events, configuration error |
| `--flag NAME=VALUE` | `flags/NAME eq 'VALUE'`, repeatable. A name with punctuation is quoted for you: `--flag my-flag=on` builds `flags/'my-flag' eq 'on'` | no feature flags, configuration error | no feature flags, configuration error |
| `--filter ODATA` | appended verbatim, repeatable | appended verbatim, repeatable | no OData at all, configuration error naming the flags that do filter |

Web Analytics accepts `eq`, `ne`, `in`, `and`, `or`, `not`, parentheses and
`startswith`. It has no comparison operators, so `gt`, `lt`, `ge` and `le` do
not work in a `--filter` there. Speed Insights accepts the same set plus
`endsWith` and the numeric comparisons `>`, `>=`, `<`, `<=`. Raw `--filter` text
is passed through unvalidated on both, so a clause the API refuses comes back as
its own 400 with Vercel's message.

### Output and behaviour

| Flag | Default | Notes |
| --- | --- | --- |
| `--json` | off | Machine readable, with the API payload under `raw`, unaltered except that this tool's own token is rewritten out of a logs row. Not with `--csv`. On a logs preset each entry carries the whole original row under its own `raw` key. |
| `--csv` | off | `csv.writer` quoting. Not with `--json`, and not with `overview`, `vitals` or `error-summary`, each of which prints several tables. On a logs preset the rows go to stdout and the report's notes to stderr, so a redirected file holds only data and the truncation and retention caveats are still on screen. |
| `--dry-run` | off | Print the request, send nothing, no token needed. Prints the full JSON body on a POST. |
| `--timeout SECONDS` | `30.0` | Per request. Must be a finite number greater than 0; anything else is a usage error. |
| `--max-retries N` | `3` | Retries after the first attempt. Only 408, 429 and 5xx responses and network failures are retried. |
| `--no-color` | auto | Also honours `NO_COLOR` and a non-TTY stdout. |
| `--verbose` | off | Diagnostics on stderr. Never the token. |
| `--list-presets` | | Print the preset table and exit 0. |
| `--version` | | Print the version and exit 0. |

Exit codes: `0` success including an empty result, `1` API or network failure,
`2` configuration or usage error, `3` a `--budget` was exceeded, `130`
interrupted. An empty logs answer is a `0`: no errors is an answer, not a failure.

## Security and permissions

- **Read-only against a six-endpoint allowlist.** One module-level table in
  `vercel_insights/http.py` maps an operation key to a fixed method and URL, and
  it has exactly six entries:

  | Method | Endpoint | What for |
  | --- | --- | --- |
  | GET | `/v1/query/web-analytics/{dataset}/{endpoint}` | traffic |
  | POST | `/v2/observability/query` | speed, and any other metric |
  | GET | `/v2/observability/schema` | which metrics this account can query |
  | GET | `/v9/projects/{project}` | the owning account id, read at most once per run |
  | GET | `/v10/projects` | `--list-projects` |
  | GET | `https://vercel.com/api/logs/request-logs` | request logs |

  The dispatcher takes an operation key, never a method and never a host, so no
  user input can select, extend or override an entry. There are exactly two HTTP
  call sites in the package, `session.get` and `session.post`, and both are
  inside that dispatcher.
- **Two hosts, and the second one is worth knowing about.** Five of those six are
  on `api.vercel.com`. Request logs are served from the dashboard host,
  `vercel.com`, because that is the endpoint Vercel's own `vercel logs` command
  calls and there is no equivalent on the API host: the documented streaming
  endpoint never answers a request-and-response client, and the metrics route
  needs the Observability Plus add-on. It is a GET, the whole query travels in
  the query string, and it is the one endpoint here that is absent from Vercel's
  published OpenAPI document, so it could change without notice. The host set is
  asserted in the test suite, so a third host cannot be added quietly.
- **The allowlist binds every hop, not just the first.** Both call sites pass
  `allow_redirects=False`, and any 3xx is turned into an error rather than
  followed. That is what keeps a redirect from an allowlisted URL from carrying
  the `Authorization` header off to whatever host a `Location` header names. The
  error reports the location it refused, so a proxy or a captive network in the
  way is visible rather than silent.
- **Log text is scrubbed of this tool's own token on the way in.** A log line is
  whatever an application printed, so a response on the logs surface can echo
  back the very token that fetched it. Every string in every row, `--json`
  included, is rewritten at the point the response is parsed, which is the one
  boundary a rendering path cannot skip. That covers the one secret this tool
  knows about. It cannot tell your own API key or connection string from ordinary
  log text, so no general redaction is claimed: what your application logged is
  what you will see.
- **Why one is a POST, and why it is still a read.** Vercel exposes no GET
  equivalent for an observability query. Speed Insights has no query API of its
  own, and the general observability surface takes its query in a JSON request
  body because a query is too structured for a query string. Nothing is created,
  updated or deleted: the body is the question, not a change. The endpoints in
  the same API that genuinely write, `/speed-insights/toggle` and
  `/web/insights/toggle`, which enable and disable the features, are absent from
  the allowlist and unreachable from any code path here. This tool cannot change
  deployments, projects, domains, environment variables or settings.
- **The token is never logged.** It is placed only in the `Authorization`
  header, never in a URL, a query parameter, a request body, a log line, an
  exception message, or any formatter output. `--verbose` and error paths render
  headers through a redactor that replaces the credential with
  `Bearer <redacted>`, and any message on its way into an error is scrubbed of
  the credential first.
- **A malformed token is caught before a request exists.** A value carrying a
  newline, another control or non-ASCII character, or a leading or trailing
  space is rejected with exit code 2 before any request object is built, and the
  message reports the length, the position and the character class only. The
  token itself is never printed. One nuance worth knowing: surrounding
  whitespace on `VERCEL_TOKEN` is trimmed as the environment is read, so a
  trailing newline picked up from a shell here-doc is fixed rather than
  reported; the same value passed with `--token` is reported instead.
- **`--dry-run` proves it.** It prints the full request, including the encoded
  URL and, for the POST operation, the complete JSON body. It never constructs
  an HTTP session and works with no token in the environment. Run it first when
  you want to know exactly what will be sent.
- **Scopes.** A standard Vercel access token with read access is enough. For a
  team-owned project the token must belong to an account with access to that
  team, and the team must be identified with `VERCEL_TEAM_ID` or
  `VERCEL_TEAM_SLUG`. No write scope is used or needed.
- **The token comes from the environment.** `VERCEL_TOKEN`, or `--token` when
  you would rather pass it explicitly. It is not read from, or written to, any
  file. Nothing is cached to disk: this tool performs no filesystem writes at
  all.
- **No dynamic execution.** No `eval`, no `exec`, no `subprocess`.

## Plans, windows and what is out of reach

**Reporting window.** Analytics data is only guaranteed to be queryable for a
limited period, and it depends on the plan:

| Plan | Reporting window |
| --- | --- |
| Hobby | 1 month |
| Pro | 12 months |
| Pro with Web Analytics Plus | 24 months |
| Enterprise | 24 months |

A `--since` beyond your plan's window is still a legal query, it just tends to
come back empty. The plan tier is not discoverable through this API, so the tool
warns on stderr past 24 months rather than blocking anything.

**Runtime logs are a different clock.** The window above is for analytics data.
Request logs are kept for 1 hour on Hobby, 1 day on Pro, 3 days on Enterprise and
30 days with Observability Plus, which is why an empty logs answer over a wider
window prints those figures instead of implying health. See
[Errors and request logs](#errors-and-request-logs).

**Plan-gated features.** Custom events need Pro or above, and UTM dimensions
need Web Analytics Plus or Enterprise. Below those tiers the queries return
nothing rather than failing. **Speed Insights needs no Observability Plus**:
Vercel documents its metrics as readable on the query surface without it, and
unlike the Web Analytics count endpoints it collects on every deployed
environment, preview included. **Request logs need none either**, which is the
reason they are the right surface for an error question: counting errors through
the metrics API instead (`--metric vercel.request.count --group-by http_status`)
answers `402 payment_required` without the add-on, and no flag fixes that.

**No live tail.** Vercel's documented streaming logs endpoint never returns
response headers to a request-and-response client, so there is no follow mode
here. Run a short `--since` again to see what has happened since.

**Real Experience Score is dashboard-only.** Vercel states that RES is not
available through the query API this tool uses, so it is not queryable here and
this client will not substitute another metric for it. Read it on the Speed
Insights tab of the project dashboard. The five vitals it is derived from are
all queryable, and `vitals` reports them together.

## More

- [examples/example_outputs.md](examples/example_outputs.md) for fuller sample
  output.
- [docs/api-notes.md](docs/api-notes.md) for the verified facts about all three
  APIs, including the response shapes, the parsing traps, what the published
  OpenAPI document does and does not pin down, and every live probe behind the
  request logs endpoint, which it does not cover at all.
- [docs/cli-contract.md](docs/cli-contract.md) for the authoritative interface.
- [CONTRIBUTING.md](CONTRIBUTING.md) to add a preset or report a bug.

## License

MIT-0 (MIT No Attribution). See [LICENSE](LICENSE).
