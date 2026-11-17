<p align="center"><b>Language</b>: English · <a href="./README.zh-CN.md">中文</a></p>

<p align="center">
  <img src="assets/banner.png" alt="yotta-workflow banner" width="100%" />
</p>

<h1 align="center">yotta-workflow · 元序 (Yuanxu)</h1>

<p align="center">A universal workflow standard for all AI agents: <b>the process is set globally, state follows the project root; read the state on start, always leave a handoff anchor on finish</b>. Lets any AI conversation resume painlessly and avoids amnesia from overlong single sessions.</p>
<p align="center">State directory is unified as <code>.workflow</code> — all agent sessions of the same project read and write the same state (one source of truth); on start, read the state to restore context; while working, actively persist logs / tasks / decisions; on finish, generate a self-contained handoff anchor.</p>
<p align="center">Pure Markdown text, zero dependencies, no injection, no platform lock; install once, works across 78+ agents such as Claude Code / Codex / Cursor / OpenCode.</p>

<p align="center">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-blue" /></a>
  <a href="https://agentskills.io/"><img alt="Standard: agentskills.io" src="https://img.shields.io/badge/standard-agentskills.io-orange" /></a>
  <a href="https://www.npmjs.com/package/@yottameta/yotta-workflow"><img alt="npm package" src="https://img.shields.io/npm/v/@yottameta/yotta-workflow" /></a>
  <a href="https://github.com/YottaMeta/yotta-workflow"><img alt="GitHub stars" src="https://img.shields.io/github/stars/YottaMeta/yotta-workflow" /></a>
  <a href="https://github.com/YottaMeta/yotta-workflow/commits/main"><img alt="last commit" src="https://img.shields.io/github/last-commit/YottaMeta/yotta-workflow" /></a>
  <a href="https://github.com/YottaMeta/yotta-workflow"><img alt="PRs welcome" src="https://img.shields.io/badge/PRs-welcome-brightgreen" /></a>
</p>

## What it is

AI sessions are inherently stateless: each conversation is independent, and the longer a chat grows the more memory it loses; switching sessions or agents means the previous context is gone. The built-in memory solutions of each platform usually serve a single agent, so different agents each keep their own records and produce multiple "sources of truth".

yotta-workflow distills "cross-session collaboration" into an agent-agnostic protocol that answers three questions:

- **Where is the state stored and in what format?** — determined by rules, not left to each agent's free choice.
- **When to read, when to write?** — read on start, write actively while working, always leave an anchor on finish.
- **How to hand off?** — a fixed template generates a self-contained handoff anchor; the next session resumes painlessly from just that anchor.

It depends on no specific agent or platform: the state is just Markdown files under the project root, readable and writable by any agent or tool.

## Core value

- **One source of truth** — all agent sessions of the same project read and write the same `.workflow\` state directory, instead of each building its own and keeping separate records.
- **State follows the project root** — `.workflow` belongs to the project root, not to a source checkout or a workspace container; an existing `.workflow` is always reused in place and never auto-migrated.
- **Proactive anti-amnesia** — every completed action is written to logs / tasks / decisions while working, not relied on in-conversation memory (context gets auto-compressed).
- **Self-contained handoff** — on finish, generate a fixed-format handoff anchor; the next session restores full context from the anchor plus state files.
- **Compatible with existing mechanisms** — if the project already has its own handoff / state mechanism, keep it, only satisfying two mandatory points: read state on start, update state and leave an anchor on finish.

## Core advantages

| Advantage | Description |
|---|---|
| **Cross-agent unified** | follows the Agent Skills open standard (agentskills.io); install once, 78+ agents share one state protocol |
| **One source of truth** | unified `.workflow` state directory; any agent of the same project reads/writes the same state, eliminating multiple sources of truth |
| **Automated path detection** | explicit root → nearest existing `.workflow` → project root / source directory / workspace classification; never hard-code a path |
| **Proactive persistence** | immediately write logs / tasks / decisions while working, so context compression never loses key state |
| **Self-contained handoff anchor** | fixed template + enforced validation (content must match state files); next session resumes painlessly |
| **Lightweight zero-dependency** | plain Markdown files, no daemon / database / injection; readable and writable on any platform |
| **Gradual adoption** | projects with an existing state mechanism keep it, only satisfying the two mandatory points; low migration cost |
| **Ecosystem distribution** | GitHub + npm dual-source sync release; four install methods (npx / git clone / Download ZIP / install.sh) covering 17+ agent directories |

## Protocol details

### Path model and state file location rule

**First distinguish three concepts: the project root owns the whole project state and is the only anchor for `.workflow`; the source directory is normally a code subdirectory under the project root; a workspace root is only a container for multiple project roots.**

| Directory | Definition | Where `.workflow` goes |
|---|---|---|
| **Project root** | Parent directory that owns the whole project state and normally contains both `.workflow` and the source directory | `<project root>\.workflow\` |
| **Source directory** | Code directory under the project root; it may have its own `.git` | Not there, unless the user explicitly says it is also the project root |
| **Workspace root** | Container holding multiple project roots; it owns no project state | Not there; choose the relevant project root first |

```text
<project root>\
├── .workflow\         # state; directly under the project root
└── <source dir>\      # source directory; under the project root
```

**Resolution order (two signals only):**

1. The user explicitly specifies a project root → use it.
2. Walk upward from the cwd and use the nearest existing `.workflow\STATE.md`; its parent is the project root. Keep it in place; **never auto-migrate it**.
3. If neither signal exists, stop and ask: `What is this task's project root directory?` Do not infer it from `.git`, `package.json`, `src`, `README`, the cwd, or directory structure.

> This skill defines only the standard layout and state location. How a real project names or layers its source directories is left to the user to adapt.

