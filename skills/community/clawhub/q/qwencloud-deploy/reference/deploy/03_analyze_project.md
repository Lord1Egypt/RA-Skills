# Project Analysis (Step 3)

The agent directly browses the project directory, collects key signals, and makes project type decisions.

---

## Collection Steps

### 1. File Tree Overview

```bash
find <project-root> -maxdepth 3 -not -path '*/node_modules/*' -not -path '*/.git/*' \
  -not -path '*/__pycache__/*' -not -path '*/.venv/*' -not -path '*/target/*' \
  -not -path '*/dist/*' -not -path '*/build/*' | head -100
```

Purpose: Understand overall project structure (static/app split? monolith? monorepo?)

### 2. Configuration Files

Read key config files in the project root and first-level subdirectories (if they exist):

| Category | Files |
|----------|-------|
| Node.js | `package.json` |
| Go | `go.mod` |
| Python | `requirements.txt`, `pyproject.toml`, `Pipfile` |
| Java | `pom.xml`, `build.gradle` |
| Rust | `Cargo.toml` |
| Docker | `Dockerfile`, `docker-compose.yml` |
| Static build | `vite.config.*`, `next.config.*`, `nuxt.config.*` |
| Runtime | `Procfile`, `.env.example` |

Read method: `cat` or `head -50` (first 50 lines for large files).

### 3. Entry Source Sampling

Read the first 30 lines of potential entry files to confirm framework and port:

Common entries: `app.py`, `main.py`, `server.py`, `main.go`, `cmd/main.go`,
`server.js`, `index.js`, `src/index.ts`, `src/main.rs`, `Program.cs`, `app.rb`

```bash
head -30 <entry-file>
```

### 4. README

```bash
head -80 README.md
```

Get build/run instructions.

### 5. Database Signals

Search config files and source code for database-related dependencies/connection strings:
- MySQL: `pymysql`, `mysql2`, `go-sql-driver/mysql`, `jdbc:mysql://`, `MYSQL_` env vars
- PostgreSQL: `psycopg2`, `pg`, `gorm.io/driver/postgres`
- Redis: `redis`, `ioredis`, `go-redis`
- MongoDB: `pymongo`, `mongoose`, `mongo-driver`
- Docker Compose `image: mysql/postgres/redis/mongo`

### 6. App Metadata

Extract app_name and app_desc from `package.json` (name/description), `go.mod` (module),
`pyproject.toml` (name), `Cargo.toml` (name), etc.
When extraction fails, use the directory name as app_name.

---

## Decision Outputs

After collection, the Agent determines these variables:

| Variable | Description |
|----------|-------------|
| `APP_NAME` | App name; must match `^[a-z][a-z0-9-]{0,30}$` (lowercase letter first; only lowercase letters/digits/hyphen, length 1-31). Used directly as the service name (systemd unit / container name / log file name). Normalize first if it contains uppercase/underscore/spaces/non-ASCII or is too long |
| `APP_DESC` | One-sentence description |
| `app_type` | See mapping table below |
| `start_command` | Full startup command (relative to deploy directory) |
| `app_port` | App listen port |
| `static_dir` | Static build output directory (e.g. `dist`) |
| `app_dir` | App directory |
| `nginx_mode` | `static+app` / `proxy` / `static` |

---

## app_type Mapping

| Signal | app_type |
|--------|----------|
| Dockerfile / docker-compose.yml | `docker` |
| go.mod / Cargo.toml (static compiled) | `systemd` + `runtime=none` |
| pom.xml / build.gradle | `systemd` + `runtime=java` |
| package.json + express/fastify/koa/nest | `systemd` + `runtime=node` |
| requirements.txt / pyproject.toml + Python entry | `systemd` + `runtime=python` |
| Pure static (React/Vue/Vite, no app) | `static-only` |

When a Dockerfile exists, prefer `docker` unless the user explicitly doesn't want it.

### All other languages go through Docker

The `runtime` whitelist has only four values — `none` / `java` / `node` / `python` — and it controls
exactly one thing: whether to install an interpreter on the ECS instance. The resulting rule:

| Project type | Choice |
|--------------|--------|
| Java / Python / Node | `systemd` + matching `runtime` |
| Compiles to a self-contained binary (Go, Rust, C/C++, Zig, …) | `systemd` + `runtime=none` |
| **Every other language** (Ruby, PHP, Elixir, .NET, Deno, Bun, Perl, …) | **`docker`** |

#### Decision order

