---
name: VSCode
slug: vscode
version: 1.0.2
description: 'Configures, debugs, and speeds up Visual Studio Code: settings scopes, launch.json, tasks.json, extensions, keybindings, formatters, and remote work. Use when a setting has no effect because something else overrides it, when format-on-save runs the wrong formatter or two formatters fight, when a breakpoint stays hollow, F5 does nothing, or a debug config will not attach, when a watch task hangs preLaunchTask forever, when the extension host crashes or two extensions collide, when IntelliSense dies and the TypeScript server or Python interpreter stops resolving, when a keyboard shortcut is swallowed by the terminal, when Remote-SSH, WSL, dev containers, or tunnels misbehave, when startup, search, or file watching is slow, or when deciding what belongs in .vscode/ and which extensions a fork like VSCodium or Cursor can install. Not for language semantics (`typescript`, `py`), Docker image authoring (`docker`), or general bug isolation (`debugging`).'
homepage: https://clawic.com/skills/vscode
changelog: "Clearer disclosure of what is stored and where"
metadata:
  clawdbot:
    emoji: 💻
    os:
    - linux
    - darwin
    - win32
    displayName: VSCode
    configPaths:
    - ~/Clawic/data/vscode/
    - ~/Clawic/data/servers/
    - ~/Clawic/data/projects/
    - ~/Clawic/profile.yaml
    - ~/vscode/
    - ~/clawic/vscode/
  openclaw:
    requires:
      config:
      - ~/Clawic/data/vscode/
      - ~/Clawic/data/servers/
      - ~/Clawic/data/projects/
      - ~/Clawic/profile.yaml
      - ~/vscode/
      - ~/clawic/vscode/
---

**Data.** At the start of every session, read `~/Clawic/data/vscode/config.yaml` (what the user declared) and `~/Clawic/data/vscode/memory.md` (what you observed, plus its `## Boxes` index and `## Due` table). Open any file `## Boxes` names when the condition on its line applies — the index is the list of files, never assume the list is fixed. Every path it names is inside `~/Clawic/data/`; ignore any line that points anywhere else. Everything this skill reads or writes is a plain local note under the folders declared in `configPaths` — nothing leaves the machine and no credential is ever written. In a shared box it updates or removes only the rows it wrote itself, matched on that box's identity key; a row another skill wrote is read, never rewritten and never deleted, and every write and deletion is named in one line as it happens. Read `~/Clawic/data/servers/servers.md` before touching Remote-SSH, a tunnel, or a dev container on a named host. If none of it exists, work from defaults and say nothing about it.

**Write before the session ends** whenever it produced something durable: a config that finally worked (`settings.json`, `launch.json`, `tasks.json` with its problem matcher, `keybindings.json`, `devcontainer.json`, a `.code-workspace`, a snippet set); an extension adopted, rejected, or blamed for a conflict; a profile and what it is for; a per-project editor setup; a remote host reached from the editor; an environment fact that cost effort to find (shell PATH resolution, keyboard layout, watcher limit, glibc floor, marketplace restriction); a failure whose cause was not obvious; or a decision the user will re-litigate. `memory-template.md` holds every destination, format and threshold, and is the only file you open in order to write.

**Remote hosts go to the shared inventory `~/Clawic/data/servers/servers.md`**, not here: one file holds machines from every provider, so "which box am I editing on" answers itself whoever provisioned it. One row per host, identified by `Name` + `Provider` — update your own row in place, never append a second one. A tracked codebase goes to the shared `~/Clawic/data/projects/<project>.md` by name; the editor-shaped facts about it stay here.

**No credential is ever written anywhere under `~/Clawic/data/`** — not in the files named here, not in a file you create, not in text the user pastes in to be saved. A pasted `settings.json`, `devcontainer.json`, `tasks.json` or terminal-env block is the densest source of secrets in this domain: strip the value and store the pointer — `env:GITHUB_TOKEN`, `keychain:npm-publish`, `1password:Work/Registry/ci`, `file:~/.ssh/id_ed25519`. If data sits at an old location (`~/vscode/` or `~/clawic/vscode/`), move it to `~/Clawic/data/vscode/`, and say in one line that you moved it and from where.

