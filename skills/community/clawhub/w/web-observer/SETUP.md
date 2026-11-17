# Setting up Web Observer

Step by step, from nothing to a monitor that messages you. Uptime first, because
it needs no credentials; the other two modules are optional and can be added at
any time.

Throughout, `<skill-dir>` is where the skill was installed, usually
`~/.openclaw/workspace/skills/web-observer`.

## 1. Install it

```bash
openclaw skills install git:https://github.com/anatoli-iliev/web-observer --as web-observer
openclaw skills check
```

It should report as ready immediately. It requires only `node`, and nothing in
`requires.env`, so there is no credential to configure before it becomes visible
to the agent.

## 2. Find out where the configuration goes

```bash
node <skill-dir>/lib/cli.js doctor
```

It will report `no_config` and name the file it expects, normally
`~/.openclaw/web-observer/config.json`. Copy the example there:

```bash
mkdir -p ~/.openclaw/web-observer
cp <skill-dir>/examples/config.json ~/.openclaw/web-observer/config.json
```

## 3. Write down what to watch

Edit that file. The smallest useful version:

```json
{
  "notify": { "channel": "telegram", "to": "telegram:123456789" },
  "uptime": {
    "watches": [{ "id": "site", "url": "https://example.com", "intervalMinutes": 5 }]
  }
}
```

### Finding your `notify.to`

It is the target OpenClaw already delivers to. If you have any cron job that
messages you, copy it from there:

```bash
openclaw cron list
```

The `Delivery` column shows entries like `announce -> telegram:123456789`. The
part after `->` is exactly what `notify.to` wants, and `telegram` is
`notify.channel`. Otherwise `openclaw directory self` will look it up.

### Checking a page that returns 200 while being broken

A 200 is not proof a page works. If your site renders an error page with a 200,
match on the body instead:

```json
{ "id": "site", "url": "https://example.com", "expectBody": "Sign in" }
```

Pick a string that appears only when the page really rendered. `expectBodyRegex`
takes a pattern instead. A body test cannot be combined with `method: "HEAD"`,
because HEAD returns no body, and the configuration refuses that combination
rather than silently passing.

## 4. Try it before scheduling anything

```bash
node <skill-dir>/lib/cli.js check
```

This checks everything immediately, whatever the intervals say, and prints a
table. It deliberately does not touch alert state, so you can run it as often as
you like without consuming the one alert a real outage is entitled to.

To see what an alert would look like without sending one:

```bash
node <skill-dir>/lib/cli.js watch --dry-run
```

The message goes to stderr, `NO_REPLY` goes to stdout, and nothing is saved.

## 5. Schedule it

```bash
node <skill-dir>/lib/cli.js schedule
```

This prints the `openclaw cron add` commands your configuration calls for and
changes nothing. Read them, then either run them yourself or let the tool do it:

```bash
node <skill-dir>/lib/cli.js schedule --apply
openclaw cron list
```

Re-running `--apply` skips any job that already exists rather than creating a
second one, so it is safe to run again after editing the configuration. If you
change `tickMinutes` or an interval, remove the job and re-apply:

```bash
openclaw cron rm web-observer-uptime
node <skill-dir>/lib/cli.js schedule --apply
```

## 6. Confirm the whole path works

```bash
node <skill-dir>/lib/cli.js doctor
```

Everything should read `ok`. To prove delivery end to end, point a throwaway
watch at a host that does not exist, with `failureThreshold: 1`, and wait one
tick. You should get a message. Then remove it.

## Adding the Vercel module

### The token

One token, scoped to the **account or team**, not to a single project. A
project-scoped token reads traffic but returns 404 on Speed Insights and is
refused on request logs, and "not found" reads like "no data" rather than "this
token cannot ask".

```bash
openclaw config set skills.entries.vercel-insights.apiKey YOUR_TOKEN
```

Get one at <https://vercel.com/account/tokens>. Do not paste it into a chat.

### The skill, on the branch that has logs

```bash
openclaw skills install "git:https://github.com/anatoli-iliev/openclaw-vercel-insights#logs-surface" --as vercel-insights --force
```

Traffic and speed work with any version. Request logs need 1.1.0, which is
currently that branch. If you already have an older copy, `--force` replaces it.
Web Observer detects a copy without the logs surface and tells you the version it
found, where it found it, and this command.

### The configuration

```json
{
  "vercel": {
    "enabled": true,
    "project": "my-project",
    "errors": { "intervalMinutes": 15, "windowMinutes": 20, "threshold": 0 },
    "budget": { "intervalMinutes": 360, "metrics": { "lcp": 2500, "inp": 200, "cls": 0.1 } }
  }
}
```

