---
name: skill-shell
description: Evaluate external skills before installation and decide whether to install, reject, or absorb only the useful ideas. Use when a user shares a ClawHub/GitHub skill link, asks whether a skill is worth installing, asks for a code/safety review before installation, or wants to compare a skill's workflow with the current OpenClaw workflow.
---

# Skill Shell

Use this skill to gate external skills before they enter the current OpenClaw workflow.

## Core rule

Do not treat every published skill as worth installing.
First decide what problem the user is actually trying to solve.
Then inspect the package, judge the risks, and decide one of three outcomes:

1. **Install candidate**
2. **Review-only / absorb ideas**
3. **Reject / do not install**

## Preferred workflow

1. Clarify the real capability the user wants.
2. Classify the skill type before judging it.
3. Inspect the package contents, not just the landing page.
4. Separate **static review** from **dynamic validation**.
5. Check whether it fits the current OpenClaw workflow or drags in another ecosystem.
6. Check whether it adds ongoing token cost, hooks, background behavior, or unstable config changes.
7. Check environment landing zone and validation level: shell, gateway, LaunchAgent, cron.
8. Explain the recommendation in plain language.
9. Install only after explicit user approval.

## Skill type classification

Classify the candidate into one primary type before making a recommendation:

- **Capability skill**: adds a concrete new capability (search, extraction, automation, generation, file handling)
- **Integration skill**: depends on credentials, env vars, services, or runtime placement to become usable
- **Automation skill**: controls browsers, CLIs, workflows, or long-running operational behavior
- **Workflow / methodology skill**: mostly guidance, process, prompts, or ways of thinking
- **Shell / incomplete skill**: mostly docs/meta, or promises code/assets that are not actually present

Different types require different scrutiny. Do not evaluate them all with one generic standard.

## Static review vs dynamic validation

### Static review

Static review asks:
- what files are actually present
- whether docs match the package
- what dependencies and scripts exist
- whether the package looks coherent or misleading
- whether Codex should be used for a deeper read-only audit

Static review is often safe to delegate to Codex.

### Dynamic validation

Dynamic validation asks:
- does it really install
- does it actually run
- which environment layers can use it
- does it work in current shell, main agent, gateway, LaunchAgent, cron
- does it rely on runtime downloads, browser binaries, proxies, daemons, or service state

Dynamic validation must be owned and finalized by the main agent before something is called fully usable.

## Environment sensitivity levels

Use these levels when judging readiness:

- **L1**: current shell only
- **L2**: main agent session
- **L3**: gateway / LaunchAgent / service environment
- **L4**: cron / automation / unattended runs

A skill is not "fully ready" unless it has passed the level actually required by the user's use case.

## What to favor

Favor skills that:
- add a concrete capability
- can be verified locally
- have understandable dependencies
- fit the user's current workflow
- improve execution more than they increase complexity

## What to distrust

Distrust skills that:
- are mostly docs or prompt shells
- claim code that is not present
- mainly redirect to another package manager or ecosystem
- add hooks, auto-reminders, or background behavior without clear value
- increase token usage more than they improve outcomes

Reject immediately or escalate hard if static review finds any of these red flags:
- `curl` / `wget` to unclear or unrelated endpoints
- unexplained data exfiltration to external servers
- requests for credentials, tokens, API keys, browser cookies, or sessions
- reads of `~/.ssh`, `~/.aws`, `~/.config`, or similar credential locations without a very clear reason
- reads of `MEMORY.md`, `USER.md`, `SOUL.md`, or `IDENTITY.md` from outside the normal workspace purpose
- `eval(...)` / `exec(...)` with external or untrusted input
- unexplained base64 decode / encoded payload execution / obfuscated code
- network calls to raw IPs instead of understandable domains
- silent package installs or background downloads not clearly documented
- writes or modifications outside the workspace without explicit need
- requests for elevated / sudo privileges

## Promotion rule

When a reviewed skill has useful ideas but poor packaging, do not install it by default.
Instead, absorb the useful parts into the local workflow:
- behavioral patterns -> `SOUL.md`
- workflow rules -> `AGENTS.md`
- tool gotchas -> `TOOLS.md`
- session-specific lessons -> `memory/YYYY-MM-DD.md`

Typical examples of "absorb, don't install":
- good red-flag lists
- trust heuristics
- repo vetting commands
- review templates
- decision labels that improve reporting but do not require a separate skill

## Checklist

Read `references/checklist.md` when evaluating a candidate skill.

## Output style

Report with this structure:
- conclusion
- skill type
- source / version / visible popularity signals
- static review result
- dynamic validation required or not
- environment sensitivity level
- what it really does
- what is actually in the package
- red flags (if any)
- risks
- fit with current workflow
- recommendation

Preferred recommendation labels:
- install
- install, but require dynamic validation
- absorb ideas only
- postpone
- reject

When helpful, also classify overall risk as:
- LOW
- MEDIUM
- HIGH
- EXTREME

Keep the answer direct. Prefer decision quality over enthusiasm.

## Attribution

- Author: 石屹
- For: 加十
- Affiliation: 为加十工作流设计
- Note: built for 加十