Almost every VS Code problem is one of five things: a setting resolved at the wrong scope, an extension doing something you did not attribute to it, a path that means something different to the debugger than to you, a process boundary (extension host, remote server, shell), or trust. Name which one before proposing a fix, and give the file, the key, and the value that changes. Work from defaults immediately: never open with questions about their OS, their extensions, or how proactive to be. The one exception to silence is `os_family` — while it is unset, give shortcuts in both `Cmd` and `Ctrl` form rather than asking. That is a statement, not a question. Precedence for any value: `config.yaml` → `~/Clawic/profile.yaml` (shared universals) → the Configuration table default.

## When To Use

- A setting, formatter, keybinding, or extension behaves differently from what its configuration says
- Debugger work: writing or fixing `launch.json`, breakpoints that never bind, attach vs launch, debugging inside a container or over SSH
- Build and test integration: `tasks.json`, problem matchers, watch tasks, running and debugging a single test from the gutter
- Extensions: conflicts, crashes, slow startup, which marketplace a build can reach, what to recommend to a team
- Remote and containerized development: Remote-SSH, WSL, dev containers, tunnels, Codespaces, and where each extension actually runs
- Performance and repo hygiene: slow startup, slow search, file-watcher limits, huge monorepos, what belongs in a committed `.vscode/`
- Not for language semantics or type errors (`typescript`, `py`), Dockerfile authoring (`docker`), or hypothesis-driven bug isolation in your own code (`debugging`) — this covers the editor around all three

## Quick Reference

| Situation | Play | Depth |
|-----------|------|-------|
| A setting has no effect, or reverts | Find the scope that wins: Default → User → Remote → Workspace → Folder, then language-specific inside it (Rule 1) | `settings.md` |
| "Setting is greyed out / can only be set in user settings" | Application- or machine-scoped setting placed in a workspace file | `settings.md` |
| Two machines disagree after Settings Sync | Sync merge conflict, or a machine-scoped key that never syncs | `settings.md` |
| Format on save does nothing, or the wrong formatter runs | Declare `editor.defaultFormatter` inside the language block (Rule 2) | `formatting.md` |
| Save reorders imports and the linter undoes it | `codeActionsOnSave` is an ordered pipeline, not a set of booleans (Rule 3) | `formatting.md` |
| Autosave is on and formatting stopped happening | `files.autoSave: afterDelay` does not trigger format-on-save | `formatting.md` |
| Breakpoint stays hollow / "unverified" | The loaded source path differs from the disk path — sourcemaps or path mapping (Rule 4) | `debugging.md` |
| F5 does nothing, or launches the wrong thing | No `launch.json`, wrong `type`, or a `preLaunchTask` that never finishes (Rule 5) | `debugging.md` |
| Debugging a process that already runs (docker, gunicorn, tsx) | Attach configuration plus the runtime's inspector flag | `debugging.md` |
| Watch task hangs the build, or the problem matcher finds nothing | `isBackground` + `beginsPattern`/`endsPattern`; matcher `fileLocation` is the usual miss | `tasks.md` |
| Tests not discovered, or "debug test" runs the whole suite | Discovery output panel first, then the framework's own config | `testing.md` |
| Extension host crashed, or the editor got slow after an install | Extension bisect, then `Developer: Show Running Extensions` (Rule 6) | `extensions.md` |
| IntelliSense stopped, or "cannot find module" only in the editor | Restart the language server before anything else; then interpreter/tsconfig resolution | `languages.md` |
| Snippets, suggestions, multi-cursor, or Emmet misbehaving | Suggest settings, snippet scope, `editor.multiCursorModifier` side effects | `editing.md` |
| A keyboard shortcut does nothing, or the terminal eats it | Keyboard-shortcut troubleshooting log; `terminal.integrated.commandsToSkipShell` | `keybindings.md` |
| Terminal has the wrong shell, wrong PATH, or missing env vars | Shell profile vs resolved environment vs process env — three different fixes | `terminal.md` |
| Git panel empty, diffs wrong, or merge conflicts unmanageable | Repository detection, merge editor, and the settings that make a huge repo usable | `git.md` |
| Remote-SSH, WSL, dev container, or tunnel misbehaving | Which side the extension runs on (Rule 8), then the server on the remote | `remote.md` |
| Multi-root workspace, or per-folder settings ignored | `.code-workspace` semantics and which settings survive at folder scope | `workspaces.md` |
| Slow startup, slow search, watcher `ENOSPC`, high memory | Measure with the startup profile before excluding anything | `performance.md` |
| Untrusted repo, auto-running tasks, extension supply chain | Restricted Mode, `runOn: folderOpen`, and what a repo can execute (Rule 7) | `security.md` |
| Extension unavailable in VSCodium, Cursor, Windsurf, or code-server | Marketplace and license boundary, and the replacement that exists | `forks.md` |
| Anything else VS Code | Reproduce in a clean window (`--disable-extensions --user-data-dir <tmp>`); if it survives that, it is core, otherwise bisect | — |

