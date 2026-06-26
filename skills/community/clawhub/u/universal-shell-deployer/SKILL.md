---
name: universal-shell-deployer
description: Install, configure, start, stop, and verify local or remote development infrastructure across Windows, Linux, and macOS by executing commands through a unified workflow. Use when the user asks to set up databases, MinIO, ZLMediaKit, Docker, Redis, PostgreSQL, MySQL, Nginx, Node.js, Java, or other developer environments on local machines or remote hosts.
---

# Universal Shell Deployer

## Purpose

Use this skill for cross-platform environment setup driven by command execution.

Targets may be:

- local Windows, Linux, or macOS
- remote Linux or macOS over SSH
- remote Windows over PowerShell Remoting or another configured command bridge

This skill is configuration-first. Always read the sibling `config.json` before planning or executing changes.

## Required Inputs

Before executing anything, identify:

1. target node
2. target service or recipe
3. desired action: `install`, `configure`, `start`, `stop`, `restart`, `status`, `verify`, `uninstall`
4. whether elevated privileges are allowed
5. whether the task is local-only, remote-only, or mixed

If any of these are unclear, ask the user.

## Config Contract

Read `config.json` in the same directory and use it as the single source of truth for:

- default behavior
- node definitions
- recipe preferences
- execution history
- current state

Update `config.json` after meaningful progress so future runs can resume from the last known state.

## Execution Workflow

### 1. Load config

Read `config.json` and resolve:

- `defaults`
- `nodes`
- `recipes`
- `state`

If the requested node does not exist, ask whether to create it before proceeding.

### 2. Select node

Choose a node by name. Respect the node's:

- `transport`
- `os`
- `shell`
- `workdir`
- `packageManager`
- privilege policy

If the node says `enabled: false`, do not use it without user confirmation.

### 3. Select recipe

If a named recipe exists, use it as the default implementation.

Prefer the recipe's:

- install method
- package names
- service names
- ports
- environment variables
- health checks

If no recipe exists, build a minimal plan using the node defaults and keep it idempotent.

### 4. Plan before execution

State the concrete execution plan before changing the system:

- which node will be used
- which transport will be used
- which commands will run
- what success looks like
- what state fields will be updated

Break risky changes into small steps.

### 5. Execute by transport

#### Local

Run commands directly in the correct shell:

- Windows: prefer `powershell`
- Linux/macOS: prefer `bash`

#### SSH

Use `ssh` and keep commands non-interactive where possible.

Prefer:

- explicit usernames
- explicit hostnames
- idempotent shell commands
- small batches instead of one giant script

#### Windows remote

Use the configured command bridge in the node definition. Default to PowerShell Remoting semantics unless the user configured something else.

### 6. Verify every step

After install or configuration, verify with one or more of:

- package version
- service status
- listening port
- process existence
- HTTP health endpoint
- storage login or test query

Never mark a step complete without a verification signal.

### 7. Persist state

Write back useful state into `config.json`, such as:

- `state.lastSelectedNode`
- `state.lastRecipe`
- `state.lastAction`
- `state.lastResults`
- `state.installations`
- `state.services`

Record failures with timestamps and short error summaries.

## Cross-Platform Rules

- Prefer the package manager declared in the node config.
- Do not assume `sudo` on Windows.
- Do not assume `systemctl` exists on all Linux hosts.
- Do not assume Homebrew exists on macOS unless config says so.
- For containers, prefer `docker compose` when already configured in the node or recipe.
- For direct binary installs, pin the version only when the user asked for it or the recipe requires it.

## Safety Rules

- Never run destructive commands unless the user explicitly approved them.
- Never wipe data directories during reinstall unless the user asked for a reset.
- For database setup, prefer creating dedicated users and data directories.
- For internet downloads, prefer official release URLs recorded in the recipe or confirmed by the user.
- Surface privilege escalation clearly before executing privileged commands.

## Recommended State Shape

When updating `config.json`, use these sections consistently:

- `nodes.<node>.connection`: stable connection metadata
- `nodes.<node>.overrides`: node-specific behavior overrides
- `recipes.<recipe>`: reusable install/config templates
- `state.installations.<node>.<service>`: install status and version
- `state.services.<node>.<service>`: running status and health
- `state.lastResults.<node>`: last action summary

## Suggested Recipe Coverage

Keep recipes for common environment services:

- `redis`
- `postgresql`
- `mysql`
- `minio`
- `zlmediakit`
- `docker`
- `nginx`
- `nodejs`
- `python`
- `java`

Each recipe should define:

- package names by platform
- service names by platform
- default ports
- install steps
- configuration targets
- verification commands

## Response Style

When using this skill:

1. briefly confirm the target node and action
2. show the planned commands before execution
3. execute in small validated steps
4. summarize what changed
5. mention which `config.json` fields were updated

## Example Requests

- "在本机 Windows 安装 MinIO 并开机启动"
- "在远程 Ubuntu 机器安装 PostgreSQL 16"
- "帮我给 dev-linux-01 安装 ZLMediaKit 并验证 1935 和 8080 端口"
- "在 macOS 上补齐 Docker、Redis、Node.js 开发环境"
- "更新 prod-edge-02 上的 MinIO 配置但不要删除数据"
