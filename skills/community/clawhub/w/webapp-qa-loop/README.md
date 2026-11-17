# Webapp QA Loop

[English](README.md) | [简体中文](README.zh-CN.md)

[GitHub](https://github.com/liubai00/webapp-qa-loop) | [ClawHub](https://clawhub.ai/liubai00/skills/webapp-qa-loop)

Browser-centered QA for coding agents: inspect a runnable web application through a real browser, preserve evidence in a durable ledger, repair root causes when authorized, and gate releases with post-deployment regression.

The skill is designed to reduce back-and-forth without silently expanding authority. It discovers repository and runtime facts first, but treats source changes, Git delivery, deployment, rollback, and high-side-effect browser actions as separate permissions.

## What it provides

- Three explicit operating modes: `audit`, `repair`, and `release`.
- Real click-through testing instead of screenshot-only review.
- Durable, resumable QA state through the bundled schema-v2 ledger.
- Evidence-backed issue triage and impact-based regression from R0 to R4.
- Root-cause repair with an explicit reuse-before-new decision record.
- Release gates that bind checks to one target, artifact, and deployment attempt.
- Bounded retry, rollback, cleanup, and external-delivery rules.
- User-language reporting without duplicating the execution rules.

## When to use it

Use this skill for:

- browser smoke or regression testing;
- click-through functional, interaction, UI, and accessibility checks;
- testing and repairing an existing runnable web application;
- verifying an already deployed version;
- an explicitly authorized deploy-and-regress workflow.

Do not use it as a substitute for static code review, API-only testing, unit-test-only work, greenfield UI creation, a screenshot-only design critique, native-app testing, dedicated security testing, or load testing.

## Language behavior

`SKILL.md` is maintained in English as the single canonical execution contract. The agent replies in the user's language unless another language is requested. Ledger enums, IDs, and command arguments stay unchanged so runs remain portable and machine-readable.

There is therefore no separate language toggle to configure: ask in English and receive English; ask in Chinese and receive Chinese.

## Requirements

- An agent runtime with real-browser control.
- Python 3.10 or newer, available as `python` or `python3`.
- A runnable web application or an accessible authorized test target.
- Repository and shell access only when repair is requested.
- Deployment and Git credentials only when those separate actions are explicitly authorized.

## Install

### Codex

Clone the repository into the Codex skills directory:

```bash
git clone https://github.com/liubai00/webapp-qa-loop.git "${CODEX_HOME:-$HOME/.codex}/skills/webapp-qa-loop"
```

Restart Codex after installation so the skill catalog is refreshed.

### OpenClaw / ClawHub

```bash
openclaw skills install @liubai00/webapp-qa-loop
```

The standalone registry client can also install it:

```bash
clawhub install @liubai00/webapp-qa-loop
```

## Use

The skill can be selected automatically for matching work or invoked explicitly as `$webapp-qa-loop`.

Audit only:

```text
Use $webapp-qa-loop to smoke-test the current web app in a real browser and give me an evidence-backed defect report. Do not change code.
```

Test and repair:

```text
Use $webapp-qa-loop to test this checkout flow, repair confirmed in-scope defects, and rerun impact-based regression. Do not commit, push, or deploy.
```

Release and verify:

```text
Use $webapp-qa-loop to test and repair the application, deploy the verified build to the explicitly named staging target, and run post-deployment regression. Commit or push only if I authorize those actions separately.
```

The agent infers the least-permissive mode that satisfies the request. A request to test does not authorize repairs; a request to repair does not authorize Git operations or deployment.

## Durable QA ledger

For repair, release, and nontrivial audit runs, the skill uses `scripts/qa_ledger.py` to preserve targets, planned scenarios, checks, evidence references, issues, repair cycles, release attempts, cleanup, and settlement.

```bash
python scripts/qa_ledger.py --help
```

The helper records caller-supplied facts. It does not open a browser, execute project commands, deploy, or grant authority.

## Validate

Run the ledger regression suite:

```bash
python scripts/test_qa_ledger.py
```

Validate the skill structure with Codex's `skill-creator` validator when it is available:

```bash
python /path/to/skill-creator/scripts/quick_validate.py .
```

## Repository layout

```text
.
|-- SKILL.md
|-- agents/openai.yaml
|-- references/
|   |-- automation-promotion.md
|   |-- browser-playbook.md
|   |-- issue-ledger.md
|   |-- release-and-rollback.md
|   |-- repair-and-reuse.md
|   `-- scope-and-selection.md
`-- scripts/
    |-- qa_ledger.py
    `-- test_qa_ledger.py
```

## Scope of assurance

The workflow proves only the declared and evidenced coverage. It deliberately avoids claims that an application is flawless, exhaustively tested, or defect-free.

## License

MIT-0. ClawHub also distributes published skills under MIT-0.
