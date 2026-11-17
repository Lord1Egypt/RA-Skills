# tokei-agent

Control your [Tokei](https://tokei.io) pre-launch and waitlist campaigns from the command line — and from AI agents like Claude Code and OpenClaw. Wraps the Tokei v1 REST API with JSON-only output, zero runtime dependencies.

## Install

```sh
npm install -g tokei-agent
# or run without installing:
npx tokei-agent --help
```

Requires Node 22.12+.

### Claude Code

Install it as a plugin and the `tokei-agent` skill comes with it — Claude then
knows the whole command surface without being told:

```
/plugin marketplace add gilesdawe/tokei-agent
/plugin install tokei-agent@tokei
```

Set `TOKEI_API_KEY` (see [Quick start](#quick-start)) and you're done. The CLI
itself still runs via `npx`, so there is nothing else to install.

## Quick start

1. Create an API key at [tokei.io](https://tokei.io) → Dashboard → Settings → API Keys. Pick **read-only** unless you need to change things; API access requires an active subscription or lifetime plan.

2. Export it — the syntax differs by shell:

```sh
export TOKEI_API_KEY=tokei_k_...          # bash / zsh
```

```fish
set -x TOKEI_API_KEY tokei_k_...          # fish
```

```powershell
$env:TOKEI_API_KEY = "tokei_k_..."        # PowerShell
```

3. Try it:

```sh
tokei-agent me                       # verify the key, see plan + API usage
tokei-agent pages:list --status active
tokei-agent stats <contestId>        # analytics for one page
```

Every command prints JSON to stdout with a top-level `rate_limit` object. Exit codes: `0` success, `1` API/network error, `2` usage error (JSON on stderr).

> **Interactive output (0.3.1+).** When stdout is an interactive terminal, the CLI renders a banner and a human-readable summary instead of raw JSON. When stdout is a pipe, a redirect, CI, or the `mcp` transport, it prints exactly the JSON it always has — so agents, scripts and MCP clients are unaffected. Set `TOKEI_OUTPUT=json` to force JSON at a terminal too; `NO_COLOR` disables colour and animation, and `TOKEI_NO_ANIM=1` keeps the colour but stops the movement.

> **Known issue — exit codes on Node 24 / Windows (fixed in 0.3.0).** On 0.2.2 and earlier the CLI could print its correct JSON output and then abort during process exit, corrupting the exit code (`$LASTEXITCODE` read `-1073740791` / `0xC0000409` on success and failure alike). On an affected version, judge a run by the JSON on stdout, not by the exit status — or upgrade. (Historical labelling slip: the 0.3.0 tarball misreported `--version` as `0.2.2`; 0.3.1+ reports correctly.)

## Commands

Read (any key):

| Command                    | Does                                                        |
| -------------------------- | ----------------------------------------------------------- |
| `me`                       | Verify the key; account, plan, API usage                    |
| `pages:list`               | List pages — `--status`, `--mode`, `--page`, `--per-page`   |
| `pages:get <contestId>`    | One page in full (prizes, reward tiers, public URL)         |
| `stats <contestId>`        | Aggregated analytics                                        |
| `leaderboard <contestId>`  | Participants ranked by points                               |
| `referrals:top <contestId>`| Top referrers ranked by conversions, plus referral totals   |
| `winners:list <contestId>` | Selection-run history, newest first, with each run's winners nested |
| `entries:list <contestId>` | Signups — filter with `--email`                             |
| `surveys:list <contestId>` | Survey responses                                            |
| `webhooks:list`            | List webhook subscriptions                                  |
| `templates:list`           | The platform's named starting points, for `pages:clone --template` |
| `actions:catalog`          | Every entry-action type Tokei supports — `--type <actionType>`     |
| `events:catalog`           | Every webhook event Tokei's delivery engine understands — `--type <eventName>` |

Write (needs a read+write key):

| Command                       | Does                                                                     |
| ----------------------------- | ------------------------------------------------------------------------ |
| `pages:clone`                 | Create a page by cloning one you own, a named template, or the starter. 20/day cap |
| `media:upload <file>`         | Upload an image or video, get back a `public_url` for `pages:update`. ≤4MB per file (video too) |
| `pages:update <contestId>`    | Update title, description, dates, prizes, reward tiers, appearance (incl. the Custom template: `--template simple` / `--custom-css`), media, and entry actions (`entry_methods`, incl. custom-link rows) |
| `pages:publish <contestId>`   | Take a page live (needs a future `end_date`)                             |
| `pages:unpublish <contestId>` | Back to draft — blocks new signups and hides the page from visitors      |
| `entries:create <contestId>`  | Add a signup                                                             |
| `webhooks:create`             | Subscribe an HTTPS endpoint (`whsec_` secret shown once — save it!)      |
| `webhooks:delete <webhookId>` | Remove a subscription                                                    |

Write commands take simple fields as flags and full/nested bodies via `--data '<json>'` or `--data @file.json` (flags win on conflict). Run `tokei-agent --help` for every flag, or see [SKILL.md](./SKILL.md) — the agent-oriented reference bundled in this package, with worked examples and error-handling guidance.

```sh
tokei-agent pages:clone --title "Spring Launch Waitlist" --source <promotionId>
tokei-agent pages:update <contestId> --end-date 2026-09-01T00:00:00Z
tokei-agent media:upload ./hero.png
tokei-agent pages:update <contestId> --image-video <public_url from the upload above>
tokei-agent actions:catalog --type twitter_follow                  # see what a type accepts
tokei-agent pages:update <contestId> \
  --data '{"entry_methods":[{"actionType":"tiktok_follow","label":"Follow us on TikTok","points":3,"config":{"username":"tokei"}}]}'
```

## MCP server

The package doubles as a local MCP server (stdio): every command above becomes an MCP tool (`pages_list`, `pages_update`, `stats`, …) for Claude Code, Claude Desktop, and other MCP clients.

```sh
claude mcp add tokei --env TOKEI_API_KEY=tokei_k_... -- npx -y tokei-agent mcp
```

Or in JSON config:

```json
{
  "mcpServers": {
    "tokei": {
      "command": "npx",
      "args": ["-y", "tokei-agent", "mcp"],
      "env": { "TOKEI_API_KEY": "tokei_k_..." }
    }
  }
}
```

## Environment

| Variable        | Required | Meaning                                          |
| --------------- | -------- | ------------------------------------------------ |
| `TOKEI_API_KEY` | Yes      | Sent as `Authorization: Bearer <key>`            |
| `TOKEI_API_URL` | No       | Base URL override (default `https://tokei.io`)   |

## Agents, human in the loop

Tokei is built so agents draft and humans approve: give monitoring agents a read-only key, reserve read+write keys for agents that genuinely need to change things, and set key expiry. New webhook subscriptions created via the API trigger a security notification to the account owner.

## Privacy Policy

Full policy: https://tokei.io/privacy

### Data collection practices

`tokei-agent` is a thin client for the Tokei v1 REST API. It collects no data of
its own: there is no telemetry, no analytics, no crash reporting, and no
phone-home of any kind.

It reads exactly two inputs from your environment — `TOKEI_API_KEY` and the
optional `TOKEI_API_URL` — plus the arguments you pass on the command line (or
the arguments an MCP client passes to a tool call). For `media:upload` it also
reads the bytes of the local file you name.

### Usage and storage

Your API key is used solely as an `Authorization: Bearer` header on requests to
your Tokei account. Command arguments become the request path, query string, or
JSON body. Nothing is written to disk: the CLI creates no config file, cache,
credential store, or log file, and holds nothing after the process exits.

API responses — which can include entrant email addresses, survey answers, and
analytics — are printed as JSON to stdout. From that point they are handled by
whatever invoked the CLI (your shell, your scripts, or your AI agent and its
conversation history). Treat that output as the personal data it is.

### Third-party sharing

Nothing is sold or shared with third parties. Data is transmitted only to:

- **Tokei** (`https://tokei.io`, or the host you set in `TOKEI_API_URL`) — every
  command, to serve your request against your own account.
- **Tokei's object storage provider** — `media:upload` only. The CLI sends the
  file to the Tokei API, which stores it with the provider; the CLI never
  contacts the provider itself. The file becomes a public asset on your
  promotion page.

The CLI contacts no other host.

### Data retention

The CLI retains nothing. Data held in your Tokei account — promotions, entries,
survey responses — is retained under the Tokei privacy policy above, and you can
request access or deletion there. API keys are created, scoped, expired, and
revoked by you at Dashboard → Settings → API Keys; revoking a key immediately
stops all access through it.

### Contact information

Tokei — https://tokei.io/privacy — support@tokei.io

## Docs

- API reference: https://tokei.io/docs/api
- OpenAPI spec: https://tokei.io/openapi.json
- Agent skill reference: [SKILL.md](./SKILL.md)

## License

MIT
