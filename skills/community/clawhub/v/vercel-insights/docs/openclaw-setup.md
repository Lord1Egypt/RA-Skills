# Setting this up as an OpenClaw skill

Everything here was checked against a real OpenClaw install (2026.7.1-2) rather
than read out of a help text. Where something is inferred rather than observed,
it says so.

If you only want the command line tool, the README's "Start here" is shorter and
enough. This page is for running it as a skill an agent can call.

## The short version

From ClawHub, which is the shortest route:

```bash
clawhub install vercel-insights

SKILL=~/.openclaw/workspace/skills/vercel-insights
chmod +x "$SKILL/bin/vercel-insights"                       # exec bit is not preserved
python3 -m venv "$SKILL/.venv" && "$SKILL/.venv/bin/python" -m pip install requests

openclaw config set skills.entries.vercel-insights.apiKey \
  --ref-provider default --ref-source env --ref-id VERCEL_TOKEN     # token stays in $VERCEL_TOKEN
openclaw config set skills.entries.vercel-insights.env.VERCEL_TEAM_ID team_...   # team projects only
openclaw skills check
```

From a local checkout, which preserves the exec bit and so needs no `chmod`:

```bash
git clone https://github.com/anatoli-iliev/openclaw-vercel-insights.git
openclaw skills install ./openclaw-vercel-insights --as vercel-insights
openclaw config set skills.entries.vercel-insights.apiKey \
  --ref-provider default --ref-source env --ref-id VERCEL_TOKEN     # token stays in $VERCEL_TOKEN
openclaw config set skills.entries.vercel-insights.env.VERCEL_TEAM_ID team_...   # team projects only
openclaw skills check
```