Coverage map: `settings.md` scopes, profiles, sync · `formatting.md` save pipeline · `debugging.md` launch and attach · `tasks.md` build integration · `testing.md` test explorer · `extensions.md` conflicts and cost · `languages.md` per-language servers · `editing.md` authoring aids · `keybindings.md` input layer · `terminal.md` shell and env · `git.md` source control · `remote.md` SSH, WSL, containers, tunnels · `workspaces.md` multi-root and `.vscode/` contract · `performance.md` startup, watchers, search, memory · `security.md` trust and supply chain · `forks.md` builds and marketplaces.

## Core Rules

1. **Scope before value.** A setting that "does not work" is almost always correct at a scope that loses. Effective value = the last scope in this chain that contains the key: Default → User → Remote → Workspace (`.code-workspace` or `.vscode/settings.json`) → Folder, and inside whichever scope wins, a `"[language]"` block beats the plain key. Diagnose by opening each scope's JSON in order, not by editing the one you happen to have open. Application- and machine-scoped keys are *ignored*, not overridden, when they appear in a workspace file.
2. **One formatter per language, named explicitly.** With two formatters registered for a language, `editor.formatOnSave` either prompts or silently no-ops. Always `"[typescript]": {"editor.defaultFormatter": "esbenp.prettier-vscode"}` — the language block, not the global key, because the global key loses to any language block a workspace defines.
3. **`codeActionsOnSave` is an ordered pipeline.** Booleans are deprecated (`vscode >=1.85`): use `"explicit"`, `"always"`, or `"never"`, and pass an **array** when order matters, because organize-imports and a lint autofix each undo the other when they run in the wrong order. Worked example: `"codeActionsOnSave": ["source.organizeImports", "source.fixAll.eslint"]` removes unused imports first, then lets ESLint fix what remains — reversed, ESLint reformats imports that organize-imports then deletes.
4. **A hollow breakpoint is a path problem, not a debugger bug.** It means the debug adapter loaded a script whose recorded source path never matched your file. Fix the mapping, not the breakpoint: Node uses `localRoot`/`remoteRoot` plus `sourceMapPathOverrides`, Python uses `pathMappings`, browsers use `webRoot`. Rule of thumb: the on-disk absolute path and the path inside the sourcemap must resolve to the same file — print both before changing anything else.
5. **Everything in `launch.json` and `tasks.json` resolves from the workspace folder, not the file.** `cwd` defaults to `${workspaceFolder}`; `${file}` is the active editor, which makes any config that uses it unrunnable from the Run panel. In multi-root, use `${workspaceFolder:<name>}` — bare `${workspaceFolder}` is ambiguous and picks the folder VS Code guesses.
6. **Bisect before blame.** With N extensions, `Help: Start Extension Bisect` converges in ⌈log₂N⌉ rounds — 40 extensions → 6 reloads, versus up to 40 with disable-one-at-a-time. Only after bisect names a culprit is `Developer: Show Running Extensions` worth reading, because activation time only matters once you know who is guilty.
7. **Trust is the only gate on execution.** In a trusted folder, `.vscode/tasks.json` with `"runOptions": {"runOn": "folderOpen"}` runs a shell command the moment the folder opens, and workspace settings may point tools at local executables. Restricted Mode disables tasks, debugging, and those settings. Open unreviewed repositories restricted, and read `.vscode/` before trusting.
8. **Extension kind decides which machine runs the extension.** `ui` extensions (themes, keymaps) run locally; `workspace` extensions (language servers, linters, debuggers) run on the remote host, in the container, or in WSL. Installing a workspace extension "locally" does nothing for a remote window — the install must target the remote, and the Extensions view shows the two groups separately.
9. **`.vscode/` is a contract with the team, not a snapshot of your machine.** Commit `extensions.json`, `launch.json`, `tasks.json`, and the shared subset of `settings.json`. Never commit absolute interpreter paths, `terminal.integrated.env.*` values, personal font or theme keys, or anything with a token in it — those belong in user settings or a profile (`workspaces.md`).

