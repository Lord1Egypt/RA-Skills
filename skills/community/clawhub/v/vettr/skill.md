---
name: vettr
description: "Static analysis scanner for third-party OpenClaw skills. Parses JS/TS with tree-sitter to flag eval/exec/spawn and obfuscation, checks package.json dependencies and lifecycle scripts, checks manifest metadata for typosquatted or blocked names, matches prompt-injection and credential-path patterns in every scanned text file (code, Markdown, JSON, YAML, TXT; prompt-injection checks include code comments), and lists literal fetch() URLs. Optional autoVet (off by default) hooks skill:pre-install and can block an install or ask the user to approve it. Local scans need no network; /skill:vet-url downloads over HTTPS (public hosts only) and /skill:vet-clawhub runs the clawhub CLI. Use when vetting a skill before installing it."
version: "2.0.8"
author: britrik
tags: ["security", "scanner", "vetting", "analysis", "static-analysis"]
metadata:
  openclaw:
    requires:
      env: []
      bins:
        - node
    envVars: []
    install:
      - kind: node
        package: "@openclaw/skill-vettr"
        bins: []
    emoji: "\U0001F6E1"
    homepage: https://github.com/britrik/skill-vettr
    notes: >
      Core /skill:vet command requires only node. The /skill:vet-url command
      additionally requires git and tar on PATH (archives are downloaded in-process). The /skill:vet-clawhub
      command requires the clawhub CLI. These are runtime-optional — the skill
      loads and registers commands regardless of their presence.
---

# skill-vettr v2.0.8

Security scanner for third-party OpenClaw skills. Analyses source code, dependencies, and metadata before installation using tree-sitter AST parsing and regex pattern matching.

## Installation

```bash
npm install
```

This installs all Node.js dependencies, including tree-sitter `.wasm` grammar files required at runtime for AST-based analysis. The `.wasm` files are located in `node_modules` and must be present for the skill to function.

> ⚠️ **Install safety:** `npm install` runs dependency lifecycle scripts, which can execute arbitrary code. For stronger isolation, run `npm ci --ignore-scripts` — but note that tree-sitter native/WASM artifacts may not build, breaking AST analysis. Prefer installing inside a container or VM when possible.

## External Binaries

The `vet-url` and `vet-clawhub` commands invoke external binaries via `execSafe` (which uses `execFile` — no shell is spawned). Only the following commands are permitted:

| Binary | Used By | Purpose |
|--------|---------|---------|
| `git` | `vet-url` | Clone `.git` URLs (hooks disabled, redirects off, connection pinned to the validated public address, user and system git config ignored) |
| `tar` | `vet-url` | Extract downloaded archives |
| `clawhub` | `vet-clawhub` | Fetch skills from ClawHub registry |

The `/skill:vet` command (local path vetting) requires only `node` and no external binaries.

## Permissions

| Capability | Used by | Scope |
|------------|---------|-------|
| Read files | all commands | The skill directory being vetted (allowed roots only) |
| Write files | `vet-url`, `vet-clawhub` | A fresh temp directory, deleted after the scan |
| Network | `vet-url`, `vet-clawhub` | HTTPS to public hosts only; none for `/skill:vet` |
| Subprocesses | `vet-url`, `vet-clawhub` | `git`, `tar`, `clawhub` via `execFile` (no shell) |

The skill never reads credentials; credential paths such as `~/.ssh` appear in its source only as detection patterns.

## Commands

- `/skill:vet --path <directory>` — Vet a local skill directory
- `/skill:vet-url --url <https://...>` — Download and vet from URL
- `/skill:vet-clawhub --skill <slug>` — Fetch and vet from ClawHub

## Detection Categories

