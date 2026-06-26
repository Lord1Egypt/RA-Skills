# SprintX OpenClaw Handoff

Standalone public repo for SprintX's first ClawHub skill.

This skill helps an existing OpenClaw operator connect SprintX with the minimum proof packet that SprintX can verify today:

```text
sx auth
-> sx project use
-> sx event
-> sx artifact add
-> sx status
-> sx brief
```

It is intentionally narrow.

- No custom MCP server
- No hidden SprintX automation
- No generic natural-language control plane
- No project creation flow inside the skill

Links:
- ClawHub: https://clawhub.ai/terry3838/sprintx-openclaw-handoff
- GitHub: https://github.com/terry3838/SprintX-SKILL
- SprintX handoff quickstart: https://www.sprintx.co.kr/docs/getting-started/openclaw-handoff-quickstart
- SprintX CLI quickstart: https://www.sprintx.co.kr/docs/getting-started/cli-quickstart
- Korean README: [README.ko.md](./README.ko.md)
- Chinese README: [README.zh.md](./README.zh.md)

## Why This Exists

OpenClaw users can already connect to SprintX with the shipped CLI.

The problem is first-use friction. The first connection still asks people to remember too much:

- which command comes first
- where the `projectId` comes from
- what success looks like
- what to do when the packet fails halfway through

This skill compresses that into one operator-facing flow.

Not more magic. Less confusion.

## What The Skill Does

The skill guides the operator through:

1. Checking SprintX prerequisites
2. Verifying that `sx` already exists before recommending install
3. Using the handoff card or handoff URL as the primary `projectId` source
4. Falling back to `sx project list` only when recovery is needed
5. Running the proof packet in the correct order
6. Verifying success with `sx status` and `sx brief`
7. Handling common failures with explicit rescue guidance

## Who This Is For

Use this if:

- you already use OpenClaw
- you already have a SprintX account
- you already have a SprintX project or can create one on the web
- you want the safest current handoff path, not a broad integration surface

Do not use this skill if you want:

- SprintX project creation from chat
- task CRUD from the skill itself
- review or approval workflows
- a remote MCP server

## Quick Start

### 1. Install the skill

From ClawHub:

```bash
clawhub install sprintx-openclaw-handoff
```

If your environment requires non-interactive install and you have already reviewed the skill:

```bash
clawhub install sprintx-openclaw-handoff --force --no-input
```

### 2. Let the skill walk the operator

Typical prompt:

```text
Use $sprintx-openclaw-handoff to connect my existing OpenClaw runtime to SprintX.
```

### 3. Follow the proof packet

The skill will keep the operator on the narrow path:

```bash
sx auth
sx project use <project-id>
sx event --type runtime.started --summary "OpenClaw handoff started"
sx artifact add --title "first-log" --reference-uri "file:///tmp/openclaw.log" --content-type "text/plain" --summary "Initial OpenClaw evidence"
sx status
sx brief
```

## Prerequisites

Before the handoff starts, the operator should have:

- a SprintX web session
- a SprintX project
- access to `/dashboard?handoff=1&projectId=<id>` or the handoff card

If the `projectId` is already visible there, the skill uses it directly.

`sx project list` is not the default first step. It is recovery only.

## Trust Boundary

This is important.

- SprintX is not the executor. OpenClaw executes, SprintX reads and governs.
- The default auth path is browser-approved `sx auth`.
- Access-token override is treated as advanced or break-glass only.
- The skill explicitly warns against pasting tokens into chat.
- Provider API keys are outside this flow.

## Advanced Operators

Headless and CI-style users are supported, but not as the primary path.

Examples:

```bash
sx --headless auth
```

The skill also documents the advanced access-token override, but keeps it out of the main onboarding path on purpose.

## Repo Structure

```text
SprintX-SKILL/
├── SKILL.md
├── README.md
├── CHANGELOG.md
├── LICENSE
├── LICENSE.md
├── package.json
├── references/
│   └── source-of-truth.md
├── scripts/
│   ├── check-skill.mjs
│   └── check-contract.mjs
└── .github/workflows/ci.yml
```

Design choice:

- `SKILL.md` is the only operator-truth document
- `README.md` is for humans evaluating the repo
- `references/` holds upstream links and source-of-truth docs
- CI validates the repo, but publish stays manual

## Validation

Run:

```bash
npm run check
```

This verifies:

- frontmatter shape
- declared runtime requirements
- install metadata
- license presence
- command order
- recovery-only `sx project list`
- advanced-only token guidance

## Release Model

This repo uses validation CI plus manual ClawHub publish.

Publish:

```bash
clawhub publish . \
  --slug sprintx-openclaw-handoff \
  --name "SprintX OpenClaw Handoff" \
  --version 0.1.3 \
  --tags latest \
  --changelog "Add localized READMEs and tighten metadata to match real requirements"
```

We keep publish manual on purpose. The current ClawHub docs clearly support CLI-driven skill publish, while plugin/package auto-publish flows are more mature than skill auto-publish flows today.

Note:

- In the locally verified `clawhub` CLI, the working command is top-level `clawhub publish <path>`.
- Some upstream docs still describe `clawhub skill publish`.
- Re-check the installed CLI help before cutting a release.

## Korean Note

이 저장소는 SprintX의 첫 공개 OpenClaw skill 저장소입니다.

- 기본 경로는 `sx auth -> sx project use -> sx event -> sx artifact add -> sx status -> sx brief`
- `projectId`는 handoff URL/card가 우선
- `sx project list`는 복구 경로
- access-token override는 기본 경로가 아니라 advanced-only

한국어 상세 문서:

- https://www.sprintx.co.kr/docs/getting-started/openclaw-handoff-quickstart
- https://www.sprintx.co.kr/docs/getting-started/cli-quickstart.ko