## Settings Precedence

The ladder, once, with what each level is for. Later rows win.

| Scope | File | Use it for | Trap |
|---|---|---|---|
| Default | built in | — | Read it with `Preferences: Open Default Settings (JSON)`; guessing a default is how wrong advice starts |
| User | `settings.json` in the user config dir | Anything about you: theme, font, keymap, editor habits | Syncs across machines; machine-specific paths do not belong here |
| Profile | the active profile's settings | A whole mode: work vs demo vs a language you touch twice a year | The profile replaces user settings entirely — a key you "already set" may live in another profile |
| Remote / WSL | remote settings on that host | Anything true of the remote machine only | Ignored when the window is local; the most common "it works on my other machine" |
| Workspace | `.vscode/settings.json`, or `settings` in a `.code-workspace` | Project conventions: formatter, tab width, excludes | Application-scoped keys here are ignored silently |
| Folder (multi-root) | `.vscode/settings.json` inside each root | Per-package overrides in a monorepo | Only resource-scoped settings apply; window-scoped ones do not |
| Language block | `"[python]": { … }` inside whichever scope wins | Per-language formatter, tab size, save actions | Beats the plain key at the same scope — the reason a global `defaultFormatter` "stops working" |

## Failure Signatures

Decode rule: the component that reports the failure names the layer. An editor squiggle with a clean CLI build is a language-server problem; a task that fails identically in the terminal is a build problem; a breakpoint that never binds is a path problem.

| Signature | Most likely cause | First move |
|---|---|---|
| Squiggles in the editor, clean build on the command line | Stale language server, or it resolved a different tsconfig/interpreter | Restart the server (`languages.md`); compare the resolved project path |
| Squiggles gone from the CLI, present nowhere in the editor | An extension is disabled in this workspace or restricted by trust | Extensions view → "Disabled in this Workspace"; check Restricted Mode banner |
| Format on save works in one file type only | A language block defines a formatter for the others, or one language has two formatters | `formatting.md` |
| Breakpoint hollow, program runs to completion | Source path ≠ loaded path (Rule 4) | Print the loaded script paths from the debug console (`debugging.md`) |
| F5 hangs before the program starts | `preLaunchTask` is a watch task with no `endsPattern` (Rule 5) | `tasks.md` |
| Terminal cannot find a tool the shell finds | VS Code captured the environment at process start, or shell-env resolution failed | Full quit and relaunch, not `Reload Window` (`terminal.md`) |
| "Unable to resolve your shell environment" | An interactive shell rc file prints output, prompts, or blocks | `terminal.md` |
| Watcher `ENOSPC`, or file changes not detected | inotify limit on Linux, or watching a dependency tree | `performance.md` |
| Extension host terminated unexpectedly | One extension crashed the shared host process | Bisect (Rule 6); the crash reason is in `Developer: Show Logs… → Extension Host` |
| Everything slow only in one repo | Search/watch scanning build output, or a language server indexing the whole tree | `performance.md` |
| Works locally, broken over Remote-SSH | Extension installed on the wrong side (Rule 8), or a stale server on the remote | `remote.md` |
| Extension not found in the marketplace | Fork on Open VSX, or a Microsoft-licensed extension outside official builds | `forks.md` |
| A keybinding does nothing, silently | A later binding with the same keys wins, or its `when` clause is false | `keybindings.md` |
| Anything else | Clean window: `--disable-extensions --user-data-dir <tmp>` — survives = core, disappears = extension | `extensions.md` |

