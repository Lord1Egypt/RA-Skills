# cybernetic-thinking

> [中文](README_CN.md) | **English**

---

## What it is

A skill for AI coding agents. It does one thing: before the model writes or changes code, it makes the model think through the problem with a control-theory and systems-theory lens — what's the state, can I observe it, is it stable, where are the bounds, how is everything coupled — and only then act.

This skill doesn't teach the model *how to code*. It teaches it *how to think*. Two books underneath:

- Tsien Hsue-shen (钱学森) & Song Jian (宋健), *Engineering Cybernetics* — the mathematical foundations: stability, feedback, multivariable decoupling, disturbance compensation, bounded control, discrete systems.
- Jin Guantao (金观涛), *Cybernetics and Scientific Methodology* — the epistemological foundations: possibility space, conjugate control, black-box recognition, information–control dependence, ultra-stability, bifurcation, catastrophe.

Language- and framework-agnostic. A web service, a data pipeline, a compiler pass, or an LLM agent loop — all fit.

## What it solves

The common pain when coding: you change one place, another place breaks; you fix a bug, you introduce a new one; tests pass, production still fails. Most of the time this isn't carelessness — it's that you didn't figure out what state the system was actually in, or where your change was going to push it.

Use it when:

- You're changing legacy code you don't fully understand
- You're debugging something intermittent and hard to reproduce
- You're refactoring modules tangled with each other
- A change needs to be both correct and robust

## Core idea

**A program is a dynamical system, and you are the controller.**

Every change injects a control signal. You only partially observe the true state. Bugs are unstable or poorly-damped trajectories. Debugging is state estimation. Tests are sensors in a feedback loop. Closed loop beats open loop.

## Installation

This skill targets AI coding agents that support custom skills (Claude Code, Codex, Kilo, WorkBuddy, Trae, Cursor, Aider, etc.).

> **Renamed in 0.4.0**: the package was renamed from `skill-systems-thinking` to `skill-cybernetic-thinking`. If you installed the old name, remove it first: `rm -rf ~/.config/kilo/skills/skill-systems-thinking` (adjust for your agent), then install the new one.

### npx install (recommended)

```bash
npx skill-cybernetic-thinking install
```

The installer uses an interactive TUI (powered by `@clack/prompts`). It scans your machine for known AI agents, shows the detected ones, then walks you through: detected-only or customize → pick agents → project or global location → link.

```text
$ npx skill-cybernetic-thinking install

◇ Detected agents
  Claude Code      ~/.claude
  Codex CLI        ~/.codex
  Kilo             ~/.kilo

◆ Install for detected agents only, or add more?
│ ● Detected only (claude, codex, kilo)
│ ○ Customize...
└
◆ Install location
│ ● Project (/current/dir)
│ ○ Global (~)
└
  [ok]   ~/.claude/skills/skill-cybernetic-thinking
  [ok]   ~/.codex/skills/skill-cybernetic-thinking
  [ok]   ~/.kilo/skills/skill-cybernetic-thinking

◇ Done! installed: 3, skipped: 0, failed: 0
```

Choose `Customize...` to open a multiselect (space to toggle) of all known agents.

Common flags:

```bash
# Skip prompts, install for detected agents
npx skill-cybernetic-thinking install -y

# Pick agents explicitly (no prompts)
npx skill-cybernetic-thinking install -a claude,codex

# Install to a custom directory (for agents not on the list)
npx skill-cybernetic-thinking install --path ~/my-agent/skills

# Global paths only / project-local only
npx skill-cybernetic-thinking install --global
npx skill-cybernetic-thinking install --local

# Overwrite existing links
npx skill-cybernetic-thinking install --force

# Help
npx skill-cybernetic-thinking install --help
```

In non-TTY environments (CI, pipes) the TUI is skipped and it installs for all detected agents at global scope.

### npm install (download only)

```bash
npm install skill-cybernetic-thinking
```

This only downloads the package into `node_modules`; it does **not** link anything into your agent skill directories. After this, still run:

```bash
npx skill-cybernetic-thinking install
```

### GitHub / Gitee download

```bash
git clone https://github.com/ShrimpLeon/cybernetic-thinking.git
# or
git clone https://gitee.com/leon0903/cybernetic-thinking.git

cp -r cybernetic-thinking <agent-skills-dir>/
```

### Agent skill directories

npx install links automatically. For manual install, here are the directories:

