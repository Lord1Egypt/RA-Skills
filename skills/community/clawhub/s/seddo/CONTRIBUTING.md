# Contributing to Seddo

Thanks for your interest 🤝. Seddo is a small, dependency-light bash project — keep it that way.

## Principles

1. **Bash + gh only.** No new runtime dependencies (no python, no jq, no node). If you
   need JSON, escape it in bash (see `json_escape` in `scripts/seddo.sh`).
2. **The gist is the source of truth.** All shared state lives in the six gist files.
3. **Self-describing.** `PROTOCOL.md` inside the gist must let any agent participate
   without external docs.
4. **Append, don't overwrite.** Both in the code's behavior and in your edits.

## Project layout

```
scripts/seddo.sh   the CLI (all logic)
templates/         initial gist file contents
install.sh         installer (auto-detects agent type)
SKILL.md           skill definition (Claude Code / OpenClaw / OpenCode)
AGENTS.md          agent-facing quick reference
ARCHITECTURE.md    how it works internally
README.md          human-facing overview
```

## Development setup

```bash
gh repo clone dofbi/seddo
cd seddo
gh auth status          # must be authenticated
bash scripts/seddo.sh doctor
```

## Before opening a PR

1. **Syntax check**: `bash -n scripts/seddo.sh`
2. **Lint** (if available): `shellcheck scripts/seddo.sh install.sh`
3. **Smoke test** against a throwaway gist:
   - `seddo init` (create a test seddo)
   - `seddo add "test"`, `seddo claim T-001`, `seddo done T-001 "ok"`
   - `seddo send @all "hi"`, `seddo inbox`
   - delete the test gist when done: `gh gist delete <id> --yes`
4. **Bump `SEDDO_VERSION`** in `scripts/seddo.sh` and add a `CHANGELOG.md` entry.

## Commit style

- Conventional-ish: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`.
- Keep messages focused; explain the *why* when it isn't obvious.

## Code style

- POSIX-friendly bash; `set -euo pipefail` stays.
- Quote variables. Prefer `local` in functions.
- Keep commands small and composable; one `cmd_*` function per subcommand.

## Reporting bugs / ideas

Open a GitHub issue with: what you ran, what happened, what you expected, and your
`seddo doctor` output.