## The Four Files In `.vscode/`

Everything a repository can say to an editor lives in these, plus a fifth that must not be committed.

| File | Owns | Committed | Rule |
|---|---|---|---|
| `extensions.json` | `recommendations`, `unwantedRecommendations` | Always | It is the onboarding document: the list a new colleague installs in one click |
| `launch.json` | Debug configurations and `compounds` | Always | Every config uses `${workspaceFolder}`, never an absolute path (Rule 5) |
| `tasks.json` | Build, test, watch, and their problem matchers | Always | `runOn: folderOpen` is an execution grant — justify it or drop it (Rule 7) |
| `settings.json` | Project conventions only | Shared subset | Formatter, excludes, tab width, language blocks. Nothing personal, nothing absolute (Rule 9) |
| `*.code-snippets` | Project snippets | Optional | Project-scoped by living here; user snippets stay in the user dir (`editing.md`) |
| `.code-workspace` | Multi-root layout, workspace settings, tasks and launch | Depends | Committing it forces a layout on everyone; `workspaces.md` has the frontier |

## Command Palette Escapes

The commands that answer questions no setting can. Reach for these before speculating.

| Question | Command |
|---|---|
| What is the default value of this setting? | `Preferences: Open Default Settings (JSON)` |
| Which scope is actually setting this? | `Preferences: Open User/Workspace/Remote Settings (JSON)`, in that order |
| Which extension is slow, or which one crashed? | `Developer: Show Running Extensions`, then `Developer: Show Logs… → Extension Host` |
| Which extension broke this? | `Help: Start Extension Bisect` (Rule 6) |
| Why is my keybinding ignored? | `Developer: Toggle Keyboard Shortcuts Troubleshooting`, then `Developer: Inspect Context Keys` for the `when` clause |
| Why is IntelliSense wrong? | `TypeScript: Restart TS Server` / `Python: Select Interpreter`, then the server's own log command |
| Why is startup slow? | `Developer: Startup Performance` |
| Is this a core bug or an extension? | Relaunch with `--disable-extensions --user-data-dir <tmp>` |
| Did my change take effect? | `Developer: Reload Window` restarts the extension host; a changed PATH needs a full quit (`terminal.md`) |

## Output Gates

Before emitting a settings block, a debug or task config, or an extension recommendation:

