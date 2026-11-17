# Working File Templates — VS Code

Read this file only when WRITING. `config.yaml` is what the user **declared**; `memory.md` and everything it indexes is what you **observed** or produced. An observation never overwrites a declaration.

## Where each thing goes

| Data | Home | How it grows |
|---|---|---|
| Declared preferences — Configuration table keys and preference areas alike | `~/Clawic/data/vscode/config.yaml` | Key by key, read-modify-write |
| Environment facts, extensions, profiles, per-project setup, pain points, due dates, box index | `~/Clawic/data/vscode/memory.md` | Rewritten in place; stays small |
| Machines reached from the editor over SSH, tunnel, or a remote container host | `~/Clawic/data/servers/servers.md` (**shared**) | One row per host, every provider in one inventory |
| The codebase itself — goal, status, decisions | `~/Clawic/data/projects/<project>.md` (**shared**) | One file per project; referenced from here by name only |
| Extensions in use, and the verdict on each | `## Extensions` in `memory.md`; `~/Clawic/data/vscode/extensions.md` once it outgrows the section | One row per extension |
| Profiles and what each is for | `## Profiles` in `memory.md`; `~/Clawic/data/vscode/profiles.md` once it outgrows the section | One row per profile |
| Editor-shaped facts about a repo — interpreter, formatter, excludes, debug entry point | `## Projects` in `memory.md`; `~/Clawic/data/vscode/projects.md` once it outgrows the section | One row per repo |
| Things you produced that get re-read whole — a `settings.json`, `launch.json`, `tasks.json` with its problem matcher, `keybindings.json`, `devcontainer.json`, `.code-workspace`, a snippet set, a runbook, a decision | `~/Clawic/data/vscode/artifacts/<kebab-name>.md` | Born as its own file, from the first one |
| **Anything durable this table does not name** | `~/Clawic/data/vscode/<plural-noun>.md`, or `artifacts/<kebab-name>.md` if it is a long text read whole | Name the file after what it holds, never after when it was made; add its `## Boxes` line in the same turn |
| Credentials of any kind | Nowhere under `~/Clawic/data/` | Pointer only — see Secrets |

Deciding where something unnamed goes, in this order: (1) would another skill want to read it — a host, a person, a project, a domain? Then it belongs in the shared box, not here. (2) Is it a text read whole when its subject comes up — a config file, a procedure, a decision with its reasoning? Then `artifacts/`, its own file from the first one. (3) Is it one more row of something that accumulates? Then a section of `memory.md` until the split threshold.

## When to write

No permission needed; every write is announced in one line that names the file. Writes and deletions stay inside the paths declared in this skill's `configPaths`. A deletion is named in that same line, and in a shared box only rows this skill itself wrote are ever updated or removed.

| It happened | Write |
|---|---|
| A `settings.json`, `launch.json`, `tasks.json`, `keybindings.json`, `devcontainer.json`, `.code-workspace` or snippet set finally worked | `artifacts/`, with what it fixed |
| A problem matcher was derived for a non-standard tool | `artifacts/` — the most expensive thing to re-derive in this domain |
| An extension was adopted, rejected, blamed for a conflict, or banned | `## Extensions` |
| A profile was created, or its purpose changed | `## Profiles` |
| A repo's editor setup was established or fixed — interpreter, formatter, excludes, debug entry point | `## Projects` |
| A machine was reached over SSH, a tunnel, or as a container host | Its row in `servers.md` (**shared**) |
| An environment fact cost effort to find — shell PATH resolution, keyboard layout, watcher limit, glibc floor, a marketplace restriction, a corporate proxy or CA | `## Environment` |
| A failure's cause was not obvious, or the same failure appeared twice | `## Pain Points`; the second occurrence earns a runbook in `artifacts/` |
| A decision was made and will be re-litigated — which fork, `.vscode/` commit policy, profiles vs one file, dev container vs local | `artifacts/`, with what was rejected and why |
| An extension audit, remote-server cleanup, profile export or keybinding review was scheduled or run | `## Due` |
| The user declared a preference | Its key in `config.yaml` |

## Start flat, split only when it hurts

Everything except artifacts and the shared boxes begins inside `memory.md`. Splitting is a procedure, not a suggestion:

1. Before appending to a section, count its entries.
2. If the append would take it past **~15 entries or ~40 lines of real content** — scaffolding, headings and comments do not count — then, in the same turn: create the new file in `~/Clawic/data/vscode/`, move the whole section into it, **delete the section from `memory.md`**, add its line to `## Boxes`, and append the new entry to the new file.
3. Keep the headings identical on both sides of the move, so the split is a copy-paste and never a rewrite.
4. Never leave a copy behind. If the same data ever appears in both places, the extracted file wins and the `memory.md` copy is deleted.

