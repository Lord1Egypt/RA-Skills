---
name: teamclaw-setup
description: Install, configure, validate, or troubleshoot the TeamClaw OpenClaw plugin for virtual software-team workflows. Use when users want TeamClaw setup help, controller or worker config snippets, on-demand process/docker/kubernetes workers, external worker registration, or safe first-run validation steps.
version: 1.0.0
metadata:
  openclaw:
    author: TeamClaws
    homepage: https://github.com/topcheer/teamclaw
    links:
      homepage: https://github.com/topcheer/teamclaw
      repository: https://github.com/topcheer/teamclaw
      documentation: https://github.com/topcheer/teamclaw/blob/main/INSTALL.md
      changelog: https://github.com/topcheer/teamclaw/releases
---

# TeamClaw Setup

Guide users to the smallest working TeamClaw installation first, then expand.

## Default workflow

1. Prefer the guided installer first:

   ```bash
   npx -y @teamclaws/teamclaw install
   ```

   The guided installer already applies `--dangerously-force-unsafe-install` for TeamClaw and defaults to an independent `teamclaw` agent/workspace.

   Advanced compatibility only:

   ```bash
   npx -y @teamclaws/teamclaw install --agent-mode main
   ```

   Use that only when the user explicitly wants the legacy shared-`main` layout.

2. Use manual plugin install only when the user wants direct control:

   ```bash
   openclaw plugins install --dangerously-force-unsafe-install @teamclaws/teamclaw
   ```

   If the user explicitly wants the ClawHub package path, use:

   ```bash
   openclaw plugins install --dangerously-force-unsafe-install clawhub:@teamclaws/teamclaw
   ```

3. Recommend `controller + process provisioning` for the first successful run unless the user explicitly needs external workers, Docker, or Kubernetes immediately.

4. Read `references/install-modes.md` before generating config. Pick the smallest matching topology and reuse the provided snippets.

5. Read `references/validation-checklist.md` before finishing. Always give the user:
   - one health-check command
   - one UI URL
   - one tiny smoke-test requirement
   - one or two likely failure checks for the chosen topology

## Installation guidance

- Start with a single host and `process` provisioning.
- Keep TeamClaw `taskTimeoutMs` large for real model runs.
- Keep OpenClaw `agents.defaults.timeoutSeconds` at least as large as the TeamClaw task window in seconds.
- For `docker` or `kubernetes`, require a reachable `workerProvisioningControllerUrl`.
- For `docker`, mention the published runtime image:

  ```text
  ghcr.io/topcheer/teamclaw-openclaw:latest
  ```

## What to produce

When helping a user, produce:

1. the exact install command
2. the minimal config snippet for the chosen topology
3. the startup command
4. the validation commands and first smoke-test task

Do not push users into distributed, Docker, or Kubernetes first unless they asked for it or already have the surrounding infrastructure ready.
