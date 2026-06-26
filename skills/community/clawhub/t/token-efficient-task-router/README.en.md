<div align="center">

[![中文](https://img.shields.io/badge/%E4%B8%AD%E6%96%87-README.md-111827?style=flat-square)](./README.md) · **English**

# token-efficient-task-router

#### A token-efficient task routing and execution control skill for AI agents

[![Version](https://img.shields.io/badge/version-v0.6.8-2563EB?style=for-the-badge)](./CHANGELOG.md)
[![License](https://img.shields.io/badge/License-MIT-0F766E?style=for-the-badge)](./LICENSE)
[![Modes](https://img.shields.io/badge/Modes-Ask%20%7C%20Plan%20%7C%20Craft%20%7C%20Expert-7C3AED?style=for-the-badge)](./SKILL.md)
[![Token](https://img.shields.io/badge/Token-Efficient-F59E0B?style=for-the-badge)](./GUIDE.en.md)

![WorkBuddy](https://img.shields.io/badge/WorkBuddy-Supported-2563EB?style=flat-square)
![iMA Copilot](https://img.shields.io/badge/iMA_Copilot-Supported-0F766E?style=flat-square)
![CodeBuddy](https://img.shields.io/badge/CodeBuddy-Supported-7C3AED?style=flat-square)
![OpenClaw](https://img.shields.io/badge/OpenClaw-Supported-E11D48?style=flat-square)

</div>

This is not a domain skill. It is a control-layer skill for agent behavior.

Its job is to make an agent pause and decide before token use, long outputs, broad context loading, file edits, or risky execution start expanding.

---

## What It Is

`token-efficient-task-router` acts as a:

- token cost controller
- task mode router
- pre-execution safety gate
- ROI manager for agent work

It helps an agent decide:

- whether the task is clear enough to act on
- whether the task should be diagnosed, planned, crafted, or escalated
- whether user confirmation is needed
- whether the user needs a sample, a next step, staged execution, or full delivery

## What It Solves

Many agents become inefficient in the same ways:

- they read too much before understanding the real task
- they explain too much before validating the scope
- they edit too early before checking file boundaries
- they over-deliver before proving full-batch work is actually needed

This skill is designed to make agent execution cheaper, safer, and more aligned with the user's real need.

## Best Fit

This skill is especially useful when:

- the request is somewhat ambiguous
- the task may involve files, folders, project structure, or knowledge bases
- the user wants fewer retries and lower token cost
- the agent should choose between Ask, Plan, Craft, and Expert behavior
- the task includes refactoring, batch operations, long-form output, or large-scope organization

## Not The Best Fit

This skill should not slow down simple work.

It is usually unnecessary for:

- one-line rewrites
- short translation
- single command explanation
- tiny template generation
- clear, low-risk, one-pass tasks

## Core Capabilities

### 1. Four-mode routing

- `Ask Mode`: diagnosis, explanation, risk analysis, next-step advice
- `Plan Mode`: define scope first, then wait for confirmation when needed
- `Craft Mode`: fast delivery for clear small tasks
- `Expert Mode`: recommend a specialist lens when more trial-and-error is wasteful

### 2. Interactive routing confirmation

When a task is ambiguous, large, costly, or file-sensitive, the skill can ask the user to confirm:

- complexity
- preferred mode
- output depth

### 3. Progressive delivery

Default progression:

`decision -> sample -> staged execution -> full batch`

instead of “do everything immediately.”

### 4. File safety gates

Without confirmation, it does not encourage:

- overwriting core files
- deleting files
- batch renaming
- batch moving
- deployment-affecting changes
- database changes
- large unreviewed rewrites

### 5. Token budget control

Built-in budget modes:

- `Micro`
- `Standard`
- `Deep`
- `Artifact`

## Platform Profiles

### WorkBuddy

Defaults should stay conservative around files and folders. Read-only analysis, scope confirmation, and sample-batch handling should come first.

### iMA Copilot

Knowledge work should start narrow. Prefer the most relevant materials, short evidence-based output, and grouped summaries before long reports.

### CodeBuddy

Code work should control read budget, edit budget, and test budget to avoid full-repo scanning and broad refactors by default.

## Example Prompts

```text
Please decide whether this task should use Ask, Plan, Craft, or Expert mode.
```

```text
Use Plan Mode first and do not modify files yet.
```

```text
This is a clear small task. Use Craft Mode and return the result directly.
```

```text
Diagnose this error in Ask Mode first. Do not change code yet.
```

```text
Use the lowest-token approach and only give me the next action.
```

## Installation

### Folder install

Place the `token-efficient-task-router/` directory into a supported skill directory or upload bundle.

### Archive install

Current release artifacts:

- `token-efficient-task-router-v0.6.8.zip`
- `token-efficient-task-router-v0.6.8.skill`

Latest local aliases:

- `token-efficient-task-router.zip`
- `token-efficient-task-router.skill`

### Codex local install

For local Codex use, place the folder under:

```text
~/.codex/skills/token-efficient-task-router
```

Restarting the app after installation is recommended.

### WorkBuddy install

According to the official WorkBuddy documentation, the standard flow is to import a local skill package from the Skills Market UI.

Recommended steps:

1. Open the Skills Market in WorkBuddy
2. Click `Add Skill` or `Upload Skill`
3. Choose the local package file, preferably `token-efficient-task-router-v0.6.8.zip`
4. After import, confirm that the skill is enabled in the installed skills list

Practical recommendation:

- enable this skill only when it is relevant to the current task
- if you are publishing to SkillHub, prefer a dedicated SkillHub-ready zip package

### CodeBuddy install

The official CodeBuddy skills documentation supports two locations:

1. User-level skills: `~/.codebuddy/skills/`
2. Project-level skills: `.codebuddy/skills/`

Recommended options:

#### Option 1: User-level install

Copy the entire `token-efficient-task-router/` folder to:

```text
~/.codebuddy/skills/token-efficient-task-router
```

#### Option 2: Project-level install

If you only want it inside one project, copy it to:

```text
<project-root>/.codebuddy/skills/token-efficient-task-router
```

After installation, you can use `/skills` in CodeBuddy to verify that the skill is loaded.

### QClaw install

Public QClaw materials state that QClaw connects to the ClawHub and GitHub skills ecosystem, and that skills can be installed from ClawHub.

That makes the safest installation guidance:

#### Option 1: Install through ClawHub or the skills marketplace

If your QClaw build exposes a Skills Market or ClawHub entry, prefer installing the skill there.

#### Option 2: Import from a GitHub skill source

If your QClaw build supports GitHub-based skill ingestion, use this repository or a release package as the import source.

#### Option 3: Manual OpenClaw-compatible install

Because QClaw is built on the OpenClaw ecosystem, environments that expose manual skill directories can usually use an OpenClaw-compatible folder install:

```text
~/.openclaw/skills/token-efficient-task-router
```

or the active workspace:

```text
<workspace>/skills/token-efficient-task-router
```

If you use the manual directory route, restarting QClaw or opening a new session is recommended so the skill reloads cleanly.

## Repository Structure

```text
token-efficient-task-router/
├── .gitignore
├── SKILL.md
├── LICENSE
├── README.md
├── README.en.md
├── GUIDE.md
├── GUIDE.en.md
├── VERSION
├── CHANGELOG.md
├── references/
├── templates/
├── examples/
├── tests/
└── scripts/
```

## Public Documents

- [README.md](./README.md): Chinese repository homepage
- [README.en.md](./README.en.md): English repository homepage
- [GUIDE.md](./GUIDE.md): Chinese external usage guide
- [GUIDE.en.md](./GUIDE.en.md): English external usage guide
- [CHANGELOG.md](./CHANGELOG.md): version history
- [LICENSE](./LICENSE): open-source license

## Version And License

- Current version: `v0.6.8`
- License: `MIT`

---

For the Chinese version, see [README.md](./README.md).