1. **Is there a `Dockerfile` / `docker-compose.yml`?** → `docker` (the author already expressed a
   deployment intent; most reliable signal)
2. **Is it Java / Python / Node?** → `systemd` + matching `runtime`
3. **Is the build output self-contained?** → if yes, `runtime=none`; otherwise Docker is required
   (see the no-Dockerfile handling below)

#### General principle: judge the build output, not the language name

The table above cannot be exhaustive. For a language that is not listed (Nim, Crystal, Haskell,
OCaml, …), decide with this question:

> **After building, do you get a file that runs as-is when copied to a bare Linux box, or code /
> intermediate output that still needs an interpreter or VM installed first?**

- The former → `systemd` + `runtime=none` (the artifact carries everything; the host needs nothing)
- The latter → use the matching `runtime` if it is in the whitelist (Java/Python/Node); everything
  else → `docker`

Judge by the **default build output**, not by what is theoretically possible. For example, .NET can
produce a self-contained executable via `dotnet publish --self-contained`, but its default output is
a DLL that requires the .NET runtime, so it belongs to `docker` — do not try to guess the user's
build flags.

> ⚠️ Apart from the statically compiled languages above, do **not** pick `runtime=none` and put the
> interpreter in `start_command`. The ECS base image has no ruby / php / dotnet runtime, so when
> `systemd.sh` resolves `start_command` the `command -v` lookup fails and it falls back to
> `/opt/qwencloud/<command>`, leaving systemd unable to start the service — by which point the
> ECS instance and EIP have already been created and are billing.

Two cases when going the Docker route:

1. **Project already has a Dockerfile / docker-compose.yml** → use it and continue normally.
2. **No Dockerfile** → tell the user at step 3 and do not proceed:
   > 💬 Detected a <language/framework> project. The built-in runtime installation only covers
   > Java / Python / Node (plus compiled languages such as Go and Rust), so your project will be
   > deployed via Docker — the general-purpose path in this skill, which works for any language.
   >
   > There is no `Dockerfile` in the project yet. I can generate one from the project structure for
   > you to review, or you can provide your own.

   Confirm with AskUserQuestion: **Generate a Dockerfile for me** / **I'll provide my own**.
   If generated, show the full contents and get user confirmation before moving on to step 4.

---

## nginx_mode Decision

| Condition | nginx_mode |
|-----------|------------|
| Has static artifacts + has app | `static+app` (default) |
| No static, pure app (Flask/Django/Streamlit etc.) | `proxy` |
| Pure static, no app | `static` |

> In `proxy` mode all requests are reverse-proxied to the app. Flask/Django/Streamlit/Gradio **must** use `proxy` —
> using `static+app` by mistake will cause `try_files` to intercept routes.

---

## Python Framework Startup Reference

| Framework | start_command | Default Port |
|-----------|---------------|--------------|
| FastAPI | `uvicorn main:app --host 0.0.0.0 --port 8080` | 8080 |
| Flask | `gunicorn -b 0.0.0.0:8080 app:app` | 8080 |
| Django | `gunicorn -b 0.0.0.0:8080 <project>.wsgi:application` | 8080 |
| Streamlit | `streamlit run app.py --server.port 8080 --server.headless true` | 8080 |
| Gradio | `python3 app.py` | 7860 |

---

## `--start-command` Explanation

`start_command` is the **full startup command** (relative to deploy directory `/opt/qwencloud`), not a file path.

- Go binary: `./server`
- Python: `python3 app.py` or `gunicorn -b :8080 app:app`
- Java: single jar `sh -c 'java -jar /opt/qwencloud/*.jar'`; multiple jars pass the real jar filename in the artifact
- Node: `node server.js`

---

## Build Commands for Git URL Sources

| Type | Build Command |
|------|---------------|
| Node.js | `npm install && npm run build` |
| Go | `go build -o <binary> .` |
| Python | `pip install -r requirements.txt` |
| Java | `mvn package -DskipTests` or `gradle build -x test` |
| Rust | `cargo build --release` |
| Docker | `docker build -t <name>:latest .` |

---

## Agent Decision Flow

1. Read `find` output to understand overall structure
2. Read config files for dependency manifests and build configuration
3. Read entry source to confirm framework and port
4. Read README for build/run instructions
5. If confident → decide directly; if uncertain → AskUserQuestion to ask

> ⚠️ After analysis: check for hardcoded secrets (keys, tokens, passwords). If found, warn the user.
