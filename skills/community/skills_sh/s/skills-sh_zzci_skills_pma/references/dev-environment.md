# PMA Dev Environment

Cross-cutting dev-runtime conventions used by every stack skill (`pma-web`, `pma-bun`, `pma-go`, `pma-rust`). Stack skills carry only the stack-specific invocation; the protocol lives here.

## Table of Contents

- [Dev URL Routing (nsl)](#dev-url-routing-nsl)
- [Tmux Process Lifecycle](#tmux-process-lifecycle)

## Dev URL Routing (nsl)

`@nsio/nsl` is a local reverse proxy that maps named `.localhost` URLs to dynamically allocated ports. Each app process — frontend or backend, in any language — runs independently and registers itself with nsl; nsl unifies them under one host and one port (default `:3355`), so the browser sees a single origin and routes like `/api` resolve to the right backend without any in-process middleware bridge.

This **replaces** the previous patterns:

- `@hono/vite-dev-server` mounting the API inside Vite
- Vite `server.proxy` blocks
- The frontend importing the API package as middleware

### Why use nsl

- Backend can be any language (Bun, Go, Rust, Python, …). Frontend does not import or proxy the backend.
- Vite config stays plain. No backend-aware plugins.
- Dev is **same-origin** (e.g. `http://myapp.localhost:3355` for both UI and `/api`). Cookies, CORS, and CSP behave the way they will in production — no dev-only workarounds.
- Identical model across stacks. The same nsl URL works whether the backend is `pma-bun`, `pma-go`, `pma-rust`, or external.

### Install

Install once per project (typically as a devDependency of the SPA package; add globally only if no JS package owns the dev workflow):

```bash
bun add -D @nsio/nsl
```

After install, invoke through `bunx nsl ...` (or wrap in package.json scripts). No global install required.

### Mental model

- Each app process is registered under a host name like `myapp.localhost` (and optionally a path prefix like `myapp:/api`).
- nsl listens on `:3355` by default and reverse-proxies `<name>.localhost:3355[/<path>]` to the registered process port.
- nsl allocates a free port for each child process and exports it as the `PORT` environment variable. Tools that read `PORT` (Vite, Bun's `Bun.serve()`, most Node frameworks, FastAPI/uvicorn, Axum + std env, Chi + std env, …) bind correctly with no extra flags.
- For tools that ignore `PORT`, pass the literal placeholder `NSL_PORT` in the child command — nsl substitutes the allocated port at spawn time.

### Two registration patterns

**A. Wrap the launch with `nsl run` (preferred when nsl manages the lifetime).**

```bash
# Frontend (Vite reads PORT)
bunx nsl run vite

# Backend with a path prefix; --strip removes /api before forwarding
bunx nsl run -n myapp:/api -s -- bun --watch src/index.ts

# Tool that only accepts a CLI port flag
bunx nsl run -n myapp:/api -s -- ./target/debug/myapp-server --port NSL_PORT
```

`-n NAME[:/PATH]` overrides the auto-inferred project name and optionally mounts under a path. `-s` (`--strip`) drops the matched prefix before forwarding, so handlers stay mounted at their domain paths (`/users`, `/orders`, …) and remain unaware of the public mount point.

**B. Register a static route after the process is up (for processes nsl does not launch).**

```bash
# Backend already listening on 8787
bunx nsl route myapp:/api 8787 --strip
```

Use this when the backend has its own launcher (Docker, systemd, IDE run config) and nsl only needs to know where it lives.

### URL layout

For a project named `myapp`:

```text
http://myapp.localhost:3355        -> frontend
http://myapp.localhost:3355/api    -> backend (with /api stripped before forwarding)
```

The frontend HTTP client uses `/api` as a relative base URL — same-origin in dev means no special config or CORS handling is needed.

### Multi-app layout

Each app gets its own host name. They can coexist on the same nsl daemon:

```text
http://app.localhost:3355          -> main SPA
http://app.localhost:3355/api      -> main API
http://admin.localhost:3355        -> admin SPA
http://admin.localhost:3355/api    -> admin API
```

This is the model used by the *Monorepo* layout — see [`docs/monorepo-example.md`](../docs/monorepo-example.md).

### Public dev domains

nsl is not limited to `*.localhost`. Each daemon can be configured (see `nsl status` → `proxy.domains`) to serve additional domains, for example a shared team domain like `*.a.fr.ds.cc`. The `Host` header forwarded to your dev server reflects whichever domain the user typed.

Practical consequences:

- A SPA dev server (Vite) must accept the public hostname. For Vite this is `server.allowedHosts` — see the per-stack guidance in `pma-web/references/runtime-and-data.md` for how to choose between an explicit list and `true`.
- Backend frameworks rarely care about `Host`. If yours does (e.g. strict virtual-host matching, CSRF based on Origin/Host), document the public domain there too.
- Cookies and CSP that pin to `localhost` will not work over a public domain. Prefer `Domain`-less cookies and same-origin CSP that follow whatever host the client used.

### Verification

```bash
bunx nsl list         # all active routes
bunx nsl get myapp    # the URL for one app (script-friendly)
bunx nsl status       # daemon state, ports, config
```

If the daemon is not running, start it once: `bunx nsl start`.

### Fallback

When the dev environment cannot run the nsl daemon at all (CI containers, sandboxed CI runners, restricted developer machines), use the stack skill's `dev:bare` script (plain `bunx --bun vite` or plain `bun --watch src/index.ts`) and accept that:

- frontend and backend will be on different ports
- you will need a temporary `server.proxy` block or absolute `http://localhost:<port>` URLs in the client (do **not** commit either)
- CORS / cookie behavior will diverge from production

Treat the bare path as the exception, not the baseline.

### Anti-patterns

- Do **not** add `@hono/vite-dev-server` or any backend-mounting Vite plugin.
- Do **not** add a `server.proxy` block in committed Vite config.
- Do **not** import the backend package from the frontend for runtime middleware mounting (a circular dependency between independently deployed processes).
- Do **not** hard-code `localhost:<port>` in the frontend HTTP client.
- Do **not** add per-developer hosts file entries; nsl already owns `*.localhost` resolution.

## Tmux Process Lifecycle

For starting and managing the dev processes themselves (Vite, `bun --watch`, `cargo run`, …), follow the tmux conventions in [`delivery.md`](./delivery.md). nsl handles URL routing; tmux handles the process lifetime.
