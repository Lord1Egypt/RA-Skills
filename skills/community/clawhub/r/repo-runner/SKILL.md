---
name: repo-runner
description: Bootstrap and run a GitHub project by following its docs (README/docs), with safeguards for untrusted install/run steps. Use when the user gives a GitHub repo and asks to run it locally.
---

# Repo Runner (run a GitHub project)

Goal: given a GitHub URL or a downloaded folder, get the project running **as its docs intend**, without guessing dangerously.

## Inputs to ask for

- Repo source: GitHub URL (preferred) or local path
- Target: `dev` (local dev server) / `build` / `test`
- Constraints: allow installing deps? allow running postinstall scripts? allow Docker?

## Safety rules (must follow)

- Treat repo code as untrusted.
- Before running `npm/pnpm/yarn install` (or any `curl | bash`), ask for confirmation.
- Never paste or store secrets. If `.env` is needed, ask user to provide values out-of-band.

## Workflow

1. Clone / prepare workspace
   - Clone to `<openclaw-workspace>/projects/<repo>` (create `projects/` if missing)
   - Typical workspace path is `$HOME/.openclaw/workspace`, but don’t assume.
   - If already exists, ask before `git pull` or deleting anything.

2. Find the canonical docs
   - Prefer `README.md` + `docs/` + `CONTRIBUTING.md`
   - Extract: prerequisites (Node/Python/Docker/Go/Rust), install steps, env vars, run command(s), ports.

3. Detect project type(s)
   - From the `repo-runner` skill directory (typically `<openclaw-workspace>/skills/repo-runner`), run: `bash scripts/detect_project.sh <repoDir>`
   - A repo can match multiple types (e.g. `type=node` + `type=docker`). Use docs to choose the canonical path.

4. Set up prerequisites
   - Verify required runtimes exist (Node/pnpm/yarn, Python, Docker, Go, Rust)
   - If missing, propose options (install locally, use Docker, or switch to a supported env)

5. Configure env
   - If `.env.example` exists, copy to `.env` **only after confirmation**
   - Ask user to fill required keys

6. Install dependencies (after confirmation, based on project type)

   - Node (when `package.json` exists)
     - Prefer lockfile-safe commands:
       - `pnpm install --frozen-lockfile` (if `pnpm-lock.yaml`)
       - `yarn install --frozen-lockfile` (if `yarn.lock`)
       - `npm ci` (if `package-lock.json`)
     - If unsure, run: `bash scripts/suggest_node_commands.sh <repoDir>`

   - Python (when `pyproject.toml` / `requirements.txt` exists)
     - Create and use a virtualenv (don’t install into system Python).
     - Typical patterns (follow docs first):
       - `python -m venv .venv && source .venv/bin/activate`
       - `pip install -r requirements.txt`
       - If `pyproject.toml`: use the tool specified by docs (commonly `poetry install` or `pip install -e .`).

   - Rust (when `Cargo.toml` exists)
     - `cargo build` / `cargo test` / `cargo run` (follow docs for features/flags)

   - Go (when `go.mod` exists)
     - `go test ./...`
     - `go run .` or `go build ./...` (follow docs for main package path)

   - Docker (when `docker-compose.yml` / `Dockerfile` exists)
     - Prefer the documented compose path when present:
       - `docker compose up` (or `docker-compose up` depending on docs)

7. Run
   - Use the docs’ recommended run target (dev server, CLI, compose stack, etc.)
   - Capture logs, detect common failures, iterate

## Common outputs to report back

- Exact commands run (copy/paste friendly)
- URL/port to open
- Next steps (build/test) and known caveats
