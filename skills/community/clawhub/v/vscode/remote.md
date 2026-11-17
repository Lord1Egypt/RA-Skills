# Remote — SSH, WSL, Dev Containers, Tunnels, and Which Side Runs What

A remote window is two processes: a local UI and a server on the target. Extensions, terminals, tasks, debuggers and the file system live on the server side. Knowing which side a thing runs on answers most questions before any configuration.

**Contents:** [The Split](#the-split) · [Extension Kind](#extension-kind) · [Remote-SSH](#remote-ssh) · [Dev Containers](#dev-containers) · [WSL](#wsl) · [Tunnels And Codespaces](#tunnels-and-codespaces) · [Port Forwarding](#port-forwarding) · [Settings And Files Across The Boundary](#settings-and-files-across-the-boundary) · [Server Hygiene](#server-hygiene) · [Remote Failure Signatures](#remote-failure-signatures)

**Before connecting or debugging a remote setup**, read `~/Clawic/data/servers/servers.md` (which hosts exist, their role and the access pointer) and `## Environment` in `~/Clawic/data/vscode/memory.md` (glibc floors, proxy and CA requirements, server-cleanup history). `remote_mode` in `config.yaml` says which of these applies by default.

## The Split

| Runs locally | Runs on the remote / in the container |
|---|---|
| The window, themes, keymaps | The file system you browse and edit |
| UI-only extensions | Language servers, linters, formatters, debuggers, test runners |
| Settings Sync, profiles | The integrated terminal and every task |
| Port-forwarding client | Every process your code starts |

Consequences worth stating: a tool must be installed **on the remote** to be usable; a task's `cwd` is a remote path; a `launch.json` path resolves on the remote; and your local shell configuration is irrelevant to anything except the local UI.

## Extension Kind

Every extension declares an `extensionKind`: `ui`, `workspace`, or both. The Extensions view splits the list into "Local — Installed" and "<target> — Installed" for exactly this reason.

- Installing a `workspace` extension while a remote window is open installs it **into the remote** by default. Installing it from a local window does nothing for the remote.
- Themes and keymaps (`ui`) are correctly local: they need no access to the code.
- An extension declaring both runs where it is installed; a duplicate install on both sides is the cause of duplicate diagnostics in a remote window (`extensions.md`).
- `remote.extensionKind` overrides the declaration for a specific extension. Reach for it only when the default genuinely breaks something — it is the setting most likely to cause a confusing state later.
- Recommendations in `.vscode/extensions.json` install on the appropriate side automatically, which is why a repo used remotely should still ship them (`workspaces.md`).

## Remote-SSH

- Connection uses your `~/.ssh/config`. The host name in the picker is the `Host` entry; `remote.SSH.configFile` points at a different file when you keep work hosts separate.
- `ProxyJump` and `ProxyCommand` work because the editor uses the system `ssh`. A bastion setup that works in a terminal works here.
- Key-based authentication with an agent is effectively required: the connection is re-established several times during a session, and a password prompt each time is unusable.
- The server is installed to a per-version directory under the user's home on the remote (`~/.vscode-server` or the fork's equivalent). First connection downloads it, which needs outbound network from the *remote host* — an air-gapped host needs the server transferred manually.
- **The server has a C library floor**: modern versions require a reasonably current glibc (`vscode >=1.86` dropped support for older distributions). An old server distribution cannot host a new client, and the failure is a connection that closes immediately with a library error in the log. Pinning the client to an older release, or upgrading the host, are the only two answers.
- `remote.SSH.remotePlatform` tells the extension the host's OS when detection fails — necessary for non-Linux targets.
- Agent forwarding (`ForwardAgent yes`) is what lets git on the remote authenticate with your local key (`git.md`). Forward deliberately: any root on that host can use the forwarded agent while you are connected.
- Connection logs are in the Remote-SSH output channel and contain the exact `ssh` command line — reproduce it in a terminal to separate an SSH problem from an editor problem.

## Dev Containers

`.devcontainer/devcontainer.json` defines the environment. A Dockerfile alone is never enough — the editor does not auto-detect one.

```jsonc
{
  "name": "api",
  "dockerComposeFile": "../docker-compose.yml",
  "service": "api",
  "workspaceFolder": "/app",
  "features": { "ghcr.io/devcontainers/features/node:1": {} },
  "customizations": { "vscode": { "extensions": ["dbaeumer.vscode-eslint"], "settings": {} } },
  "forwardPorts": [3000],
  "remoteUser": "node",
  "postCreateCommand": "pnpm install"
}
```

- `image` / `build` / `dockerComposeFile` are the three mutually exclusive ways to specify the container. With compose, `service` and `workspaceFolder` are mandatory and `workspaceFolder` must match where the code is actually mounted.
- `customizations.vscode.extensions` is what installs extensions **inside** the container. Extensions installed by hand into a container are lost on rebuild; this list is the durable form.
- **Lifecycle commands**, in order: `initializeCommand` (on the host, before the container), `onCreateCommand`, `updateContentCommand`, `postCreateCommand` (once, after creation), `postStartCommand` (every start), `postAttachCommand` (every attach). Putting `install` in `postStart` reruns it every time you open the folder; putting it in `postCreate` runs it once and skips it after a dependency change. Neither is wrong — pick by whether the state lives in the image or in a volume.
- `remoteUser` decides file ownership of everything the container writes into the mount. A mismatch with your host UID is the cause of files you cannot edit after a container session (`docker`).
- **Performance**: bind-mounting a source tree into a container on macOS or Windows crosses a virtualization boundary and is slow for dependency directories. Put `node_modules`, `.venv`, `target` and build output in a named volume rather than the bind mount.
- `features` compose reusable toolchain installs and are the maintainable alternative to a hand-written Dockerfile per project.
- Rebuild vs Reopen: "Rebuild Container" reruns the build and the create commands; "Reopen in Container" reuses the existing one. A config change that appears not to apply needs the former.