Artifacts are the exception: a config file, a runbook or a decision is born as its own file whatever its size, because it is read whole and only when its subject comes up.

## Secrets

Nothing under `~/Clawic/data/` ever holds a secret value — not the files named here, not files you create, not text the user pastes in and asks you to keep. A pasted `settings.json`, `tasks.json`, `devcontainer.json`, `launch.json` `env` block or terminal environment block is the densest source of secrets in this domain: strip each value **before** writing and leave its pointer in place, in this shape: `<kind>:<locator>`.

`env:GITHUB_TOKEN` · `keychain:npm-publish` · `1password:Work/Registry/ci` · `bitwarden:Dev/Sentry` · `vault:secret/dev/api` · `profile:work` · `file:~/.ssh/id_ed25519` · `file:~/.npmrc`

In a text, the pointer goes where the value was: `"GITHUB_TOKEN": "<env:GITHUB_TOKEN>"`. Say in one line that you did it.

In this domain — **not secrets, keep them**: extension ids and versions, setting keys, task and launch labels, problem-matcher regexes, file and folder paths, workspace and profile names, host names and SSH aliases, port numbers, interpreter and toolchain paths, marketplace names, git remote URLs without credentials, keyboard shortcuts, glibc and editor version numbers.

**Secrets, strip them**: personal access tokens and API keys in `terminal.integrated.env.*`, `tasks.json` `options.env`, `launch.json` `env`, or `devcontainer.json` `containerEnv`/`remoteEnv`; registry tokens in `.npmrc`/`.pypirc` the user pastes; `settings.json` keys ending in `apiKey`, `token`, `secret`, or `password`; SSH private keys and passphrases; git remote URLs that embed a password; license keys; proxy URLs carrying credentials.

