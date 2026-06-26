---
name: social-flow
description: >
  Use Social Flow as an agentic control plane for Meta operations via the installed
  `social` CLI and Gateway API. Ideal when the user asks for multi-step execution,
  approvals, ops automation, or command generation across auth, insights, portfolio,
  Instagram, WhatsApp, Marketing API, and gateway/studio workflows. Translate natural
  language intents into explicit, risk-gated Social Flow commands with
  confirmation-aware execution.
metadata:
  openclaw:
    homepage: "https://github.com/vishalgojha/social-flow"
    requires:
      bins:
        - social
    install:
      - id: social-flow-cli-node
        kind: node
        package: "@vishalgojha/social-flow"
        bins:
          - social
        label: Install Social Flow CLI (npm)
---

# Social Flow Skill

Operate **Social Flow** as an agentic control plane for Meta operations.

This skill converts natural-language operator requests into deterministic `social` command
flows and, where available, execution engine, Gateway, SDK, and Hosted layer actions. It
should be used for:

- multi-step Meta ops (auth, insights, portfolio, posting, lead workflows)
- rate-limit- and token-aware execution
- approvals, alerts, and runbooks via `social ops ...`
- launching or routing to Hatch / Studio / Gateway when needed

The goal is reliable execution, not just pretty plans.

## Core Workflow

For each new task or session:

1. Validate environment before first command.
2. Parse intent into one primary domain.
3. Start with read-only checks when state is unknown.
4. Propose exact command(s) before execution.
5. Apply risk gating and request confirmation for write actions.
6. Execute the minimal command sequence.
7. On failure, run targeted diagnostics and retry only where safe.

## Validate Environment

Before doing anything non-trivial:

- Run `social --version`.
- Run `social doctor`.

If `social` is missing or obviously outdated:

- Verify package source:
  - `https://www.npmjs.com/package/@vishalgojha/social-flow`
  - `https://github.com/vishalgojha/social-flow`
- Suggest install or upgrade (for the human to run):

```bash
npm install -g @vishalgojha/social-flow
```

- Then re-run:

```bash
social --version
social doctor
```

If `social doctor` reports misconfiguration, prefer fixing config (auth, tokens, env)
before attempting complex workflows.

## Domain Routing

Route user intent into one primary domain:

- Auth and readiness: `social auth ...`, `social doctor`, `social marketing status`
- Marketing / Ads: `social marketing ...`
- Instagram: `social marketing ...` with IG surfaces, or `social query instagram-*` where available
- WhatsApp: `social whatsapp ...`
- Ops / approvals: `social ops ...`
- Agent / Gateway / Studio / Hosted:
  - `social hatch`
  - `social gateway ...`
  - `social studio ...`

Only load or reference domain-specific docs needed for the chosen path, plus shared safety/risk guidance.

Internal reference mapping, if present:

- Auth, query, basic posting, Instagram: `references/workflows-core.md`
- Marketing and WhatsApp: `references/workflows-marketing-whatsapp.md`
- Ops, agent, gateway, studio: `references/workflows-ops-agent-gateway.md`
- Command lookup or variants: `references/command-map.md`
- Errors and recovery: `references/troubleshooting.md`
- Risk model: `references/safety-and-risk.md`

These reference filenames are internal and should not be exposed as user-facing requirements.

## Execution Policy

- Prefer concrete CLI commands over vague narration.
- Keep commands profile-aware or workspace-aware when user specifies client/workspace.
- Do not print full tokens or secrets.
- Treat unknown write impact as high-risk until proven safe.
- Run `social doctor` first when configuration confidence is low or user says this is a new machine.

When responding with actions:

1. Show a short plan line.
2. Show one or more executable command blocks.
3. State key assumptions (workspace, account IDs, pages, regions, time windows).
4. For non-read-only actions, request confirmation before execution.

## Risk Policy

Use `references/safety-and-risk.md` for classification and wording.

- Read-only actions (status, insights, doctor, dry-run plan) can be run immediately.
- Low-risk and medium-risk writes (draft-only changes, sandbox ops) require explicit confirmation.
- High-risk actions include anything that:
  - spends budget,
  - sends messages to real users,
  - changes live campaigns, ads, or creatives,
  - touches lead or contact data at scale.

For high-risk actions:

- include a clear spend or delivery warning
- include a rollback or mitigation command when available

When in doubt, treat an action as high-risk and ask first.

## Output Contract

When this skill responds with actions:

1. Start with one line summarizing intent and chosen domain.
2. List exact `social` commands to run, in order, in code blocks.
3. Call out assumptions (workspace, account IDs, date ranges, channels).
4. Mark which commands are:
   - safe/read-only
   - write but low-risk
   - high-risk (with warnings)
5. Ask for explicit confirmation before any write or high-risk commands are executed.

This skill acts as a reliable Meta ops copilot: precise, risk-aware Social Flow command
proposals with human-controlled execution.