| Category | Method | Examples |
|----------|--------|----------|
| Code execution | AST | eval(), new Function(), vm.runInThisContext() |
| Shell injection | AST | exec(), execSync(), spawn("bash"), child_process imports |
| Dynamic require | AST | require(variable), require(templateString) |
| Prototype pollution | AST | __proto__ assignment |
| Prompt injection | Regex | Instruction override patterns, control tokens (in string literals) |
| Homoglyph attacks | Regex | Cyrillic/Greek lookalike characters in identifiers |
| Encoded names | Regex | Unicode/hex-escaped "eval", "exec" |
| Credential paths | Regex | Cloud and SSH credential directory references, system credential store access |
| Network calls | AST | fetch() with literal URLs (checked against allowlist) |
| Malicious deps | Config | Known bad packages, lifecycle scripts, git/http deps |
| Typosquatting | Levenshtein | Skill names within edit distance 2 of targets |
| Dangerous permissions | Config | shell:exec, credentials:read in SKILL.md |

## Limitations

> ⚠️ **This is a heuristic scanner with inherent limitations. It cannot guarantee safety.**

- **Static analysis only** — Cannot detect runtime behaviour (e.g., code that fetches malware after install)
- **Evasion possible** — Sophisticated obfuscation or multi-stage string construction can evade detection
- **JS/TS only** — Binary payloads, images, and non-text files are skipped
- **Limited network detection** — Only detects `fetch()` with literal URL strings; misses axios, http module, dynamic URLs
- **No sandboxing** — Does not execute or isolate target code
- **Comment scanning** — Prompt injection detection scans string literals, not comments
- **Filesystem scope** — `vet-url` downloads and extracts remote archives into a temp directory; `vet` accepts paths under `os.tmpdir()`, `~/.openclaw`, and `~/Downloads` by default. Set `allowCwd: true` in config to also permit `process.cwd()` (see Configuration below)
- **Network scope** — `vet-url` only connects to hosts whose DNS answers are all public unicast addresses; loopback, private, link-local and cloud-metadata ranges are refused, every redirect is re-validated, and the connection is pinned to the checked address. Git clones run with redirects disabled and HTTPS as the only allowed protocol
- **External binary trust** — `vet-url` and `vet-clawhub` invoke `git`, `tar`, and `clawhub` via `execFile`. These binaries must be trusted and present on `PATH`

For high-security environments, combine with sandboxing, network isolation, and manual source review. Run inside a disposable container when vetting untrusted URLs.

## Configuration

### `allowCwd`

By default, `process.cwd()` is **not** included in the set of allowed vetting roots. The default allowed roots are:

- `os.tmpdir()`
- `~/.openclaw`
- `~/Downloads`

To allow vetting paths under the current working directory, set `allowCwd: true` in your vetting config:

```json
{
  "allowCwd": true
}
```

> ⚠️ **Security implication:** Enabling `allowCwd` means the scanner will accept any path under the directory you launched it from. If you run from `/` or `$HOME`, this effectively grants access to your entire filesystem. Only enable this when running from a scoped project directory or inside a container.

## `.vettrignore`

A `.vettrignore` file in the root of the scanned skill can exclude files or directories from analysis, for example test fixtures that contain deliberate malicious patterns.

Because the scanned skill controls that file, it is **not applied by default**: the scanner reports it as a WARNING and scans everything. Set `"trustVettrignore": true` in the `skill-vettr` config only when scanning your own skill. Even then, patterns that would exclude the whole skill (`*`, `**`) or `SKILL.md` / `package.json` are rejected, and the report lists every excluded path.

### Format

- One glob pattern per line
- Lines starting with `#` are comments
- Empty lines are ignored
- Patterns ending with `/` match entire directories
- `*` matches any sequence of non-separator characters
- `**` matches any sequence including path separators (recursive)
- `?` matches a single non-separator character

### Example

```
# Exclude test fixtures containing deliberate prompt injection vectors
test/fixtures/

# Exclude generated files
dist/
*.min.js
```

If the `.vettrignore` file is unreadable or contains invalid UTF-8, the engine logs an INFO-level warning and proceeds with a full scan.