## WSL

- Each distribution is a separate remote target with its own server installation and its own extension set.
- **Keep the code inside the Linux filesystem.** A repository at `/mnt/c/...` is accessed through a translation layer and is dramatically slower for file watching and for any tool that stats thousands of files; a repository under the distro's home is not.
- Windows tools and Linux tools both being on the PATH inside WSL means `node`, `git` or `python` may resolve to the Windows binary, with Windows path semantics. This produces errors that look like a broken toolchain.
- Line endings: a repo shared between Windows and WSL needs a consistent policy, or every file shows as modified. `.gitattributes` is the durable fix; `files.eol` in settings only affects new files.

## Tunnels And Codespaces

- A **tunnel** exposes a machine you control through a relay so you can reach it from another network or from a browser, with no inbound port. The machine runs a server process that must stay running; it is a session, not a service, unless installed as one.
- Access control is the account the tunnel is registered to. A tunnel is remote shell access to that machine for whoever holds that account — treat it with the same care as an SSH key (`security.md`).
- **Codespaces** is a hosted variant of the dev container model: the same `devcontainer.json`, with prebuilds and machine sizes on top. Everything in the Dev Containers section applies; the differences are lifecycle and billing, not mechanism.
- Browser-based windows lose some keybindings to the browser itself, and the clipboard behaves differently. Expect a keymap that is subtly not yours (`keybindings.md`).

## Port Forwarding

- The editor detects a port opened by a process in the terminal and forwards it automatically. The Ports panel lists what is forwarded, on which local port, and lets you change visibility.
- `forwardPorts` in `devcontainer.json` declares ports up front; `remote.autoForwardPorts` and `remote.autoForwardPortsSource` tune the automatic behavior.
- A port that "does not forward" is usually a process bound to `127.0.0.1` **inside** the target: from the target's perspective, nothing else can reach it. Bind to `0.0.0.0` there.
- Making a forwarded port public shares it beyond your machine. It is a deliberate act with a real exposure — check the visibility column before assuming a port is private.
- Local port collisions are silent: the panel shows the local port actually used, which may not be the one you expect.

## Settings And Files Across The Boundary

- **Remote settings** are a full scope between user and workspace (`settings.md`). Machine-specific values for that host belong there, not in your user settings.
- Workspace settings live in the repository on the remote and apply normally.
- Your local user settings apply to the UI; a setting that only affects the server side has no effect from the local file.
- Files: drag and drop copies across the boundary; the terminal's `code` command opens remote files in your local window (`terminal.md`).
- `.gitignore`, formatter configs and everything else the tooling reads live on the remote, because the tooling runs there.

## Server Hygiene

- Each editor version installs its own server directory on the remote and old ones are not always removed. On a host you connect to for a year, this is gigabytes.
- Symptom of a full home directory on the remote: connections that fail during install, or a server that starts and immediately dies. Check free space before debugging anything else.
- "Kill VS Code Server on Host" is the reset for a wedged server; the next connection reinstalls it.
- Orphaned server processes from dropped connections accumulate on a shared host. Periodically checking for them is a legitimate `## Due` cadence, alongside pruning old server versions.

## Remote Failure Signatures

| Signature | Cause | First move |
|---|---|---|
| Connection closes immediately after authenticating | Unsupported C library on the host, or no space in the home directory | Read the Remote-SSH output channel; check free space |
| Connects, then no language features | Workspace extensions installed locally only | Install into the remote (Extension Kind) |
| Terminal works, task cannot find a tool | Tool not on the remote's non-interactive PATH | `terminal.md`, applied to the remote's shell |
| Breakpoints hollow only in the container | Debugging *into* the container instead of *from* it | Path mapping (`debugging.md`) |
| Container starts, config change has no effect | Reopened rather than rebuilt | Rebuild Container |
| Everything slow on macOS/Windows containers | Dependency directories on a bind mount | Named volume for them |
| Everything slow in WSL | Repository under `/mnt/c` | Move it into the distro's filesystem |
| Wrong `node`/`python` inside WSL | Windows PATH inherited into the distro | Check `which`; fix the distro's PATH |
| Port unreachable despite forwarding | Bound to localhost inside the target | Bind `0.0.0.0` |
| Git asks for credentials on the remote | Local helper does not apply there | Agent forwarding, or a helper on the host |
| Extension present but inert | Installed on the wrong side, or duplicated on both | Extensions view, both groups |
| Anything else | Reproduce over plain `ssh` or `docker exec`; if it fails there, it is not an editor problem | — |

**After connecting to a machine from the editor**, write its row in the shared inventory `~/Clawic/data/servers/servers.md` — `Name` + `Provider` is the identity, update in place, `Role` says `remote-ssh dev host`, `tunnel host` or `devcontainer host`, cost carries its currency, and the access column is a pointer (`file:~/.ssh/id_ed25519`), never a key (`memory-template.md`). **When a devcontainer or SSH configuration finally works**, it goes to `~/Clawic/data/vscode/artifacts/devcontainer-<repo>.md` with its `## Boxes` line in the same turn. Host-level facts that will break the next connection — library floors, proxy and CA requirements, forwarded-agent policy, disk pressure from old servers — go in `## Environment`, and a server-cleanup cadence goes in `## Due`.
