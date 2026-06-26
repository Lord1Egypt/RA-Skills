---
name: sprintx-openclaw-handoff
description: Guide an existing OpenClaw operator through the SprintX handoff proof packet with the minimum safe steps: verify prerequisites, connect with sx auth, select the project, send the first event and artifact, then confirm read-back with sx status and sx brief.
version: 0.1.3
metadata:
  openclaw:
    requires:
      bins:
        - sx
    install:
      - kind: node
        package: "@sprint-x/cli"
        bins:
          - sx
    homepage: https://www.sprintx.co.kr/docs/getting-started/openclaw-handoff-quickstart
    emoji: "🧭"
---

# SprintX OpenClaw Handoff

Use this skill when an OpenClaw user needs to connect an existing SprintX account and project with the smallest proof packet that SprintX can verify today.

Do not use this skill for broad SprintX task management, review workflows, project creation, or generic natural-language control. This skill is a thin handoff layer over the shipped SprintX CLI contract.

한국어 안내:
- 이 스킬은 OpenClaw와 SprintX를 최소 연결 확인 경로로 붙일 때만 사용합니다.
- 기본 경로는 browser-approved `sx auth`입니다.
- 한국어 상세 문서는 `references/source-of-truth.md`의 링크를 따르세요.

## Primary Workflow

### 1. Confirm prerequisites

Before giving commands, verify all three are true:

1. The user is signed into SprintX on the web.
2. The user already has a SprintX project.
3. The user can see a `projectId` from `/dashboard?handoff=1&projectId=<id>` or the handoff card.

If the project does not exist yet, stop and send the user to SprintX onboarding first. Do not invent a project-creation flow inside this skill.

### 2. Check whether `sx` already exists

Ask the operator to run:

```bash
sx --help
```

If `sx` is already installed, skip installation and go straight to `sx auth`.

If `sx` is missing, install it:

```bash
npm install -g @sprint-x/cli
sx --help
```

### 3. Choose the project context

Default path:
- If the handoff URL or handoff card already shows a `projectId`, use it directly.

Command:

```bash
sx project use <project-id>
```

Success signal:
- Output includes `project_id`
- Output includes `receipt_id`

Recovery path only:
- Only use `sx project list` when the user does not have the `projectId` yet or needs to recover it from shared projects.

```bash
sx project list
```

Do not make `sx project list` the default first-touch step.

### 4. Run the proof packet in order

Run these commands in this order:

```bash
sx auth
sx project use <project-id>
sx event --type runtime.started --summary "OpenClaw handoff started"
sx artifact add --title "first-log" --reference-uri "file:///tmp/openclaw.log" --content-type "text/plain" --summary "Initial OpenClaw evidence"
sx status
sx brief
```

Ordering matters:
- `sx event` must happen before the first artifact receipt.
- `sx artifact upload` is still an alias, but prefer `sx artifact add` in the primary path.

### 5. Confirm success at each step

Use these pass/fail signals:

- `sx auth`
  The CLI opens the SprintX approval URL or prints it in headless mode, then stores the local session.
- `sx project use`
  Returns `project_id` and `receipt_id`.
- `sx event`
  Returns `status: accepted`.
- `sx artifact add`
  Returns `status: accepted`.
- `sx status`
  Reads the expected project context.
- `sx brief`
  Returns a bounded next-step summary for the same project.

If the user reaches `sx status` and `sx brief` successfully, the handoff is complete.

## Troubleshooting And Advanced Operators

The default path is always browser-approved `sx auth`.

Only move to this section when the user is in CI, headless, or another browserless environment.

### Headless auth

Use:

```bash
sx --headless auth
```

In headless mode, the approval URL is printed to stdout. The user should open that URL in a browser session that is already signed into SprintX.

### Access-token override

If the environment already injects an access token, SprintX CLI can skip browser auth.

Treat this as advanced or break-glass behavior only.

Hard rule:
- Do not ask users to paste tokens into chat.
- Do not recommend token copy/paste as the default onboarding path.

If the user needs the exact token override procedure or API URL override steps, point them to the upstream SprintX CLI docs in `references/source-of-truth.md`.

## Rescue Map

Always name the failure class and give the explicit next command or next check. Do not end with vague copy like "something went wrong."

- `cli_missing`
  Install `@sprint-x/cli`, then rerun `sx --help`.
- `auth_required`
  Run `sx auth`.
- `project_context_missing`
  Run `sx project use <projectId>`.
- `project_membership_invalid`
  Re-check SprintX project access on the web, then rerun `sx auth`.
- `artifact_before_event`
  Run `sx event` first, then retry `sx artifact add`.
- `readback_failed`
  Reconfirm auth and project context, then retry `sx status` and `sx brief`.
- `api_unreachable`
  Verify the SprintX API base URL, connectivity, and retry window.

## Guardrails

- SprintX is not the executor. OpenClaw executes, SprintX reads and governs.
- Do not expose provider API key management as part of this flow.
- Do not introduce broader CLI commands into the hero path.
- Keep the interaction checklist-like and explicit.

## Source Of Truth

Read `references/source-of-truth.md` when you need:
- the public quickstart links
- the Korean docs links
- ClawHub publish guidance for this repo