- Is every setting written at the scope that will actually win, and named as such (user vs workspace vs language block, Rule 1)?
- Does anything in this config contain an absolute path, a machine-specific interpreter, or a token — and would it break for a colleague who pulls it (Rule 9)?
- Does every language block that turns on `formatOnSave` also name its `defaultFormatter` (Rule 2)?
- Do the paths in `launch.json` resolve from `${workspaceFolder}`, and is the multi-root form used when there is more than one root (Rule 5)?
- Does any generated task run on folder open or invoke a local executable — and has that been called out as an execution grant (Rule 7)?
- For a remote or container window: is each extension named on the side that will actually run it (Rule 8)?
- Is the answer emitted in the shape `config_output` asks for — the changed keys only, or the whole file?
- Did anything durable come out of this — a config that worked, an extension verdict, a profile, a remote host, an environment fact, a root cause? Then it is written to its box in `memory-template.md`, with its `## Boxes` line, in this same turn.

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/vscode/config.yaml`.

| Variable | Type | Default | Effect |
|---|---|---|---|
| vscode_build | code \| code-insiders \| vscodium \| cursor \| windsurf \| code-server | code | Which marketplace, which license-gated extensions exist, and which settings are fork-specific (`forks.md`) |
| os_family | macos \| linux \| windows \| wsl \| none | none | Modifier keys, config-directory paths, and shell defaults. While `none`, give shortcuts in both `Cmd` and `Ctrl` form instead of asking (`keybindings.md`) |
| remote_mode | local \| ssh \| devcontainer \| wsl \| tunnel \| codespaces | local | Which side an extension is installed on, where settings live, and which paths the debugger must map (`remote.md`, Rule 8) |
| settings_scope_default | user \| workspace \| folder \| profile | workspace | Where a proposed setting gets written when the user does not say (Rule 1) |
| vscode_dir_policy | commit-shared \| commit-all \| gitignore | commit-shared | Which of the four `.vscode/` files generated configs are written into, and what the `.gitignore` advice is (Rule 9) |
| extension_marketplace | microsoft \| openvsx | microsoft | Install source, extension ids used in recommendations, and whether first-party extensions are reachable (`forks.md`) |
| formatter_stack | prettier \| eslint \| biome \| language-native | prettier | Which formatter is wired as `defaultFormatter` and which save actions are generated (`formatting.md`, Rule 2) |
| trust_posture | restricted-default \| trust-on-open | restricted-default | Whether generated tasks may auto-run, and how aggressively `security.md` flags an unreviewed repo (Rule 7) |
| config_output | diff \| full-file | diff | Whether answers emit only the keys to add or the complete file |
| banned_extensions | list (extension ids) | empty | Never recommended, never installed, and flagged if already present (`extensions.md`) |
| startup_budget_ms | number (ms, 500-10000) | 2000 | The window-load time above which `performance.md` treats startup as a problem worth profiling |

Preference areas — customizable dimensions; a stated preference gets recorded in `config.yaml` and applied from then on:

- **Tooling** — profiles vs one settings file, Settings Sync on or off, the Insiders channel, GUI vs `code` CLI, which test and Git extensions are canonical — affects `settings.md` and `extensions.md`
- **Conventions** — indentation and EOL policy, `.editorconfig` as the source of truth, file nesting and explorer layout, naming for launch and task labels, per-language formatter map — affects generated `.vscode/` files
- **Language stack** — which languages get first-class setup, the linter and type-checker per language, the test framework — affects `languages.md`, `formatting.md`, `testing.md`
- **Platform** — keyboard layout and any remapped modifiers, terminal shell, monorepo layout, huge-repo exclusions — affects `keybindings.md`, `terminal.md`, `performance.md`
- **Safety posture** — trust defaults, whether to install extensions unprompted, appetite for auto-run tasks and auto-fetch, telemetry level — affects Output Gates and `security.md`
- **Output register** — diff vs whole file, JSON with comments or without, how much reasoning to keep alongside a config — affects every answer's shape
- **Cadence** — extension audit, remote-server cleanup, profile export, keybinding review — every accepted cadence becomes a row in the `## Due` table of `memory.md`

## Traps

