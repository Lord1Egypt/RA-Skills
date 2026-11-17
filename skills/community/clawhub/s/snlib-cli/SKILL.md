---
name: snlib-cli
description: Run Seongnam Library (snlib.go.kr) tasks with the native MoonBit CLI: login, book search, account/loan/reservation status, interlibrary loans, hope-book requests, and basket queries. Prepare write requests first and submit only after explicit user confirmation.
metadata: { "openclaw": { "requires": { "bins": ["bash", "curl"] } } }
---

# snlib-cli (MoonBit)

Run `"{baseDir}/scripts/snlib-cli.sh" <command>` with exactly one JSON object
on stdin. Use `{}` for commands without fields. Clojure flags, EDN request
payloads, and `SNLIB_USER` / `SNLIB_PASSWORD` are not used by this launcher.

## Setup

Requires Bash, curl, and either `sha256sum` or `shasum`. No MoonBit,
compiler, or source checkout is needed. The native executable uses the system
libcurl runtime (on Debian/Ubuntu, install `libcurl4` or `libcurl4t64` as
appropriate for your distribution).

Supported release assets: macOS ARM64 and glibc Linux ARM64/x86-64.
Linux x86-64 builds target Ubuntu 22.04; ARM64 builds target Ubuntu 24.04.
Intel macOS (unsupported by the current MoonBit toolchain), Alpine/musl,
Windows, and older runtime libraries are not supported.

On first use, the launcher downloads the matching prebuilt binary from
`https://github.com/ruseel/snlib-cli/releases/download/<pinned-tag>/`.
The tag and SHA-256 checksums are pinned in
`{baseDir}/references/native-release.txt`. A checksum mismatch stops execution.
The binary is cached under `$XDG_CACHE_HOME/snlib-cli` (default
`~/.cache/snlib-cli`) and verified on every invocation. Once cached, no
download is needed. Downloads do not consume the JSON input or login password.

For offline/local development only, set `SNLIB_CLI_BINARY` to an absolute path
to an already-built, trusted native executable. This explicitly bypasses
release downloading and checksum verification. The launcher never compiles
code, downloads a source repository, or falls back to Clojure.

## Quick Start

```bash
"{baseDir}/scripts/snlib-cli.sh" --help

# Public search: no login required.
printf '%s\n' '{"keyword":"제2차 세계대전 발췌본","manage_codes":["MA"],"page":1,"per_page":10}' |
  "{baseDir}/scripts/snlib-cli.sh" search-books

# Login from a private JSON file with user_id and password (permissions 0600).
"{baseDir}/scripts/snlib-cli.sh" login < /path/to/private-login.json

printf '%s\n' '{}' | "{baseDir}/scripts/snlib-cli.sh" my-info
printf '%s\n' '{}' | "{baseDir}/scripts/snlib-cli.sh" loan-status
```

## Workflows

- Account/session: `login`, `my-info`.
- Discovery: `search-books`, `basket-list`.
- Account queries: `loan-status`, `loan-history`, `reservation-status`,
  `interloan-status`, `hope-book-list`, `hope-book-detail`.
- Request preparation/submission: `interloan-request` (alias
  `interlibrary-loan-request`) and `hope-book-request`.

Read `{baseDir}/references/commands.md` for JSON patterns.

## Safety and Results

- Inspect JSON `outcome` and `code`, not just the exit status. The native CLI
  currently exits successfully even for command-level errors.
- Write commands default to preparation only. Review `data.prepared_payload`
  and obtain explicit confirmation of the full request before setting
  `"submit":true`. Never infer SMS/contact consent from unchecked form defaults.
- Never automatically retry a POST after a network or persistence error. Check
  `interloan-status` / `hope-book-list` first; it may already have succeeded.
- Read login JSON from a private file outside this repository, with owner-only
  permissions (`0600`). Do not put real passwords in arguments, history, or logs.
  Login does not save the password.
- Account outputs and prepared payloads contain personal data. Avoid shared logs.
- Sessions live under `$XDG_CONFIG_HOME/snlib-cli`, falling back to
  `~/.config/snlib-cli`, and expire after three hours. Cookie refresh does not
  extend this limit. Legacy Clojure sessions remain untouched; log in once with
  the native CLI.
- Every authenticated command uses origin-bound cookies. Changing
  `SNLIB_BASE_URL` requires a new login. Use the default HTTPS service unless
  intentionally testing against a literal loopback server.

## Troubleshooting

- Release manifest missing: this is an unprepared source checkout; the
  maintainer must run `clawhub-release.bb prepare --version VERSION`.
- Download failure: check network access to GitHub and the pinned release.
- Checksum mismatch: do not execute the file; reinstall the trusted skill or
  remove the corrupted cached file and retry.
- Unsupported platform / missing runtime library: use a supported OS/architecture
  and install the libcurl runtime. No source build is attempted.
- JSON/input errors: pipe one JSON object; check `references/commands.md`.
- `session-missing`, `session-expired`, or `session-rejected`: log in again.
- `session-origin-mismatch`: log in for the selected server.
- `submit-failed`: the response did not confirm submission; inspect status before retry.
- `session-save-failed`: fix config-directory access; after a write, check status
  before retrying.
- HTTP/parse errors: do not claim success; the website may have changed.

Source: https://github.com/ruseel/snlib-cli
