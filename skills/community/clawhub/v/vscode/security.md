# Security — Trust, Auto-Run, Extensions, and Secrets in Config

Opening a folder in an editor is closer to running its code than most people assume. A repository can ship a command that runs on open, point a "linter" at any executable, and recommend an extension that does anything at all. Trust is the gate on all of it.

**Contents:** [Threat Model In Three Lines](#threat-model-in-three-lines) · [Workspace Trust](#workspace-trust) · [What A Repository Can Execute](#what-a-repository-can-execute) · [Reviewing An Unknown Repository](#reviewing-an-unknown-repository) · [Extension Supply Chain](#extension-supply-chain) · [Secrets In Configuration](#secrets-in-configuration) · [Remote And Tunnel Exposure](#remote-and-tunnel-exposure) · [Telemetry And Data](#telemetry-and-data) · [Security Checklist](#security-checklist)

**Before trusting a folder or installing anything new**, read `## Extensions` in `~/Clawic/data/vscode/memory.md` for banned ids and past verdicts, and `## Environment` for the trust posture already established on this machine. `trust_posture` and `banned_extensions` in `config.yaml` are declarations — apply them, do not re-ask.

## Threat Model In Three Lines

1. **The repository is untrusted input.** Anyone who can open a pull request can propose a `.vscode/` change; anyone who can get you to clone can ship one.
2. **Extensions run with your user's full privileges.** There is no sandbox: an extension reads every file you can read and runs any process you can run.
3. **Configuration files are the densest place secrets end up**, because environment blocks live next to settings and everything in `.vscode/` looks committable.

## Workspace Trust

Restricted Mode is the only mechanism that separates "reading code" from "running it".

| In Restricted Mode | Effect |
|---|---|
| Tasks | Disabled, including auto-run on folder open |
| Debugging | Disabled |
| Machine-overridable settings from the workspace | Ignored — this is what stops a workspace pointing a tool at an arbitrary binary |
| Extensions that declare untrusted support | Run, possibly with reduced capability |
| Extensions that do not | Disabled for that folder |

- `security.workspace.trust.enabled` (application-scoped) governs the whole feature. Turning it off removes the only barrier there is.
- `security.workspace.trust.untrustedFiles` decides what happens to files opened from outside a trusted folder: prompt, open, or newWindow.
- **Parent folder trust** is the sharp edge: trusting a parent directory trusts everything beneath it, forever. Trusting your home directory or a `~/code` root defeats the feature for every repository you will ever clone.
- Multi-root workspaces can have trusted and untrusted roots simultaneously; the window operates at the lowest trust level present.
- Trust is per folder path and persists. Renaming a folder resets it; cloning to a new path prompts again.

## What A Repository Can Execute

Concretely, from files in the repo, once trusted:

- **`tasks.json` with `"runOptions": {"runOn": "folderOpen"}`** — a shell command at open, no prompt (`tasks.md`).
- **`settings.json` pointing a tool at an executable** — any setting whose value is a path to a linter, formatter, compiler or interpreter. The extension will run it.
- **`terminal.integrated.env.*` and `terminal.integrated.profiles.*`** — environment and shell for every terminal you open in that folder.
- **`.devcontainer/devcontainer.json` lifecycle commands** — `initializeCommand` runs **on your host**, before any container exists (`remote.md`).
- **`.vscode/extensions.json` recommendations** — a prompt, not an install, but a prompt that most people accept.
- **Build tooling the repo already has** — a `package.json` `postinstall`, a `Makefile`, a git hook. The editor is not the interesting attack surface once you run the build anyway.

None of this is a vulnerability; it is the feature set. The mitigation is reviewing before trusting, not disabling the features.

## Reviewing An Unknown Repository

Two minutes, in Restricted Mode, before trusting:

1. Read `.vscode/tasks.json` — anything with `runOn`, and what every command actually invokes.
2. Read `.vscode/settings.json` — any key whose value is a path to an executable, any `terminal.integrated.env.*`, any tool-path override.
3. Read `.devcontainer/devcontainer.json` — `initializeCommand` first, since it runs on the host.
4. Read `.vscode/extensions.json` — recognize the publishers; an unfamiliar one is worth a look before accepting the prompt.
5. Check git hooks (`.githooks/`, a configured `core.hooksPath`) — outside the editor's control and often forgotten.
6. Only then trust the folder.

For code you intend to read and never run, staying in Restricted Mode indefinitely is a legitimate end state, not a temporary inconvenience.

## Extension Supply Chain

- Extensions are published by anyone with an account. Publisher verification exists and means the publisher proved domain ownership — it says nothing about the code.
- Signals worth reading before installing something that touches code or the network: install count and age together (a new extension with a huge count is odd), the repository link resolving to real source, the changelog matching the version history, and whether the publisher owns other extensions you already trust.
- **Typosquatting** is the common attack: a near-identical name and icon for a popular extension. Verify the **id** (`publisher.name`), not the display name — the id is what `.vscode/extensions.json` and every install command use.
- An extension that requests nothing at install time can still do everything at runtime; there is no permission model. The install decision is the entire security decision.
- Auto-update means the code changes without a decision. That is the right default for most people and the reason a compromised publisher account affects everyone quickly; it is also why pinning a version after any doubt is cheap (`extensions.md`).
- Removing an extension leaves its data behind in the user directory. A removed extension that was doing something unwanted should be followed by clearing its storage.

## Secrets In Configuration

Where they end up, and what to do instead:

| Place | Why it happens | Instead |
|---|---|---|
| `terminal.integrated.env.*` in user settings | Convenient, and it syncs | An OS keychain entry, a gitignored env file the shell sources |
| `terminal.integrated.env.*` in workspace settings | Committed to the repository | Never; this is a leak with a commit hash |
| `tasks.json` `options.env` | The task needed a token | An env file read by the tool, kept out of version control |
| `launch.json` `env` | The debug session needed one | `envFile` pointing at a gitignored file |
| `devcontainer.json` `containerEnv` / `remoteEnv` | The container needed one | A secret mechanism from the container runtime, or a gitignored env file |
| A `promptString` input with `password: true` | Looks safe | The value reaches the command line and the terminal scrollback anyway |
| A git remote URL with an embedded token | It made a push work once | A credential helper (`git.md`) |

Settings Sync makes any user-settings secret a multi-machine secret. `settingsSync.ignoredSettings` exists, but the correct answer is that the value never goes there.

**Nothing under `~/Clawic/data/` ever holds a secret value** — not the files this skill declares, not files it creates, and not text the user pastes in for safekeeping. A pasted `settings.json`, `tasks.json`, `launch.json` or `devcontainer.json` is exactly the dense case: strip every value before writing and leave its pointer, in the shape `<kind>:<locator>` — `env:GITHUB_TOKEN`, `keychain:npm-publish`, `1password:Work/Registry/ci`, `file:~/.ssh/id_ed25519`. Say in one line that you did it. Extension ids, setting keys, ports, host names and file paths are working data and stay (`memory-template.md`).

## Remote And Tunnel Exposure

- A **tunnel** is remote access to that machine for whoever controls the registered account, from anywhere, without an inbound port. Enabling one on a machine with production access is a decision, not a convenience.
- A tunnel running as a service survives reboots and logouts. Know which mode you started.
- **Forwarded ports** default to private; making one public exposes a local service to anyone with the URL. Check the visibility column in the Ports panel before assuming (`remote.md`).
- **SSH agent forwarding** lets anything running as root on that host use your agent for as long as you are connected. Forward to hosts you administer, not to shared boxes.
- A dev container runs your code with your mounted source tree; `initializeCommand` runs outside it, on the host. That distinction is the one worth remembering.

## Telemetry And Data

- `telemetry.telemetryLevel` (`all` / `error` / `crash` / `off`) is application-scoped, so it can only be set in user settings, and it governs the editor's own reporting.
- Extensions have their own telemetry; the editor's level is respected by well-behaved ones and is not enforced. An extension's privacy statement is the only source for what it sends.
- Settings Sync stores your settings, keybindings, snippets and extension list against your account. It syncs configuration, not source code.
- Forks change all of this: a different build has a different telemetry posture and different defaults (`forks.md`).

## Security Checklist

| Check | Passing looks like |
|---|---|
| Trust | Restricted Mode is on by default; no parent folder covering all your repositories is trusted |
| Auto-run | No `runOn: folderOpen` you did not read; any one you ship is documented |
| Executable-path settings | No workspace setting points a tool at a binary you did not verify |
| Extension ids | Every installed id matches the publisher you intended; banned ids absent |
| Secrets in settings | No token, key or password in user, workspace, task, launch or devcontainer configuration |
| Committed `.vscode/` | Nothing personal, nothing absolute, nothing secret (`workspaces.md`) |
| Tunnels | None running that you did not start; none installed as a service unintentionally |
| Forwarded ports | Nothing public that should not be |
| Agent forwarding | Only to hosts you administer |
| Stored data | Nothing under `~/Clawic/data/` holds a secret value; every one is a pointer |

**After any security decision** — an extension banned or accepted with a reason, a repository trusted or deliberately left restricted, a tunnel enabled, an agent-forwarding policy — write it to `~/Clawic/data/vscode/artifacts/decision-<what>.md` with the date, what was rejected and the condition to revisit, plus its `## Boxes` line in the same turn (`memory-template.md`). A ban also goes to `banned_extensions` in `config.yaml`, because that is a declaration. An extension audit cadence belongs in `## Due`: a list vetted a year ago has a year of auto-updates on top of it.