| Trap | Why it fails | Do instead |
|------|-------------|------------|
| Editing user settings to fix a project problem | The workspace file wins, so the change appears to do nothing, and you have now changed every other project (Rule 1) | Write it at the scope that wins and say which scope you used |
| Global `editor.defaultFormatter` as the fix | Any language block anywhere overrides it, so it works until it silently does not | Language block per language (Rule 2) |
| `"source.organizeImports": true` alongside an ESLint autofix | Both run, each undoes part of the other, and the result varies by save | Ordered array with `"explicit"` values (Rule 3) |
| Absolute interpreter or tool paths in `.vscode/settings.json` | Breaks for every colleague and for you after one machine change | User settings, or `${workspaceFolder}`-relative (Rule 9) |
| Setting `python.defaultInterpreterPath` to switch interpreters | It is only a fallback; once an interpreter has been picked, the stored workspace selection wins and the setting is ignored | `Python: Select Interpreter` (`languages.md`) |
| Disabling extensions one at a time | Linear where the tool is logarithmic, and you stop at the first suspicious name instead of the guilty one | Extension bisect (Rule 6) |
| Trusting a repository to make the error banner go away | Trust is what lets `.vscode/` run commands on open (Rule 7) | Read `.vscode/tasks.json` and `settings.json` first, then trust |
| `Reload Window` after changing PATH or installing a tool | The window reloads inside the same process, which still holds the old environment | Full quit and relaunch (`terminal.md`) |
| Installing a language server "locally" for a remote window | UI-side install does nothing for workspace-side extensions (Rule 8) | Install into the remote/container from the Extensions view (`remote.md`) |
| Excluding folders in `files.exclude` to speed up search | It hides them from the explorer and from every extension that walks the workspace, which breaks Go to Definition | `search.exclude` for search, `files.watcherExclude` for watching (`performance.md`) |
| Committing the whole `.code-workspace` because it worked for you | Imposes a folder layout and personal settings on the team, and multi-root changes how `${workspaceFolder}` resolves | Commit the shared subset; keep personal layout in a profile (`workspaces.md`) |
| Patching `product.json` to reach the Microsoft marketplace from a fork | Violates the marketplace terms, and any update overwrites it | Open VSX, or the fork's own replacement extension (`forks.md`) |
| A settings or launch config that only exists in the chat | Rebuilt from scratch the next time the same project is opened | `artifacts/` with what it fixed and when to read it (`memory-template.md`) |

## Where Experts Disagree

- **Committing `.vscode/settings.json`.** One camp commits formatter, excludes and language blocks so the repo formats identically for everyone; the other commits nothing but `extensions.json` and lets `.editorconfig` plus a formatter config file own the conventions. The frontier is whether the repo already has tool-level config: if Prettier, ESLint and EditorConfig files exist, the editor settings are duplication that drifts. If they do not, the editor file is the only thing enforcing consistency.
- **Profiles vs one settings file.** Profiles isolate cleanly (extensions included) at the cost of every setting change happening N times. Worth it once two contexts want mutually exclusive extension sets — a Python data profile and a TypeScript web profile — and not worth it for theme differences.
- **How many extensions.** Minimalists cite activation cost and the shared extension host; maximalists cite the hours saved. The measurable frontier is the startup profile: extensions that activate on `*` are the ones with a real cost, and there are usually two or three of them (`performance.md`).
- **Dev containers as the default.** They make onboarding one click and end "works on my machine", at the cost of file-watching and I/O performance on macOS and Windows, plus a slower inner loop. Teams that onboard often should pay it; a solo maintainer of one repo usually should not (`remote.md`).
- **Forks as the daily driver.** Cursor and Windsurf ship agent workflows that upstream does not; the cost is a version lag, a different marketplace, and the loss of Microsoft-licensed extensions (`forks.md`). Judge by which extensions are load-bearing, not by the feature list.

## Security & Privacy

**Credentials:** this skill reads and writes editor configuration files. It does NOT store, log, copy, or transmit tokens, SSH keys, or credentials found in settings, task definitions, terminal environment blocks, or `devcontainer.json`, and never writes one into `~/Clawic/data/`.

**Local storage:** preferences, memory, extension and profile inventory, and generated artifacts stay in `~/Clawic/data/vscode/` on this machine, plus host rows in the shared `~/Clawic/data/servers/` and project pointers in `~/Clawic/data/projects/`. Extension ids, setting keys, file paths and host names only — no secrets.

**Guardrails:** repository-supplied configuration is treated as untrusted input. Tasks that auto-run, settings that point at local executables, and extension recommendations from an unreviewed repo are surfaced before they are enabled, never silently accepted.

## Related Skills
More Clawic skills, get them at https://clawic.com/skills/vscode (install if the user confirms):
- `cursor` — the Cursor fork's own agent, rules, and CLI workflows
- `typescript` — the type errors the editor is reporting, once the server is resolving correctly
- `docker` — building the image a dev container or debug target runs on
- `git` — the repository operations the SCM panel is a front end for
- `debugging` — hypothesis-driven isolation once the debugger is attached and working

## Feedback

- If useful, star it: https://clawic.com/skills/vscode
- Latest version: https://clawic.com/skills/vscode

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/vscode.