**Contents:** [config.yaml](#configyaml) · [memory.md](#memorymd) · [shared servers inventory](#shared-servers-inventory) · [shared projects box](#shared-projects-box) · [artifacts/](#artifacts) · [split-out files](#split-out-files)

## config.yaml

Keys come from the Configuration table in `SKILL.md`, plus free-form keys nested under a preference area. Write a key only when the user states the preference.

**Writing is read-modify-write**: load the existing file, set or replace only the key just declared, keep every other key byte for byte. Never emit a `config.yaml` from this template — the template shows shape, not content. Create `~/Clawic/data/vscode/` if it does not exist.

```yaml
vscode_build: code
os_family: macos
remote_mode: devcontainer
settings_scope_default: workspace
vscode_dir_policy: commit-shared
extension_marketplace: microsoft
formatter_stack: prettier
trust_posture: restricted-default
config_output: diff
banned_extensions: [hookyqr.beautify]
startup_budget_ms: 1500

# Preference areas — free-form keys added as the user reveals them.
# A preference the user states is a declaration and belongs here, never in memory.md.
tooling:
  profiles: true
  settings_sync: true
conventions:
  editorconfig_is_truth: true
  indent: "2 spaces, LF"
language_stack:
  python: {linter: ruff, tests: pytest}
  typescript: {linter: eslint, tests: vitest}
platform:
  keyboard_layout: "US, right alt remapped"
  shell: zsh
safety_posture:
  install_extensions_unprompted: false
cadence:
  extension_audit: quarter
  remote_server_cleanup: month
```

If you find a preference recorded in `memory.md`, move it here and note the move.

## memory.md

Write only the sections you have content for — a heading with nothing under it is noise, and it inflates the line count that decides a split. Never copy these hints into the user's file. `## Boxes` is the one section that is never dropped when `memory.md` is rewritten: deleting a line there orphans a file forever. This is what a populated file looks like:

```markdown
# VS Code Memory

## Status
status: ongoing
last: 2026-07-26

## Boxes
- Extensions and verdicts (22) → `extensions.md`; read before recommending or installing anything
- Working launch.json for the api monorepo → `artifacts/launch-api-monorepo.md`; read before touching any debug config in that repo
- Problem matcher for the in-house compiler → `artifacts/matcher-acme-cc.md`; read whenever a task's errors do not appear in the Problems panel
- Dev container for the data repo → `artifacts/devcontainer-data.md`; read before changing the container or its extensions
- Decision: VSCodium as daily driver → `artifacts/decision-vscodium.md`; read whenever an extension turns out to be unavailable

## Due
| What | Every | Last run | Next due |
|------|-------|----------|----------|
| Extension audit (activation cost + unused) | quarter | 2026-05-02 | 2026-08-02 |
| Remote `~/.vscode-server` cleanup on build-1 | month | 2026-07-04 | 2026-08-04 |
| Profile export backup | quarter | 2026-04-11 | 2026-07-11 |
| Keybinding conflict review after major updates | quarter | 2026-06-20 | 2026-09-20 |

## Environment
macOS 15, arm64, VS Code stable, zsh with a `.zshrc` that prints a banner — shell-env resolution failed until it was guarded by `[[ -o interactive ]]`.
Corporate proxy needs `http.proxyStrictSSL: false` plus the CA in the system keychain; extension installs fail without it.
Linux workstation: `fs.inotify.max_user_watches` raised to 524288; below that the monorepo threw ENOSPC on open.
Right Alt remapped at the OS level — `alt+click` multi-cursor unavailable, so `editor.multiCursorModifier` is `ctrlCmd`.
Remote `build-1` runs Debian 12; anything older than glibc 2.28 cannot host the server (`vscode >=1.86`).

## Extensions
| Extension | Id | Verdict | Why | Scope |
|---|---|---|---|---|
| Prettier | esbenp.prettier-vscode | keep | default formatter for web languages | all profiles |
| ESLint | dbaeumer.vscode-eslint | keep | fixAll after organizeImports | web profile |
| Beautify | hookyqr.beautify | banned | second formatter for the same languages, silent no-op on save | — |
| Python | ms-python.python | keep | interpreter selection, test discovery | data profile, workspace side |

## Profiles
| Profile | For | Extension set | Notes |
|---|---|---|---|
| web | TypeScript/React work | prettier, eslint, vitest | default profile |
| data | notebooks and pytest | python, jupyter, ruff | separate because Pylance indexing slowed the web repos |

## Projects
| Repo | Interpreter / toolchain | Formatter | Debug entry | Excludes | Notes |
|---|---|---|---|---|---|
| acme-api | .venv (poetry) | ruff | attach :5678 in container | `**/.venv`, `**/dist` | pathMappings needed, see artifact |
| acme-web | node 22 via fnm | prettier | `pnpm dev` + Chrome attach | `**/node_modules`, `**/.next` | multi-root with acme-shared |

## Pain Points
2026-04: two days lost to a hollow breakpoint — the container mounted the repo at `/app`, `pathMappings` was missing. Now in the launch artifact.
2026-06: extension host crashed on every save; bisect found a linter extension shipping a broken binary for arm64.

## How They Work
Keyboard-first, no mouse. Wants the JSON keys, not the Settings UI path. Will not install an extension without knowing what activates it.

---
*Updated: 2026-07-26*
```

Rules that keep this readable next month:

- **`## Boxes`**: one line per file that exists — `<what> (<volume>) → <file>; read when <condition>`. Written in the same turn the file is created. Never delete a line without deleting the file it points to. A box with no index line does not exist.
- **`## Due`**: check it against today's date at the start of a session and state any overdue item in one line — a statement, not a question. Every recurring thing this skill schedules belongs here, and the cadences come from `cadence` in `config.yaml` when the user has declared them.
- **`## Environment`**: facts about the machine, the shell, the keyboard and the network that changed a decision, one line each. This is the section that stops the same PATH, watcher-limit or proxy problem from being rediscovered every few months. Anything about a *host as a machine* (provider, specs, cost, access) belongs in the shared inventory instead; what stays here is editor-shaped.
- **`## Extensions`**: `Verdict` is `keep`, `trial`, `dropped`, or `banned`, and `Why` is one clause — the reason is what stops the same extension being reinstalled next quarter. A `banned` row mirrors `banned_extensions` in `config.yaml`; the row carries the reason, the config key carries the enforcement.
- **`## Profiles`**: a profile with no stated purpose gets merged back within a month. Record what forced the split, not just the name.
- **`## Projects`**: editor-shaped facts only. The repo as a *project* — goal, status, decisions, milestones — belongs in the shared `~/Clawic/data/projects/<project>.md` and is referenced here by name. Never duplicate the project record.
- **`## Pain Points`**: date, symptom, actual cause, what changed. A second occurrence of the same symptom stops being a line here and becomes `artifacts/runbook-<symptom>.md`.
- These headings are exactly the ones `extensions.md`, `profiles.md` and `projects.md` get when their sections outgrow this file, so each split stays a copy-paste.

| Status | Meaning |
|-------|---------|
| `ongoing` | Still learning their setup |
| `complete` | Know their build, profiles, repos and habits well |

## Shared servers inventory

Lives at `~/Clawic/data/servers/servers.md` and is shared with every other infrastructure skill — the user may not have any of them installed, so the format travels with this skill. Write a row when the editor connects to a machine over SSH, a tunnel, or as a dev-container host.

```markdown
# Servers

| Name | Provider | Account / Project | Region | Type | Role | Monthly | Access reference |
|------|----------|-------------------|--------|------|------|---------|------------------|
| build-1 | hetzner | acme | fsn1 | CPX31 | remote-ssh dev host | 15 EUR | file:~/.ssh/id_ed25519 |
```

- **Identity is `Name` + `Provider`.** Read the file before adding. If that pair is already there, update the row in place — it is yours. Never touch a row whose `Provider` you did not write.
- **Retirement is part of the inventory.** When a host is decommissioned or the editor stops using it, delete the row you own and note the date in `## Environment` of `memory.md`. An inventory that only grows stops being an inventory.
- **Amounts carry their currency in the value** (`15 EUR`), because rows from other providers are in other currencies and someone will add the column up. An estimate carries the date it was estimated.
- **`Role` is what the machine does**, and for this skill it says `remote-ssh dev host`, `tunnel host` or `devcontainer host` plus what runs on it.
- **Scale cut**: one row per host while there are ≤15. Past that, one file per host at `~/Clawic/data/servers/<name>.md` with the same fields, and `servers.md` becomes the index (`Name | Provider | Role | → file`). If you arrive and the folder already looks like that, follow it — do not start a parallel `servers.md`.
- **Foreign columns win.** If `servers.md` already exists with a different column set, match its columns and add anything missing as a trailing note. Never rewrite its header.
- Access reference is a pointer only. Never a key, token, or password.

## Shared projects box

Lives at `~/Clawic/data/projects/<project>.md`, one file per project from the first one, shared with every skill that touches the same work. This skill writes the editor-relevant line and nothing else: the repo's location, the debug entry point, and any editor decision the team depends on.

- **Identity is the file name** — the project slug in kebab case. Read the folder before creating a file; if the project already has one, append to it, never start a second file under a different spelling.
- Retirement is `status: done | cancelled — <date>` inside the file; the file is never deleted, because it is the record of what was delivered. Past ~20 closed projects, move them to `projects/archive/<project>.md` without renaming.
- If a project also names a person — a client, a maintainer — the person goes in `~/Clawic/data/contacts/contacts.md` and is referenced here by name only. Never duplicate the person record inside a VS Code file.
- Everything editor-shaped that does not belong to the project as a whole (interpreter path, excludes, formatter) stays in `## Projects` in `memory.md`.

## artifacts/

One file per thing, at `~/Clawic/data/vscode/artifacts/<kebab-name>.md`, created the first time it exists. Canonical types here: **a config file that finally worked**, **a problem matcher**, **a runbook for a failure that recurred**, **a decision with what was rejected**. Every artifact opens with when to read it, and gets its `## Boxes` line in the same turn. Every secret inside is already a pointer.

```markdown
# launch.json — acme-api in its dev container
*Read before touching any debug config in acme-api. Working as of 2026-07-26.*

Why it is shaped this way: the container mounts the repo at /app, so pathMappings maps
${workspaceFolder} to /app or every breakpoint stays hollow; justMyCode is off because the
bug was inside a dependency; the attach port is published in the compose file, not the image.

...the JSON, with every secret replaced by its pointer...
```

```markdown
# Problem matcher — acme-cc compiler
*Read whenever an acme-cc task's errors do not appear in the Problems panel. 2026-07-26.*

Regex, capture-group order, and `fileLocation: ["relative", "${workspaceFolder}"]` because the
compiler prints paths relative to the build directory, not the workspace root.
```

```markdown
# Decision — VSCodium as the daily driver
*Read whenever an extension turns out to be unavailable. 2026-07-26.*

Decision: ...one sentence...
Rejected: official build — telemetry policy.
Cost: no Pylance, no Remote-SSH from the Microsoft pack; replacements and their gaps listed here.
Revisit when: a load-bearing extension has no Open VSX equivalent.
```

If the user tracks this work as a project, the one-line decision summary also belongs in the shared `~/Clawic/data/projects/<project>.md`, with the full artifact staying here and referenced by name.

## Split-out files

Created only by the split procedure above, never on day one. Each keeps the exact headings it had inside `memory.md`.

`extensions.md` — `## Extensions`, plus `## Activation Cost` (extension, activation event, measured startup contribution, date measured) once an audit has run. The audit log is the reason this file exists: without it the same extension gets reinstalled, re-blamed and re-measured every year.

`profiles.md` — `## Profiles`, plus `## Export Log` (profile, date exported, where the export lives as a pointer). A profile that has never been exported is one disk failure from being rebuilt by hand.

`projects.md` — `## Projects`, one `## <repo>` heading per repo once the rows stop fitting on one line each. This is the file that answers "how is this repo set up in the editor" without opening the repo.