Find the project name with:

```bash
node <skill-dir>/lib/cli.js vercel overview
```

With no project configured, that lists the account's projects instead of
guessing one.

For more than one site, list them under `projects` instead of `project`:

```json
{ "vercel": { "enabled": true, "projects": ["my-project", "my-other-project"] } }
```

Each project is polled separately and keeps its own alert state. Uptime needs no
equivalent: add one entry per URL to `uptime.watches`.

Then test the poll without alerting:

```bash
node <skill-dir>/lib/cli.js vercel-watch --dry-run
node <skill-dir>/lib/cli.js schedule --apply
```

### If your Vercel plan is not Hobby

The defaults assume the shortest retention, one hour. Nothing needs changing:
polling more often than retention is always safe, and the window only ever
reaches back as far as it needs to. On a longer-retention plan you may want a
longer `windowMinutes` for a wider safety margin after downtime.

## Adding the GA4 module

```bash
openclaw skills install git:https://github.com/anatoli-iliev/open-ga4 --as open-ga4
node <skill-dir>/lib/cli.js ga4 doctor --json
```

`open-ga4`'s own doctor walks through the service-account setup one step at a
time. Once it reports `ok`:

```json
{ "ga4": { "enabled": true, "property": "123456789", "digest": { "cron": "0 9 * * 1", "since": "7d" } } }
```

For several sites, write `"properties": ["123456789", "987654321"]` instead of
`property`; the digest gets one section per property.

```bash
node <skill-dir>/lib/cli.js digest --dry-run
node <skill-dir>/lib/cli.js schedule --apply
```

## Troubleshooting

Each row here is a failure that actually happens, with what it looks like.

| Symptom | Cause | Fix |
| --- | --- | --- |
| `doctor` says `no_config` | No configuration file yet | Copy `examples/config.json` to the path it names |
| `doctor` says `no_cron_jobs` | Nothing is scheduled, so nothing runs on its own | `schedule --apply` |
| `doctor` says `no_notify_target` | `notify.channel` or `notify.to` is unset, so a job would have nowhere to deliver | Copy the target from `openclaw cron list` |
| Nothing ever alerts, `check` looks fine | The cron job was never created, or the Gateway is not running | `openclaw cron list`, `openclaw cron status`, `openclaw doctor` |
| `interval_shorter_than_tick` | A watch asks to be checked more often than the job runs, so its real cadence is the tick | Lower `tickMinutes` or raise the interval |
| A configuration key seems to be ignored | It is not: an unknown key is refused | Read the error, which names the key and suggests the closest real one |
| `expectStatus` rejected | A quoted code such as `"200"` | Write a number `200`, or a class `"2xx"` |
| Every check fails with `redirect-off-allowlist` | The URL redirects to a host no watch configures, such as apex to `www` | Watch the final URL, or add the target host as its own watch |
| A watch returns 301 and fails | Redirects are not followed by default | Set `followRedirects: 2`, or add `[300, 399]` to `expectStatus` |
| Vercel errors refuse to run, naming a version | The installed copy predates the logs surface | Run the `#logs-surface` install command above |
| `no Vercel token is configured` on a scheduled run but it works by hand | A cron job runs with the Gateway's environment, which has no skill variables | Set `skills.entries.vercel-insights.apiKey`, so it can be read rather than inherited |
| A `${VAR}` in a skill's config resolves to nothing | The Gateway's environment is not your shell's | Set a literal value, or export the variable where the Gateway can see it |
| `secret reference ... only the Gateway can resolve` | The token is a `SecretRef` | Give Web Observer its own copy: `openclaw config set skills.entries.web-observer.env.VERCEL_TOKEN ...` |
| An error alert arrives with no message text | By design: raw log text is not forwarded | Run `vercel errors` yourself, or set `includeMessages: true` having read the caveat |
| "No request logs" over a long window | Logs age out: 1 hour on Hobby | Not proof of health. Shorten the window, or check the plan |
| A GA4 command says the skill is not installed | It is not | `openclaw skills install git:…/open-ga4 --as open-ga4` |

## If OpenClaw's cron is unavailable

With `cron.enabled: false` or `OPENCLAW_SKIP_CRON=1`, there is a systemd unit and
timer in `examples/`. Install them with:

```bash
mkdir -p ~/.config/systemd/user
cp <skill-dir>/examples/web-observer-monitor.* ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable --now web-observer-monitor.timer
systemctl --user status web-observer-monitor.timer
```

That path calls `openclaw message send` directly, which needs the Gateway
running anyway. Prefer cron when you have it: the cron route is what lets alerts
travel over your configured channel without this skill holding any credential.