| Agent | Skill directory |
|---|---|
| Claude Code | `~/.claude/skills/` or project `.claude/skills/` |
| Codex CLI | `~/.codex/skills/` or project `.codex/skills/` |
| Cursor | `~/.cursor/skills/` or project `.cursor/skills/` |
| Gemini CLI | `~/.gemini/skills/` or project `.gemini/skills/` |
| GitHub Copilot | `~/.copilot/skills/` (user-level; project `.github/skills/` also read by the CLI) |
| Kilo | `~/.kilo/skills/` or project `.kilo/skills/` |
| Aider | `~/.aider/skills/` or project `.aider/skills/` |
| Windsurf | `~/.windsurf/skills/` or project `.windsurf/skills/` |
| Zed | `~/.zed/skills/` or project `.zed/skills/` |
| WorkBuddy | `~/.workbuddy/skills/` or project `.workbuddy/skills/` |
| Trae | `~/.trae/skills/` (international) or project `.trae/skills/`; China / **Trae Work** uses `~/.trae-cn/skills/` (the installer checks both) |
| Agent Skills standard (`.agents`) | `~/.agents/skills/` — the user-level shared folder (cross-agent standard, read by Trae, Kilo, Claude and others) |

For agents not on the list, use `--path` to point at the directory.

### Verify install

```bash
pwsh init.ps1
# or
powershell -ExecutionPolicy Bypass -File init.ps1
```

Look for `Verification Complete — OK`.

## Usage

### 1. When to load

- Architecture design
- Debugging non-deterministic behavior
- Cross-module refactoring
- Any change where correctness AND robustness both matter

### 2. Read SKILL.md

Start with `SKILL.md`. It has a runtime-prompt block that installs 13 cognitive laws into the model's thinking. The workflow below follows naturally.

### 3. Name things before touching code

Before proposing any change, the LLM must name:

- `x` — the controlled variable: what must stay correct
- `u` — the control variable: the lever you will actually move
- Possibility space: what set of outcomes are you choosing among? Which does your change rule out?
- Observability: how will you know the current value of `x`? If you can't see it, you can't control it
- Bounds: every actuator saturates; no unbounded loop is acceptable

### 4. Seven-step loop

| Step | Principle | Reference |
|---|---|---|
| 1 | Identify — name `x`, `u`, possibility space, observability, bounds | `references/state-and-control.md`, `references/possibility-space.md` |
| 2 | Analyze — reproduce, measure, locate fault, model as black-box hypothesis | `references/modeling.md`, `references/black-box-epistemology.md` |
| 3 | Stabilize — kill divergence / oscillation / leaks before features | `references/stability.md`, `references/system-evolution.md` |
| 4 | Synthesize — minimal `u`; decouple what hurts, coordinate what helps; conjugate control when needed | `references/multivariable.md`, `references/possibility-space.md` |
| 5 | Close the loop — observe actual result; correct until bounded | `references/closed-loop-workflow.md`, `references/information-and-control.md` |
| 6 | Compensate — feedforward measurable disturbances; damping for delay | `references/disturbance.md` |
| 7 | Optimize — only then tune secondary indicators | `references/bounded-control.md` |

For sampled-system and test-cadence concerns, see `references/discrete-systems.md`.

### 5. Templates

These live in the skill's `templates/` directory:

- Debugging: copy `templates/debugging-checklist.md` into the session
- Planning: use `templates/change-proposal.md` to write the control plan

### 6. Self-audit

Before declaring done, pass all MUST checks in `evals/checks.json`.

## 13 cognitive laws

1. Name `x` before `u`. Unnamed targets are unregulated.
2. Name the possibility space. A change that doesn't narrow uncertainty isn't control — it's motion.
3. Observe before you guess. Measure current behavior before synthesizing the fix.
4. When control fails, suspect a missing information channel before a missing actuator.
5. Stabilize before you optimize. Divergence under perturbation is failure.
6. Close the loop. Observe the actual result; correct until deviation is bounded. Feedback amplifies a weak controller.
7. Feedforward measurable disturbances; feedback the rest. Never crank gain on delay.
8. Decouple harmful coupling. Coordinate beneficial coupling. Regulate relations, not just absolutes.
9. Minimal control. The smallest `u` that moves `x` to target. No speculative extras.
10. Convergence. Corrections must shrink. If they grow, you're unstable — stop and re-identify.
11. Treat the system as a black box. Your model is a hypothesis, not the internals. Open one layer at a time.
12. Make your model falsifiable. State what observation would prove your hypothesis wrong, before acting.
13. Recognize ultra-stability and bifurcations. Some instability is a repair mechanism; at bifurcations, small choices lock in large differences.

## Worked example

**Symptom:** an API endpoint intermittently returns 500 under load.

| Step | Control-theoretic action |
|---|---|
| Identify | `x` = error rate; `u` = retry/timeout/cache logic; bound = request budget. Possibility space = {timeout too short, dependency slow, retry storm, cache miss cascade, ...}. The fix must narrow this set. |
| Analyze | Reproduce under load; measure error rate climbs with concurrency (unstable). Hypothesis: retry storm. Falsifiable prediction: if I bound retries to 2 with backoff, dependency p99 drops below 500 ms. |
| Stabilize | Add circuit breaker + bounded retries with backoff → error rate bounded. Identified as oscillation, not steady-state drift. |
| Synthesize | Minimal change; don't rewrite the service. |
| Close the loop | Load-test again; error rate converges to ~0, not growing. |
| Compensate | Feedforward on measurable dependency outage (fail fast) + feedback on the rest. |
| Optimize | Only now trim p99 latency. |

