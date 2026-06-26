---
name: Worktree Manager
slug: worktree-manager
version: 1.3.0
description: "Manage Docker-based dev instances and git worktrees. Handles app container lifecycle, database seeding, and proxy route activation. Requires mysql-manager and proxy-manager to be running first."
changelog: "v1.3.0: Fix dump_main_to to avoid sh -c/backtick shell injection (two docker exec), validate DB names before all SQL ops, validate instance name on all commands, align password var with MYSQL_ROOT_PASSWORD. v1.2.0: Validate instance names, add remove-worktree confirmation, warn on default password. v1.1.0: Split MySQL and proxy lifecycle into separate plugins."
triggers:
  - "start instance"
  - "stop instance"
  - "create worktree"
  - "remove worktree"
  - "criar worktree"
  - "remover worktree"
  - "iniciar instância"
  - "parar instância"
  - "list instances"
  - "listar instâncias"
  - "worktree-manager"
metadata: {"clawdbot":{"emoji":"🌿","requires":{"bins":["docker","git"]},"os":["linux","darwin"]}}
---

# Worktree Manager

Manages Docker app instances and git worktrees for local development.

Each instance gets its own docker-compose stack (backend + frontend), isolated git branch, and `.env.worktree-<name>` file. MySQL and nginx-proxy are managed separately by their own plugins.

## Prerequisites

Start these first (order matters):
1. `proxy-manager start` — creates the shared Docker network (`nginx-proxy_net`)
2. `mysql-manager start` — starts the shared MySQL container

## Architecture

```
project/
├── docker-compose.yml        # app stack template (backend + frontend)
├── run.sh                    # this plugin's entry point (copy to project root)
├── .env.base                 # main instance env
├── .env.worktree-<name>      # per-worktree env (gitignored)
└── .worktrees/
    └── <name>/               # git worktree (gitignored)
```

- `main` → `.env.base`, project root
- `worktree` → `.env.worktree-<name>`, checked out at `.worktrees/<name>`
- URLs: `http://<name>.frontend.localhost` / `http://<name>.backend.localhost`

## Commands

All commands run from the project root:

```bash
./run.sh list                        # show all instances + mysql/proxy status
./run.sh start [main|<name>]         # seed db, start containers, connect proxy
./run.sh stop  [main|<name>]         # stop containers (db persists)
./run.sh restart [main|<name>]       # stop then start
./run.sh logs  [main|<name>]         # follow container logs
./run.sh create-worktree <name>      # git worktree + branch + env file
./run.sh remove-worktree <name>      # stop containers + drop db + remove worktree
```

## How to Execute Tasks

### Full environment setup (first time)
```bash
proxy-manager/run.sh start        # network + nginx-proxy
mysql-manager/run.sh start        # MySQL
./run.sh start main               # main app instance
```

### Create a new worktree and start it
1. `./run.sh create-worktree <name>` — creates branch `worktree/<name>`, dir `.worktrees/<name>`, env file
2. `./run.sh start <name>` — seeds db from main snapshot, starts containers, activates proxy route
3. URLs reported at the end

### Stop an instance
```bash
./run.sh stop <name>
```

### Remove a worktree (destructive — always confirm first)
Confirm with user: "Remove worktree '<name>'? Deletes containers, database, git worktree (branch `worktree/<name>`), and `.env.worktree-<name>`."
```bash
./run.sh remove-worktree <name>
```

### List all instances
```bash
./run.sh list
```

## What `start` Does

1. Checks MySQL container is running (exits with error if not)
2. `CREATE DATABASE IF NOT EXISTS` for the instance
3. For non-main instances: dumps `codai_main` → instance db
4. `docker compose up --build -d`
5. `docker network connect` — proxy to instance network (activates routes)

## Rules

- Always check `./run.sh list` before starting — it shows MySQL/proxy status.
- Always confirm before `remove-worktree` — it is irreversible.
- After `start`, print the frontend and backend URLs.
- If `./run.sh` is not executable: `chmod +x run.sh`
- `.env.worktree-*` files and `.worktrees/` dir must be gitignored.

## Configuration

| Variable          | Default             | Purpose                        |
|-------------------|---------------------|--------------------------------|
| `MYSQL_CONTAINER` | `codai_db`          | MySQL container name           |
| `MYSQL_ROOT_PASS` | `secret`            | MySQL root password            |
| `MYSQL_MAIN_DB`   | `codai_main`        | Source DB for snapshots        |
| `PROXY_CONTAINER` | `codai_nginx_proxy` | nginx-proxy container name     |
| `PROJECT_PREFIX`  | `codai-dev`         | Docker Compose project prefix  |

## Related Plugins

- `proxy-manager` — nginx-proxy lifecycle and network management (start first)
- `mysql-manager` — MySQL lifecycle and database admin (start second)
