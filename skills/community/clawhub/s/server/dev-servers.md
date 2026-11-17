# Local Development Servers

The rules here are different from every other file in this skill: the development server is a tool for one person, not a service. Its conveniences are dangerous in production, and its problems are almost all about how the browser talks to two servers at once.

**Before assigning a local port**, read `conventions.port_range` in `~/Clawic/data/server/config.yaml`: this user's app and admin ranges are already decided, and a dev server squatting on the range a real service uses is a conflict you meet on the box, not on the laptop.

**Contents:** [Never in Production](#never-in-production) · [Binding and Reaching It](#binding-and-reaching-it) · [Port Conflicts](#port-conflicts) · [Proxying the API](#proxying-the-api) · [HMR and WebSockets](#hmr-and-websockets) · [HTTPS Locally](#https-locally) · [Tunnels and Sharing](#tunnels-and-sharing) · [Docker in the Dev Loop](#docker-in-the-dev-loop) · [Matching Production Enough](#matching-production-enough) · [Write It Down](#write-it-down)

## Never in Production

Framework dev servers — the Django and Flask built-ins, `next dev`, `vite`, `webpack-dev-server`, `php -S` — are single-connection or single-process, unhardened, and often serve source maps and directory listings by design. They are not slow versions of production servers; they are different programs.

The tell that one escaped: a production box serving on port 3000/5173/8000 directly, or a `NODE_ENV` that is not `production`, or hot-reload assets in a live page. Fix by building and serving the build output behind the real proxy (`stack.md`), not by tuning the dev server.

## Binding and Reaching It

Most dev servers bind `127.0.0.1` by default, which is right for a laptop and wrong the moment you want to test on a phone:

| Goal | Do |
|---|---|
| Test on a phone on the same Wi-Fi | Bind `0.0.0.0` (`--host 0.0.0.0`, `--host` in Vite) and use the laptop's LAN IP |
| Test from a VM or a container | Bind `0.0.0.0`; `localhost` inside the VM is the VM |
| Keep it private on an untrusted network | Leave it on `127.0.0.1` — a dev server on `0.0.0.0` in a café is an open filesystem |

Vite and similar tools also enforce an allowed-hosts list; reaching the server by an unexpected hostname returns a blocked-request error rather than a connection failure, and the fix is the config, not the network.

## Port Conflicts

`EADDRINUSE` in development is usually a previous run that did not die: a crashed watcher, a debugger holding the port, or a container still up. Find the holder (`lsof -i :5173`) before picking a different port — moving to 5174 leaves the old process running and eventually you have four.

Many dev servers auto-increment to the next free port and print it quietly. That is why the app "sometimes" cannot reach the API: the API moved and the proxy config did not. Pin the port explicitly in project config for anything another process needs to find.

## Proxying the API

The single fix for development CORS: serve the API through the dev server's own origin instead of relaxing the API's headers.

```javascript
// vite.config.js
server: {
  proxy: {
    '/api': { target: 'http://127.0.0.1:8000', changeOrigin: true }
  }
}
```

Now the browser makes same-origin requests and CORS never enters the picture — which also means the production configuration is not weakened to make a laptop work. Cookies work too, because the origin matches, and the whole class of "works in dev, breaks in prod" auth bugs disappears.

`changeOrigin` rewrites the `Host` header to the target's; needed when the API validates host, harmful when it uses the original host to generate links. Know which yours does.

When a wildcard `Access-Control-Allow-Origin` genuinely is added to unblock a demo, it must be written into the deploy record as a thing to remove; otherwise it ships (`debug.md`).

## HMR and WebSockets

Hot module replacement runs over a WebSocket, and it is the first thing to break behind any proxy or tunnel:

- Through a reverse proxy, the upgrade headers must be forwarded on the HMR path as well as the app path (`proxy.md`).
- Over HTTPS, the HMR socket must be `wss://`, not `ws://` — browsers block mixed content, and the console message names the socket rather than the cause.
- Behind a tunnel or a nonstandard port, the client's HMR endpoint has to be told explicitly (`server.hmr.clientPort`, `host`, `protocol`), because it defaults to the page's origin and the tunnel's origin is not the dev server's.
- A page that loads but never hot-reloads, with a repeating connection error in the console, is always this. The app is fine.

## HTTPS Locally

Needed for service workers, secure cookies, WebAuthn, camera and microphone APIs, and anything that behaves differently on a secure origin.

- A locally trusted CA tool (`mkcert` and equivalents) generates a certificate the browser trusts because you installed the CA locally. This is the clean path.
- A self-signed certificate produces a browser warning that also blocks WebSocket and fetch in ways that are hard to read — click-through works for pages, not for subresources.
- `localhost` is already a secure context in browsers without any certificate: if the only requirement is a secure context, use `localhost` rather than a certificate.
- Never install a development CA on a shared or production machine, and never reuse a development certificate anywhere real.

## Tunnels and Sharing

Exposing a dev server publicly to demo it or receive a webhook:

- Set the allowed-hosts entry for the tunnel domain, or the framework rejects the request before your code sees it.
- Webhooks need a stable path; ephemeral tunnel URLs change on restart and every provider then has a dead endpoint registered.
- A tunnel bypasses your firewall entirely. That is the point, and it means the dev server — with its source maps, its debug endpoints, and no authentication — is on the internet for as long as the tunnel is up. Close it when the demo ends.
- Never tunnel a dev server that talks to production data.

## Docker in the Dev Loop

- Bind-mount the source, but keep `node_modules` (or the equivalent) in a container volume: mounting the host's is slow on macOS/Windows and installs native modules built for the wrong platform.
- File watching often fails across a bind mount because inotify events do not cross it; enable polling in the watcher (`usePolling`) at the cost of CPU.
- Inside a container, `localhost` is the container. The API is at the service name (`api:8000`) or at `host.docker.internal` if it runs on the host (`containers.md`).
- Bind the dev server to `0.0.0.0` inside the container, or the published port reaches nothing — this is the most common "the container is running but the page will not load".

## Matching Production Enough

Development does not need to be production, but a few mismatches produce bugs that only appear after deploy:

| Mismatch | Bug it produces |
|---|---|
| No reverse proxy in dev | Forwarded-header handling and path rewriting are first exercised in production (`proxy.md`) |
| HTTP in dev, HTTPS in production | Secure-cookie and mixed-content failures at launch |
| Different database version | A query that works locally and fails live |
| Case-insensitive filesystem locally | An import with the wrong case builds locally and 404s on Linux |
| No compression, no cache headers in dev | Performance work that cannot be validated until it is live (`static.md`) |
| Seeded tiny dataset | Everything is fast until real data arrives (`capacity.md`) |

The cheapest high-value alignment is running the same proxy locally in front of the dev server: it is one config file, and it moves an entire class of bug from production to the laptop.

## Write It Down

Development configuration is per-project and belongs in the project's repository, not in this skill's data. The one thing worth persisting is a **convention**: the port ranges this user assigns to apps and admin UIs, and their dev-proxy pattern. Those are declared preferences and go in `~/Clawic/data/server/config.yaml` under `conventions` when the user states them (`memory-template.md`) — never in `memory.md`, and never a project's local URLs or credentials.
