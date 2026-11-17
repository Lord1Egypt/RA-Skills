# Terminal — Shells, PATH, and the Environment the Editor Actually Has

Three different environments are in play and people conflate them: the process environment the editor was launched with, the environment it resolves from your login shell, and the environment inside a terminal you just opened. Almost every "command not found" is a mismatch between two of them.

**Contents:** [The Three Environments](#the-three-environments) · [Shell Environment Resolution](#shell-environment-resolution) · [Profiles](#profiles) · [Environment Variables](#environment-variables) · [Shell Integration](#shell-integration) · [The `code` Command](#the-code-command) · [Persistent Sessions And Splits](#persistent-sessions-and-splits) · [Terminal Failure Signatures](#terminal-failure-signatures)

**Before diagnosing a missing tool or variable**, read `## Environment` in `~/Clawic/data/vscode/memory.md` — the shell, the version manager, and any rc-file guard that had to be added were recorded the first time this cost an hour.

## The Three Environments

| Environment | Where it comes from | Who uses it |
|---|---|---|
| **Process environment** | Whatever launched the editor — a Dock/Start-menu click gives you the OS session's environment, a `code .` from a shell gives you that shell's | Extensions, tasks, debug sessions, language servers |
| **Resolved shell environment** | The editor runs your login shell once at startup and imports what it prints (macOS and Linux) | Merged into the process environment for extensions and tasks |
| **Terminal session environment** | A fresh shell, sourcing your rc files, plus editor-injected variables | Only what you type in the terminal |

The consequence that explains most of this file: **a tool available in the integrated terminal may be invisible to a task, a debug session or a language server**, because the terminal sourced your rc file and they only got the process environment plus whatever resolution produced.

And its converse: changing your PATH in a shell rc file requires a **full quit and relaunch** of the editor to affect the process environment. `Developer: Reload Window` reloads the window inside the same process and keeps the old environment — this is the single most common wasted debugging hour in this domain.

## Shell Environment Resolution

On macOS and Linux, the editor launches your login shell at startup to learn your PATH. It fails when the shell does anything other than print an environment.

- "Unable to resolve your shell environment" means the rc file printed output, prompted for input, took too long, or exited non-zero. The message names the shell but not the line.
- The fix is to guard interactive-only content. In `~/.zshrc` or `~/.bashrc`, wrap banners, prompts, `fastfetch`-style output and interactive tool init in a check for an interactive shell, and keep PATH exports above the guard.
- Version managers are the usual offenders and the usual victims: an nvm/pyenv/rbenv init that prints or that only runs for interactive shells leaves the editor with no toolchain, which then presents as a broken language server (`languages.md`).
- `terminal.integrated.inheritEnv` (default true) controls whether new terminals inherit the editor's environment on top of the shell's. Setting it false gives terminals a clean shell environment — useful when the editor's inherited environment is the thing that is wrong.
- The reliable escape from the whole problem: launch the editor from a shell (`code .`) so the process environment is already correct. The reliable diagnosis: compare `env` in the integrated terminal against the environment an extension reports.

## Profiles

A terminal profile is a shell plus arguments plus environment.

```json
{
  "terminal.integrated.profiles.osx": {
    "zsh-login": { "path": "zsh", "args": ["-l"] },
    "project": { "path": "zsh", "args": ["-l"], "env": { "NODE_ENV": "development" } }
  },
  "terminal.integrated.defaultProfile.osx": "zsh-login"
}
```

- Profiles are per platform: `.osx`, `.linux`, `.windows`. Setting the wrong one is silent.
- `defaultProfile` is machine-overridable, so a workspace can set it only in a trusted folder (`security.md`) — and a repo that sets it is choosing which shell runs your commands, which is worth noticing.
- Login shell (`-l`) sources profile files; a non-login interactive shell may not. A tool present in one terminal and absent in another is usually two profiles with different flags.
- `automationProfile` is a separate setting for the shell that runs **tasks**, which is how you give tasks a minimal fast shell while keeping a heavy interactive one for yourself (`tasks.md`).
- On Windows, the choice between PowerShell, `cmd`, Git Bash and a WSL distro changes path semantics entirely; a task written for one fails on another (`remote.md`).

## Environment Variables

Precedence, lowest to highest, for a new terminal:

1. The editor's process environment.
2. What the shell's rc files set.
3. `terminal.integrated.env.<platform>` from settings.
4. Variables injected by extensions ("Environment Variable Collection" — the terminal shows a warning icon when an extension has modified the environment; hovering it lists what changed and who did it).

Rules:

- `terminal.integrated.env.*` is a settings value. **Never put a token there** — settings sync, it is committed if a workspace sets it, and it lands in every terminal's environment (`security.md`).
- A workspace setting an env var only takes effect in a trusted folder.
- The extension-injected layer is the one people cannot explain. The warning icon is the answer; the "relaunch terminal to apply" prompt is that layer changing after the terminal opened.
- Variables for a *task* come from `options.env` in `tasks.json`; variables for a *debug session* come from `env`/`envFile` in `launch.json`. Neither reads your rc file.

## Shell Integration

Shell integration lets the editor know where commands start and end. It powers command decorations in the gutter, `Terminal: Run Recent Command`, sticky scroll in the terminal, and accurate cwd detection for new splits.

- It is injected automatically for common shells; for unusual setups it can be sourced manually from the shell's rc file.
- It breaks when a prompt framework rewrites the prompt escape sequences it relies on. The symptom is decorations disappearing after installing a prompt theme.
- `terminal.integrated.shellIntegration.enabled: false` turns it off — the right move when it fights your prompt, and a real loss of functionality otherwise.
- The cwd detection matters beyond convenience: splitting a terminal inherits the detected cwd, and without integration the split starts at the workspace root instead of where you were.

## The `code` Command

- On macOS it is installed from the command palette (`Shell Command: Install 'code' command in PATH`); on Linux and Windows it usually comes with the package.
- Flags that earn their place: `--diff a b`, `--merge base a b result`, `--goto file:line:col`, `--wait` (blocks until the file is closed — what makes it usable as `$EDITOR` and `$GIT_EDITOR`), `--add folder` (adds to the current multi-root workspace), `--new-window`, `--reuse-window`.
- Diagnostic flags: `--status`, `--verbose`, `--log trace`, `--disable-extensions`, `--user-data-dir <tmp>`, `--extensions-dir <path>`, `--prof-startup` (`performance.md`).
- Forks ship their own command name (`codium`, `cursor`, `windsurf`, `code-insiders`). A script hardcoding `code` breaks on a fork (`forks.md`).
- In a remote window, `code` inside the integrated terminal is a shim that talks back to your local editor — which is why `code file.txt` on an SSH host opens locally in the right window instead of trying to run an editor on the remote.

## Persistent Sessions And Splits

- Terminals are restored across window reloads by default (`terminal.integrated.enablePersistentSessions`), reconnecting to the same shell process. A long-running process survives a reload but not a full quit.
- `terminal.integrated.persistentSessionReviveProcess` controls whether the process is actually revived or just the terminal shell restored.
- Over SSH, persistent sessions live on the remote server process; a dropped connection reconnects to the same terminals when the server survived (`remote.md`).
- For anything that must outlive the editor entirely, use a multiplexer on the host. Editor persistence is a convenience, not a session manager.
- `terminal.integrated.scrollback` defaults to a bounded buffer; a build that prints a hundred thousand lines has already lost its head. Redirect to a file when the output matters.

## Terminal Failure Signatures

| Signature | Cause | First move |
|---|---|---|
| Tool found in terminal, not in a task or language server | Terminal sourced rc files, the process did not | Launch from a shell, or fix shell-env resolution |
| Tool found nowhere in the editor, found in a real terminal | PATH changed after the editor started | Full quit and relaunch, not Reload Window |
| "Unable to resolve your shell environment" | rc file prints, prompts, blocks, or exits non-zero | Guard interactive-only content |
| Wrong shell on new terminals | `defaultProfile.<platform>` unset or set for the wrong platform | Per-platform key |
| Env var missing in one terminal only | Profile-specific `env`, or an extension's collection | Hover the terminal's warning icon |
| Prompt decorations disappeared | Shell integration broken by a prompt framework | Re-source integration or disable it |
| `code` not found | Shim not installed, or a fork with a different command name | Install from the palette; check the fork's name |
| Terminal opens at the workspace root instead of the current folder | No shell integration, so no cwd detection | Enable it, or set `cwd` explicitly |
| Anything else | Compare `env` in the terminal with the environment an extension reports; the delta is the answer | — |

**When an environment fact costs time to establish** — the rc-file guard that fixed shell resolution, the version manager the editor cannot see, a proxy or corporate CA needed by extension installs, the profile flags that produce a usable shell — write it as a line in `## Environment` of `~/Clawic/data/vscode/memory.md` in the same turn (`memory-template.md`). If the fix was a terminal profile block worth reusing, it goes to `artifacts/settings-terminal.md` with its `## Boxes` line. A declared shell preference is a declaration: `platform.shell` in `config.yaml`, not memory.
