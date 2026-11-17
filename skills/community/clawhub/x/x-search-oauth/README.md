# x-search-oauth

Search X/Twitter from the command line with xAI OAuth and the xAI Responses API `x_search` tool, with an OpenClaw skill for agent-side X search workflows.

This repo intentionally ships two surfaces from one source:

- **ClawHub skill**: `SKILL.md` for OpenClaw agents using native `x_search`.
- **CLI utility**: `xso`, a standalone Node.js command that logs in with xAI device-code OAuth and runs terminal searches.

---

## What It Does

- Opens a remote-friendly xAI OAuth device-code login with `xso auth`
- Stores the OAuth token locally in `~/.config/x-search-oauth/auth.json` with `0600` permissions
- Refreshes the token automatically when a refresh token is available
- Calls `https://api.x.ai/v1/responses` with the `x_search` tool
- Supports query, handle, date, image, video, and JSON output options
- Keeps X posts treated as untrusted external content

---

## Install The CLI

From npm registry:

```bash
npm install -g x-search-oauth
xso auth
xso "AI coding agents" --from-date 2026-05-20
```

From GitHub via npm:

```bash
npm install -g github:LeoStehlik/x-search-oauth#v0.2.3
```

From GitHub/source:

```bash
git clone https://github.com/LeoStehlik/x-search-oauth.git
cd x-search-oauth
npm test
npm link
xso auth
```

That installs two commands:

```bash
x-search-oauth --help
xso --help
```

---

## Install The OpenClaw Skill

From ClawHub:

```bash
openclaw skills install x-search-oauth
```

The skill is for OpenClaw agents. It tells agents when to use native `x_search`, how to shape X queries, and how to report/cite X results. It also declares `xso` as an optional Node companion binary, installed from the npm registry.

---

## CLI Usage

Authenticate once:

```bash
xso auth
```

The CLI prints a verification URL and user code. Open the URL in your browser, enter the code if needed, approve xAI access, then return to the terminal. This works when the CLI runs on a different machine, because it does not depend on a localhost callback.

Search X:

```bash
xso search --query "OpenClaw xAI OAuth" --from-date 2026-05-20
```

A positional query also works:

```bash
xso "AI coding agents" --from-date 2026-05-20
```

Restrict to handles:

```bash
xso search --query "OpenClaw 2026.5.19" --handle openclaw --from-date 2026-05-20
```

Print JSON:

```bash
xso search --query "AI coding agents" --from-date 2026-05-20 --json
```

Inspect local auth state:

```bash
xso doctor
```

Remove the local token file contents:

```bash
xso logout
```

Supported v0.2.0 options:

```text
-q, --query <text>          X search query
    --handle <handle>       Restrict to handle; repeat or comma-separate
    --exclude-handle <h>    Exclude handle; repeat or comma-separate
    --from-date YYYY-MM-DD  Start date
    --to-date YYYY-MM-DD    End date
    --image                 Enable image understanding
    --video                 Enable video understanding
    --json                  Print normalized JSON payload
    --raw                   Same as --json for v0.2.0
    --timeout <seconds>     Search request timeout, default 45
    --model <name>          xAI model, default grok-4-1-fast-non-reasoning
    --max-turns <n>         Optional xAI Responses max_turns
```

Set `X_SEARCH_OAUTH_CONFIG_HOME` to override the config directory used for `x-search-oauth/auth.json`.

---

## Skill Usage

Inside OpenClaw, prefer the native `x_search` tool when it is available. The skill instructions are included for agent-side X search workflows.

Ask naturally inside OpenClaw:

```text
Use x-search-oauth to search recent AI agent posts on X.
```

```text
Search X for OpenClaw xAI OAuth announcements from the last 24 hours.
```

The skill tells the agent to prefer multiple narrow searches, use date/handle filters when useful, cite returned X status URLs, and discard no-citation summaries.

---

## Distribution Model

- **GitHub** is the canonical source for both the skill and CLI.
- **ClawHub** distributes the OpenClaw skill metadata/instructions.
- **npm/GitHub package install** distributes the `xso` terminal utility. The current ClawHub install hint uses the tagged GitHub package; switch it to plain `x-search-oauth` after npm registry publication.
- Git tags use SemVer (`v0.2.0`, `v0.2.1`, ...). ClawHub skill versions should match repo tags when the skill text changes.

---

## Why This Exists

The practical CLI path is direct xAI OAuth plus direct `x_search`. It avoids API-key-only wrappers, avoids unofficial scraping, and avoids making a command-line product depend on OpenClaw Gateway connectivity between two machines.

OpenClaw remains useful as the live agent environment and as the reference implementation for xAI OAuth/tool semantics, but the CLI should be testable from a normal shell.

---

## What's Inside

```text
x-search-oauth/
|-- bin/x-search-oauth.js  CLI entrypoint
|-- src/cli.js             OAuth, argument parsing, xAI request, formatting
|-- test/cli.test.js       Node test suite with mocked xAI calls
|-- SKILL.md               OpenClaw skill instructions
`-- README.md
```

---

## Verification

```bash
npm test
npm pack --dry-run
```

The test suite verifies argument parsing, device-code auth handling, local token refresh, xAI request shape, and output formatting.

---

## License

MIT - see [LICENSE](LICENSE)