### Project state system (five file types)

| File | Content |
|---|---|
| `STATE.md` | current progress / recent decisions / open issues / next steps (key for the next session to resume) |
| `TASKS.md` | task list (`- [ ]` todo / `- [x]` done / `- [~]` in progress) |
| `DECISIONS.md` | decision log (each with background / decision / rationale / alternatives) |
| `ROADMAP.md` | long-term goals + next-step plan |
| `logs\YYYY-MM-DD.md` | one daily log (what was done / produced / pitfalls hit) |

### Three-phase protocol

**On start (every session)** — locate the state directory by the rule → if present, fully read STATE / TASKS / ROADMAP / DECISIONS and recent logs to restore context; if absent, initialize all files and confirm with the user; a session delivers one milestone.

**While working (write actively, don't rely on memory)** — append to the day's log after each completed action; update TASKS status in real time; write directional decisions into DECISIONS on the spot; keep STATE "current progress" up to date; key info must be persisted, not left only in the conversation.

**On finish (every session)** — update STATE / TASKS / ROADMAP → append the day's log → generate a handoff anchor by template and output it verbatim for the user to copy.

### Handoff anchor format

On finish, output by the fixed template; the anchor must be self-contained and its content must match the state files (never invented). The full template is in SKILL.md "五、交接话术模板". Structure points:

| Section | Content |
|---|---|
| header | project name (one-line positioning), project root absolute path, last session end date |
| progress | current progress, completed (consistent with STATE.md) |
| next | next steps (by priority), key decisions, open issues / notes |
| footer | on start please read: `.workflow\STATE.md`, TASKS.md, ROADMAP.md |

## Usage examples

**On start** — read state, then talk about the task:

```text
Please read .workflow\STATE.md, TASKS.md, ROADMAP.md first to restore the project context.
```

**While working** — after completing one thing, persist it immediately:

```text
Completed "xxx", append to logs\2026-08-25.md; tick the TASKS.md item; update STATE.md current progress.
```

**On finish** — generate a handoff anchor by template:

```text
Handoff anchor for your next session

【会话交接锚点】
项目：<project name>（<one-line positioning>）
路径：<project root absolute path>
上次会话结束于：<date>
当前进度：…
下一步（按优先级）：…
开工请先读取：.workflow\STATE.md、TASKS.md、ROADMAP.md
```

## When to trigger

Use this skill in these scenarios:

- When starting or ending a work session, or resuming a project.
- When the project state changes (completing a task / recording a decision / updating the roadmap).
- When you need to leave a self-contained handoff anchor for the next session, or read an existing one.

It is not needed for one-off read-only questions (e.g. "what does this function mean").

## Installation

Pick any of the four methods below; the order is the recommended priority. Skill files always come from **npm** (GitHub can be slow without a proxy; npm supports mirrors).

### Method 1: npm one-liner (recommended)

```text
# Optional China mirror: npm config set registry https://registry.npmmirror.com
npx -y @yottameta/yotta-workflow@0.4.5 --agent <agent-name>      # install to the agent's default user-level skills dir
npx -y @yottameta/yotta-workflow@0.4.5 --dir <your-skills-dir>   # point to the skills dir itself (e.g. ~/.codex/skills)
```

- `--agent <name>` installs to that agent's default user-level directory; `--list` shows each agent's default directory.
- `--dir <path>` installs to the given directory; for agents not in the preset list, point `--dir` at their skills directory.
- If the mirror has not synced the new package (404): add `--registry=https://registry.npmjs.org/` (a proxy may be needed in China), or wait for the mirror cache.

### Method 2: git clone (developers / git available)

```text
git clone https://github.com/YottaMeta/yotta-workflow.git <your-skills-dir>/yotta-workflow
```

### Method 3: GitHub Download ZIP (manual / no git)

On the GitHub repository `YottaMeta/yotta-workflow`, click **Code → Download ZIP**, unzip it and put the `yotta-workflow` folder into the agent's skills directory.

### Method 4: install.sh (multi-agent one-liner script)

```text
bash install.sh --agent <name>   # install to the agent's default user-level directory
bash install.sh --dir <path>     # install to the given directory
bash install.sh --list           # list agents -> default directories
```

> Method 1 uses the npm registry (npmmirror / npmjs) and does not depend on GitHub; Methods 2/3 use GitHub and may fail without a proxy in China.
## Upgrade / uninstall

- **Upgrade**: reinstall the latest version to overwrite — rerun the install command you used (e.g. `npx -y @yottameta/yotta-workflow@0.4.5 --agent <name>` or `bash install.sh --agent <name>`). Old files in the skill directory are replaced; the project state files (`.workflow\`) are unaffected.
- **Uninstall**: delete the `yotta-workflow` folder under the target agent's skills directory (see the table above). Uninstalling does not affect state files already written into a project.

## FAQ

- **Where is the state directory?** Accept an explicitly specified project root first; otherwise walk upward from the cwd to find an existing `.workflow\`. If neither exists, ask. State always lives at `<project root>\.workflow\`, not in a source directory or workspace root.
- **Multiple agents out of sync?** Confirm they point to the same project directory (the same `.workflow\`). This skill is designed to share one state; if each built its own `.workflow`, the project directory differs.
- **The source directory has `.git`; should state live there?** Not by that signal alone. State belongs under the project-root `.workflow`; the user decides how source directories are organized.
- **Project already has its own handoff mechanism?** Keep it, only satisfying the two mandatory points: read state on start, update state and leave an anchor on finish.

## Development & checks

Run inside this project: `python tools/validate-skill.py yotta-workflow`.

## References

- references/faq.md
- references/path-model.md
- references/walkthroughs.md
- references/exception-playbook.md

## License

MIT © YottaMeta