That `apiKey` line saves a *reference*, not the token: no secret goes on the
command line, and `~/.openclaw/openclaw.json` ends up pointing at the
`VERCEL_TOKEN` environment variable instead of holding a credential. Set that
variable wherever the gateway starts. [Step 4](#4-save-the-token-where-the-gateway-reads-it)
covers it properly, along with the plainer route and what that one costs.

The rest of this page explains each step, and what to do when one of them does
not behave.

> **Both blockers above were found by installing the published skill and running
> it**, not by reading the code. A ClawHub install arrives with
> `bin/vercel-insights` at mode 644 rather than 755, so it fails with
> `Permission denied`; and `requests` is not present on most system
> interpreters. Neither shows up when testing from a source checkout.

---

## 1. Get a token, scoped correctly

<https://vercel.com/account/tokens>. Read scope is enough: this skill never
writes. **Take the least privileged read scope Vercel offers you**, because the
token's reach is the blast radius of any copy of it that gets away: an
account-scoped token can read every project, every analytics dataset and every
request log that account can see, not only the ones you meant to ask about.

**Scope it to the account or team, not to a single project.** This is the single
most common way to end up with a half-working install, because the failure does
not look like a permissions problem:

| Token scope | Traffic presets | Speed presets |
| --- | --- | --- |
| Account or team | work | work |
| Single project | work | `404 Observability Data not found.` |

Vercel serves Speed Insights through an account-scoped observability API, so a
token bound to one project has no account context to resolve and is refused. The
message reads like "your project has no data" but means "this token cannot ask".

To check what a token can actually reach:

```bash
npx vercel@latest metrics schema
```

That lists every metric the credential can query. If `vercel.speed_insights.*`
entries appear, the scope is right. Note that the Vercel CLI prefers the
`VERCEL_TOKEN` environment variable over its own login, so unset it first if you
want to test the CLI's own credentials instead.

## 2. Install the skill

```bash
openclaw skills install /path/to/openclaw-vercel-insights --as vercel-insights
```

Add `--force` to overwrite an existing install.

**Install from a clean clone if you can.** `openclaw skills install <path>`
copies the whole directory and does not honour `.gitignore`, so installing from
a working checkout also copies `.git`, tool caches and any `.venv`: 138 MB
against 828 KB of real content in one measured case. Harmless, but wasteful, and
it is what causes the next problem.

## 3. Make sure it can import `requests`

`requests` is the only runtime dependency. The skill needs an interpreter that
has it.

The launcher at `bin/vercel-insights` prefers a `.venv` sitting beside the skill
and falls back to `python3` on `PATH`, so the usual fix is a virtualenv inside
the installed skill directory:

```bash
SKILL=~/.openclaw/workspace/skills/vercel-insights
python3 -m venv "$SKILL/.venv"
"$SKILL/.venv/bin/python" -m pip install requests
"$SKILL/bin/vercel-insights" --version
```

If you installed from a checkout that already had a `.venv`, it was copied along
with everything else and probably already works, in which case creating one
fails with a permission error on `activate.csh` (the copy is read-only). Check
before rebuilding:

```bash
"$SKILL/.venv/bin/python" -c "import requests; print(requests.__version__)"
```

If that prints a version, skip this step entirely.

Nothing here is installed globally and nothing is written outside the skill
directory. If no interpreter can import `requests`, the tool says so and names
the one it tried, rather than failing with an import traceback.

## 4. Save the token where the gateway reads it

The gateway runs as its own process. **A variable exported in an interactive
shell may never reach it.** So the token has to be somewhere the gateway itself
looks: an environment it inherits, or the config file. Those are the two routes
below, safer one first.

### Recommended: a reference, so the token is not in the config file

`apiKey` accepts a reference as well as a literal:

```bash
openclaw config set skills.entries.vercel-insights.apiKey \
  --ref-provider default --ref-source env --ref-id VERCEL_TOKEN
```

Nothing secret is on that command line, so nothing secret reaches your shell
history or a process listing, and the config file holds a pointer rather than a
credential. The token stays wherever you keep your environment: a systemd unit's
`EnvironmentFile`, a launchd plist, a secrets provider, or a profile file only
your user can read. Set it where the gateway starts, not only in your shell, or
the skill reports a missing token and stays in "Missing requirements".

### The fallback: the token in the config, in plaintext

Simpler, and what most people do. It is worth knowing exactly what it costs:

```bash
openclaw config set skills.entries.vercel-insights.apiKey YOUR_TOKEN
```

> **This stores a secret at rest.** Three consequences, none of them obvious:
>
> - A token pasted on a command line is written to your shell history file, and
>   is readable in a process listing for as long as the command runs. Deleting
>   the history entry afterwards is a patch, not a fix.
> - The value is then in plaintext in `~/.openclaw/openclaw.json`. Anything that
>   can read that file can read this account's Vercel data for as long as the
>   token lives.
> - `config set` writes `~/.openclaw/openclaw.json.bak` on every change, so the
>   previous token survives in the backup too. A synced home directory, a
>   dotfiles repository or an ordinary machine backup carries both copies.
>
> So: `chmod 600 ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak`, keep
> both out of anything that syncs or archives, use the least privileged read
> token Vercel will issue, and rotate it at
> <https://vercel.com/account/tokens> if it has ever been anywhere less private
> than that.

Or in the Control UI (`openclaw dashboard`): **Skills, vercel-insights, Save
key**. That keeps the token off a command line, though the value still lands in
the config file, so the file caveats above still apply.
`openclaw skills info vercel-insights` prints both routes itself.

This works because the skill declares `primaryEnv: VERCEL_TOKEN`, which is what
maps a saved key onto `skills.entries.vercel-insights.apiKey`.

> `openclaw configure --section skills` does **not** prompt for a key. It reports
> skill status and exits. Verified by diffing the config before and after: it
> changed nothing but timestamps.

### By hand

`~/.openclaw/openclaw.json`. This is the plaintext route written out, so every
caveat in the box above applies to it in full. The reference form is written by
`config set --ref-provider ...` rather than by hand here, because how it is
stored was not something this page verified.

```json
{
  "skills": {
    "entries": {
      "vercel-insights": {
        "enabled": true,
        "apiKey": "vercel_tok_...",
        "env": { "VERCEL_TEAM_ID": "team_..." }
      }
    }
  }
}
```

The `env` map takes `"${SOME_VAR}"` to read from the environment instead of
storing a value, which is the same idea as the reference above applied to the
settings that are not secrets. `config set` writes a `.bak` beside the file on
every change, so `cp ~/.openclaw/openclaw.json.bak ~/.openclaw/openclaw.json`
undoes the last one: useful after a mistake, and one more file with your token
in it to keep private.

## 5. Add the team, if the project belongs to one

```bash
openclaw config set skills.entries.vercel-insights.env.VERCEL_TEAM_ID team_...
```

Vercel's Web Analytics documentation is explicit: *"For team projects, find the
team's `teamId` or `slug` and include one in each request. For projects owned by
your personal account, omit `teamId` and `slug`."*

So it is required for a team project and wrong for a personal one, which is why
it is **not** in `requires.env`: that gate is unconditional, and demanding it
would leave every personal account permanently "needs setup". Instead, a traffic
query refused with 403 or 404 while no team is configured says so in the error.

Speed presets do not need it. The owning account is read from the project's own
record, which is what `scope.ownerId` wants. Setting it just saves that lookup.

Find the id under Team Settings, General, or with:

```bash
curl -sS -H "Authorization: Bearer $VERCEL_TOKEN" https://api.vercel.com/v2/teams \
  | python3 -m json.tool | grep -E '"id"|"slug"|"name"'
```

## 6. A default project, optionally

```bash
openclaw config set skills.entries.vercel-insights.env.VERCEL_PROJECT_ID prj_...
```

Entirely optional. Without it the skill lists the account's projects and asks
which one, which is usually what you want with more than one project. Either the
project **name** or its `prj_` id works everywhere.

## 7. Check it

```bash
openclaw skills check
openclaw skills info vercel-insights
```

`vercel-insights` should move out of "Missing requirements" and into "Ready and
visible to model". `skills info` shows which requirements resolved.

Then, from a shell, confirm the tool itself works before involving the agent:

```bash
~/.openclaw/workspace/skills/vercel-insights/bin/vercel-insights --list-projects
~/.openclaw/workspace/skills/vercel-insights/bin/vercel-insights vitals --project <name>
```

---

## Troubleshooting

Every row here is a failure hit during real setup, not a hypothetical.

| What you see | What it means | Fix |
| --- | --- | --- |
| `404 Observability Data not found.` on any speed preset | The token is scoped to a single project. Speed Insights needs account scope. | New token at <https://vercel.com/account/tokens>, scoped to the account or team |
| `404 User not found.` | Same cause, seen through a different endpoint. A project scoped token has no account context. | As above |
| `openclaw skills check` says "needs setup" | `VERCEL_TOKEN` has not resolved | Step 4. Remember the gateway may not see your shell's exports |
| `error: 'requests' is not importable by this interpreter` | The interpreter running the skill lacks the dependency. The message names which one it tried. | Step 3 |
| `Permission denied` running `bin/vercel-insights` | A ClawHub install does not preserve the executable bit, so the launcher arrives at mode 644 | `chmod +x ~/.openclaw/workspace/skills/vercel-insights/bin/vercel-insights` |
| `Permission denied: .../\.venv/bin/activate.csh` | A `.venv` was copied in by the install and is read-only | It probably already works. Test it before rebuilding, per step 3 |
| `openclaw configure --section skills` prompts for nothing | It reports status; it does not prompt | Use step 4 |
| `403` or `404` on a traffic preset | Often a team owned project queried without its team | Step 5. The error says this when no team is configured |
| Traffic works, speed does not | Token scope, every time | Step 1 |
| Empty results, exit code 0 | Genuinely no data in that window, or the feature is off for that project | `--list-projects` shows `data`, `empty` or `off` per project |
| `Granularity ... is not valid` | Speed Insights buckets are `1h`, `1d`, `1w`, `1mo`, `1y`; Web Analytics uses `hour`, `day`, `week`, `month`, `year` | Both spellings are accepted and translated, so this should not happen; report it |
| `the hobby plan only grants access to the latest 7 days of data` | Observability retention on Hobby is 7 days, shorter than Web Analytics' 1 month | Narrow `--since`, or upgrade |

## Exit codes

| Code | Meaning |
| --- | --- |
| 0 | Worked. An empty result is a success: it means no data, not a failure |
| 1 | The API returned an error, or the network failed after retries |
| 2 | The command was configured wrongly. The message names the fix |
| 3 | `--budget` only: the query worked and a threshold was exceeded |

## What this skill can reach

Exactly 6 endpoints, all read-only, fixed in a table in `vercel_insights/http.py`
that no input can extend:

| Method | Endpoint | For |
| --- | --- | --- |
| GET | `/v1/query/web-analytics/{dataset}/{endpoint}` | traffic |
| POST | `/v2/observability/query` | speed, and any other metric |
| GET | `/v2/observability/schema` | `--list-metrics` |
| GET | `/v9/projects/{project}` | resolving a project name and its owner |
| GET | `/v10/projects` | `--list-projects` |
| GET | `https://vercel.com/api/logs/request-logs` | request logs |

Five of those six live on `api.vercel.com`; `request_logs` is the one
exception, served from `vercel.com` instead. The observability query is a
POST because Vercel exposes no GET equivalent; the body carries the question
and nothing is created or changed. The endpoints that would enable or disable
these features are absent from the table entirely.

## Removing it

```bash
openclaw skills uninstall vercel-insights
cp ~/.openclaw/openclaw.json.bak ~/.openclaw/openclaw.json   # if you want the config back too
```
