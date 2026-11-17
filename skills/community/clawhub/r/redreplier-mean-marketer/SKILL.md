---
name: redreplier-mean-marketer
description: A background accountability loop that surfaces fresh, high-scoring RedReplier lead opportunities and — if you ignored the last one (didn't approve or reject it) — roasts you, hilariously and meanly, about your marketing until you act. All criteria and the roast itself are computed server-side by RedReplier; this skill just loops and relays. Use when the user wants automated lead nudges, a "marketing accountability" or "roast me into marketing" loop, or to be pinged about new high-relevance Reddit/HN/X/Bluesky leads above a configurable score. Requires a RedReplier account + API key.
homepage: https://redreplier.com
metadata:
  openclaw:
    emoji: 😡
    primaryEnv: REDREPLIER_API_KEY
    requires:
      env:
        - REDREPLIER_API_KEY
      network:
        - ai.redreplier.com
permissions:
  env_read:
    - REDREPLIER_API_KEY
  network_egress:
    - host: ai.redreplier.com
      paths: [/ai-app/api/v1/mean-marketer/*]
      purpose: Read the next lead and the server-generated message. Sends no page content, only the bearer token.
  filesystem_write:
    - path: ~/.config/redreplier/config.json
      mode: "0600"
      purpose: Store the API token when you run `setup`.
  filesystem_read:
    - ~/.config/redreplier/config.json
    - ./.redreplier/config.json
---

# RedReplier Mean Marketer 😡

Your unhinged marketing accountability buddy. On a loop it asks RedReplier for the next
good lead, hands it to you with the link — and if you ghosted the last one it gave you, it
gets **funny-mean** about your marketing until you actually act. Building in public, not
building in private.

> **This skill is intentionally dumb.** Every decision — which leads count, when to get
> mean, how mean, and the exact roast — is made **server-side by RedReplier** and returned
> to you fully formed. Your only jobs are: run `poll` on a cadence, and relay the
> `message` + the opportunity link to the user. Do not write your own insults, do not
> re-rank leads, do not invent criteria. Just loop and relay.

## What it needs

Reuses your existing RedReplier setup. If you installed the base `redreplier` skill, you're
done. Otherwise:

1. Sign up at https://redreplier.com/signup and add the site(s)/keywords to monitor.
2. Settings → API Tokens → generate a dedicated token (starts with `redreplier_`).
3. Provide it via `REDREPLIER_API_KEY`, or store it once:
   ```bash
   ./scripts/mean-marketer.js setup          # prompts, input hidden
   printf %s "$TOKEN" | ./scripts/mean-marketer.js setup   # or pipe it
   ```
   Written to `~/.config/redreplier/config.json` with mode `600`.

> Never pass the token as a command-line argument. Arguments land in shell history and are
> visible to every process on the machine through `ps`. `setup` rejects a `--key` flag for
> exactly that reason.

Base URL `https://ai.redreplier.com/ai-app` · auth `Authorization: Bearer $REDREPLIER_API_KEY`.

## Permissions and data flow

What this skill touches, in full.

| what | detail |
|---|---|
| Env read | `REDREPLIER_API_KEY`, and nothing else |
| Network | `https://ai.redreplier.com/ai-app/api/v1/mean-marketer/*`, and nothing else |
| Sent | Only the bearer token. No page content, no file contents, no local paths |
| Files written | `~/.config/redreplier/config.json`, mode `600`, only when you run `setup` |
| Files read | The same config file, plus `./.redreplier/config.json` if present |
| Shell | None. No subprocesses, no `sudo`, zero dependencies |

The token never appears in a command-line argument. `setup` reads it from a hidden prompt
or from stdin, and refuses a `--key` flag outright. Keep it out of your crontab too: the
cron examples below rely on the stored config file rather than an inline variable, so the
secret stays in one `600` file instead of being copied into `crontab -l` output, process
listings and backups.

To rotate or revoke, delete `~/.config/redreplier/config.json` and generate a new token at
https://redreplier.com/api-tokens.

## Configure the criteria (the user controls this)

All criteria live on the server. Read or change them with `config` — these map to
`GET`/`PUT /api/v1/mean-marketer/config`:

```bash
./scripts/mean-marketer.js config                       # show current config
./scripts/mean-marketer.js config --min-score 60        # only surface leads scoring >= 60 (50-100)
./scripts/mean-marketer.js config --enabled false        # pause the whole loop
./scripts/mean-marketer.js config --profanity false      # keep it savage but swear-free
./scripts/mean-marketer.js config --website <websiteId>  # only nag about one monitored site
```

| Setting | Meaning |
| --- | --- |
| `minScore` | Minimum relevance score (50–100) a lead must hit to be surfaced. Default 50. |
| `enabled` | Master switch for the loop. |
| `profanity` | `true` = swearing on (default). `false` = clean tone, same savagery. |
| `websiteId` | Optional: restrict to a single monitored website. |

## Run it on a schedule — READ THIS, it's the whole point

This skill does **not** poll by itself, and there is **no webhook** — RedReplier's API is
pull-based. Installing the skill only gives you a command. **You (the host agent) MUST create
a recurring job that runs that command**, or nothing will ever happen. This is a required
setup step, not optional.

**Cadence: every 5 minutes.** Reddit/X posts appear continuously, and a lead is only worth
acting on while it's fresh, so poll often. Escalation is time-based on the server, so polling
frequently does **not** make it meaner faster. A 5-minute cadence is safe.

The API allows 600 requests per minute per token, which a 5-minute loop never approaches. If you share the token with other RedReplier automation and start seeing `429`, respect the `Retry-After` header rather than tightening the loop.

### The one command your scheduled job runs

```bash
./scripts/mean-marketer.js notify
```

`notify` polls once and prints **only the user-facing text** (the roast + the opportunity
link), or **prints nothing** when there's nothing to say. So a "notify only when there's
something" job works with zero extra logic: empty output → no message; non-empty → send it to
the user verbatim.

> ⚠️ **Each poll mutates server state** (it hands the lead over and advances the strike
> clock). So the scheduled job must ALWAYS deliver whatever `notify` prints — never run a
> poll just to peek and throw it away, or you'll "consume" a lead silently.

### Set it up — pick your host

**Hermes (cron):** create one cron job, every 5 minutes, no-agent mode, delivering the
script's stdout to your channel. Concretely:
- schedule: `5m`
- script/command: `node ~/.hermes/skills/redreplier/redreplier-mean-marketer/scripts/mean-marketer.js notify` (adjust the path to where the skill is installed)
- no_agent: `true` (the script already formats the message; no model needed to run it)
- deliver: your channel (e.g. Telegram), so the printed roast is sent to you; empty output sends nothing

**OpenClaw (loop):** register a 5-minute background loop that runs the same `notify` command
and relays its stdout to the user.

**Plain cron (any machine):** add to crontab —
```cron
*/5 * * * * cd /path/to/redreplier-mean-marketer && node scripts/mean-marketer.js notify
```
The token is deliberately absent from that line. The script reads it from
`~/.config/redreplier/config.json`, so it never reaches your crontab, `ps` output, or the
backups that copy both. If your scheduler insists on an env var, point it at a file it
sources that you have chmodded `600`, rather than writing the value inline.

Pipe stdout wherever you want it delivered (a notifier, a webhook to Slack, etc.).

### One-off manual check

To test without scheduling anything, just run it once: `./scripts/mean-marketer.js notify`
(prints the message, or nothing). Use `poll` instead if you want the raw JSON.

## What `poll` returns (the raw JSON behind `notify`)

The server returns everything pre-decided. Example:

```jsonc
{
  "enabled": true,
  "minScore": 60,
  "beMean": true,            // server decided you ignored the previous lead
  "tier": 2,                 // 0 friendly · 1 annoyed · 2 pissed · 3 nuclear (informational)
  "strikes": 2,
  "previous": { "id": "…", "status": "NEW", "triaged": false, "hoursOutstanding": 27.4 },
  "opportunity": {           // null if nothing new cleared the threshold
    "id": "…", "title": "…", "url": "https://…", "relevanceScore": 71,
    "source": "REDDIT_POST", "subreddit": "SaaS", "keyword": "…", "relevanceReason": "…"
  },
  "noNewOpportunity": false,
  "message": "…the ready-to-send, server-generated message…"
}
```

Your job each tick is mechanical:

1. **If `message` is non-null, send it to the user as-is.** It's already written in the
   right tone at the right meanness — do not rewrite, soften, or embellish it.
2. **If `opportunity` is present**, include its **link** (`url`) so the user can act, plus
   the score and source for context. (The message already references it.)
3. **If `enabled` is `false`** (`message` is null) or **`noNewOpportunity` is true and
   `beMean` is false**, stay quiet — nothing to say this tick.
4. Do **not** generate your own roast or fabricate leads. Only relay what `poll` returns.

## Closing the loop — approve / reject

When the user replies "approve" / "reject", triage it (this resets the server's strike
count next poll):

```bash
./scripts/mean-marketer.js triage --id <opportunity_id> --status APPROVED   # or REJECTED
```

## Tone & safety

The personality and its guardrails are enforced **server-side** (self-directed marketing
roast, no slurs/targeting, profanity toggle). If the user asks you to tone it down, set
`config --profanity false` rather than editing the message — the server handles the rest.
