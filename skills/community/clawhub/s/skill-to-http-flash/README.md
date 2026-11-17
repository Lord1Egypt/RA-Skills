# skill-to-http-flash

> Compile a single agent Skill into a standalone HTTP REST API microservice — subprocess direct execution, zero LLM at runtime, 100% reproducible.

`skill-to-http-flash` turns any Python skill entry (an `argparse`-based `.py` script) into a production HTTP service:

```
POST /run  →  subprocess.run(["python3", "scripts/main.py", "--foo", "x", ...])
            →  envelope { success / exit_code / elapsed_ms / data | output / stderr / truncated }
```

No Gateway, no LLM, no `sessions_spawn` at runtime. Sub-second cold start, deterministic output.

**Runtime-neutral by design.** It does not import any agent SDK — it just compiles an `argparse` Python script into a REST API. It runs on OpenClaw, Claude Code, Cursor, any other agent runtime, **or no agent at all** (plain machine / CI / container). The only runtime-specific bit is *where it looks for skill directories by default*, and that is fully overridable via `--skill-dir` / `FLASH_SKILL_DIR`.

## ⚠️ Security Notice — read before deploying

Compiling a skill into an HTTP service exposes whatever that skill can do (file, network, system actions) to any caller who can reach the endpoint. Treat it as publishing a code-execution surface, not a zero-risk wrapper:

- **Network exposure of the wrapped skill.** `/run` executes the skill via subprocess for any reachable caller. Auth (API Key) is optional and CORS is permissive by default — set an API Key and restrict binding/CORS before exposing beyond `localhost` or a trusted network. Default HTTP is unencrypted; enable HTTPS for cross-host use.
- **Optional generation-time LLM sends SKILL.md off-host.** During `create` / `recreate` only, param-schema extraction can call an external chat-completions endpoint with the skill's `SKILL.md`. This is **off by default** (unconfigured → heuristic fallback); it activates only when you set `llm.base_url` + `llm.api_key`. Runtime (`/run`) never touches an LLM. If you enable it, ensure SKILL.md holds no secrets/internal details and trust the endpoint. 
- **`--delete-files` is destructive.** `flash.py remove --skill <name> --delete-files` permanently deletes the generated service files. Double-check the skill name before running — there is no undo.

## Features

- **Subprocess direct execution** — no LLM drift, 100% reproducible, `<2s` cold start
- **JSON → CLI mapping** — request JSON auto-maps to long flags (`{"foo_bar": 10}` → `--foo-bar 10`), field-name allowlist `[a-z][a-z0-9_]*` + argv-as-list (no shell injection)
- **Unified envelope** — business failure (`exit_code != 0`) returns HTTP 200 + `success:false`; only framework errors use HTTP status codes
- **Sync + async** — `POST /run` (60s default, 512KB truncation) and `POST /run/async` (no truncation, in-memory + JSONL persistence, logrotate, SQLite export)
- **Multi-agent runtime** — auto-detects skill dirs for OpenClaw / Claude Code / Cursor / generic `./skills` out of the box, or override via `FLASH_SKILL_DIR` / `--skill-dir`
- **HTTP by default, HTTPS on demand** — self-signed SAN cert auto-generation, optional API-Key auth (`hmac.compare_digest` constant-time), configurable CORS
- **Self-contained output** — generated `server.py` has cert / job store / argv builder / envelope inlined; `scp` it to any machine and run

## Quick Start

`skill-to-http-flash` auto-detects skill directories for common runtimes
(`~/.openclaw/workspace/skills`, `~/.claude/skills`, `~/.cursor/skills`,
`~/.config/skills`, `./skills`, `/app/skills`). Point it anywhere else with
`--skill-dir` / `FLASH_SKILL_DIR`.

```bash
# 1. Create a flash project for a skill
python3 scripts/flash.py create --skill <skill-name>

# 2. Start the generated service
cd <data-dir>/services/<skill-name>-api
pip install -r requirements.txt
python3 server.py start

# 3. Call it
curl -X POST http://127.0.0.1:7780/run \
  -H 'content-type: application/json' \
  -d '{"foo": "bar"}'
```

### Custom / standalone paths

For any runtime with a non-standard layout, or a plain machine with no agent:

```bash
export FLASH_SKILL_DIR=/your/path/to/skills
export FLASH_DATA_DIR=/your/path/to/flash-data
python3 scripts/flash.py create --skill my-skill
```

The generated `server.py` is fully self-contained — `scp` it to any machine
and run it with just `pip install -r requirements.txt`.

## Requirements

- Python 3.10+
- `pip install fastapi uvicorn cryptography pydantic jsonschema`
- `openssl` (optional, HTTPS mode)
- Skill entry must be a `.py` file (recommend `argparse` long flags)

## Usage

Full documentation, endpoint reference, param-mapping rules, TLS/auth/CORS config and the CLI command list are in [SKILL.md](./SKILL.md).

## Install

Clone or copy the skill folder into your runtime's skills directory — the
tool auto-detects it. No runtime is privileged; pick whichever applies:

| Runtime | Install |
|---|---|
| OpenClaw | `clawhub install skill-to-http-flash`, or copy to `~/.openclaw/workspace/skills/` |
| Claude Code | Copy to `~/.claude/skills/` |
| Cursor | Copy to `~/.cursor/skills/` |
| Any other runtime | Copy anywhere, then set `FLASH_SKILL_DIR` / `--skill-dir` |
| Standalone (no agent) | `git clone` this folder and run `python3 scripts/flash.py ...` directly |

```bash
git clone https://github.com/Songhonglei/html-tool-suite.git
cp -r html-tool-suite/skills/skill-to-http-flash <your-skills-dir>/
```

## License

MIT (see [LICENSE](./LICENSE))

## Author

Evan Song · [github.com/Songhonglei](https://github.com/Songhonglei)

## Changelog

### v2.0.4 (2026-07-28)

- Documentation-only: added a **Security Notice** near the top of the README covering (1) network exposure of the wrapped skill (auth/CORS/HTTP defaults), (2) the optional generation-time LLM path that sends `SKILL.md` off-host — off by default, runtime stays LLM-free, and (3) `--delete-files` being a destructive, no-undo operation. Addresses review findings about missing user warnings. No code change.

### v2.0.3 (2026-07-14)

- Runtime-neutral README — equal treatment for OpenClaw / Claude Code / Cursor / standalone (previously the Install section was OpenClaw-centric)

### v2.0.2 (2026-07-14)

- Multi-agent skill-dir detection (Claude Code / Cursor / XDG / local `./skills`) — works out of the box on any runtime
- Doc consistency: clarified runtime is LLM-free; LLM is optional at generation time only (falls back to heuristic schema)
- Graceful shutdown: generated `server.py` no longer `os._exit(0)` in lifespan (avoids bypassing atexit/finally, prevents truncated JSONL flush)
- Security: API-Key check uses constant-time `hmac.compare_digest`; 401 no longer echoes the header name
- `FLASH_MAX_ASYNC` env to configure async concurrency limit (default 20)

### v2.0.1

- PVC persistence paths, TLS/auth/CORS, async job store, SQLite export