**Without this lens:** add retries with no bound → retry storm (unstable delay loop) → next "fix" removes retries entirely (feedback overshoot, direction reversal) → original bug returns. Laws 10 and 13 catch both errors.

## References

12 deep-dive references, each anchored to the original text with LLM behavior patterns:

| Topic | File |
|---|---|
| Closed-loop workflow | `references/closed-loop-workflow.md` |
| State, control, observability, bounds | `references/state-and-control.md` |
| Stability (incl. stable-state structure, feedback overshoot, ultra-stability) | `references/stability.md` |
| Modeling and model validity | `references/modeling.md` |
| Multivariable: decouple and coordinate | `references/multivariable.md` |
| Disturbance compensation and time-delay | `references/disturbance.md` |
| Bounded control | `references/bounded-control.md` |
| Discrete systems and test cadence | `references/discrete-systems.md` |
| Possibility space and conjugate control | `references/possibility-space.md` |
| Black-box epistemology and falsifiability | `references/black-box-epistemology.md` |
| Information–control dependence | `references/information-and-control.md` |
| System evolution: stable-state, ultra-stability, bifurcation, catastrophe | `references/system-evolution.md` |
| Original text excerpts from both books | `references/original-text.md` |

## Self-audit

`evals/checks.json` lists MUST/SHOULD checks an LLM or reviewer applies to confirm the discipline was followed. All MUST items must pass before a task is called done.

## Contributing

- Every claim in `SKILL.md` must trace to a reference file
- Every reference link must resolve to an existing file
- Keep the skill small and aligned with both books
- Run `./init.ps1` before submitting

See `AGENTS.md` for the full working rules and definition of done.

## Version

This skill follows [Semantic Versioning](https://semver.org/) (`X.Y.Z`).

| Version | Date | Notes |
|---|---|---|
| 0.6.0 | 2026-08-09 | Expanded the agent registry and made it multi-root: added **WorkBuddy** (`~/.workbuddy`), **Trae** (`~/.trae` + China/Trae Work `~/.trae-cn`), and the cross-agent **Agent Skills standard / user-level `.agents`** folder (`~/.agents/skills`). Kilo now also detects `~/.kilocode`. Custom install can now target `~/.agents/skills`. Fixed **GitHub Copilot** detection: it now targets `~/.copilot/skills` (the real Copilot CLI user-level dir) instead of `~/.github`, which false-positived on machines that only had git/GitHub Desktop/gh installed. |
| 0.5.0 | 2026-08-05 | Rewrote `scripts/install.js` with `@clack/prompts` TUI (detect → select → location → install → done); fixed `install` subcommand crash; added Gemini CLI; non-TTY auto-fallback. Added `author`/`tags` to `SKILL.md` frontmatter + `skills-sh` keyword for skills.sh discoverability. |
| 0.4.0 | 2026-07-30 | **Renamed** from `skill-systems-thinking` to `skill-cybernetic-thinking` (package, repo, skill name). Old package deprecated on npm. |
| 0.3.1 | 2026-07-30 | Removed redundant `assets/runtime-prompt.txt` (inlined in `SKILL.md`); cleaned up `assets/` directory and related references |
| 0.3.0 | 2026-07-30 | Integrated *Cybernetics and Scientific Methodology*; added 4 references, 5 cognitive laws; rewrote install UX (scan list + selection + custom path) |
| 0.2.0 | 2026-07-26 | Added agent selection and location flags to install CLI |
| 0.1.5 | 2026-07-25 | Split README.md / README_CN.md; unified version numbers |
| 0.1.4 | 2026-07-25 | Bug fix |
| 0.1.3 | 2026-07-25 | Unified version numbers; added XYZ convention to AGENTS.md; removed postinstall script |
| 0.1.2 | 2026-07-25 | Added Gitee download link; updated repository and homepage to Gitee |
| 0.1.1 | 2026-07-24 | Fixed repository.url; expanded keywords; added homepage and bin field |
| 0.1.0 | 2026-07-24 | Initial public release |

Full history: [CHANGELOG.md](CHANGELOG.md).

## License

MIT License. See [LICENSE](LICENSE).

## Source

- Qian Xuesen (钱学森) & Song Jian (宋健), *Engineering Cybernetics* (工程控制论) — the mathematical foundations.
- Jin Guantao (金观涛), *Cybernetics and Scientific Methodology* (控制论与科学方法论) — the epistemological foundations.

The original books and their mathematical derivations are the authoritative source; this skill is a distilled, practice-oriented interpretation, not a replacement.
