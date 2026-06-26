---
name: yuzhua-openclaw
description: Install, start, stop, and health-check Yuzhua (gesture + voice + OpenClaw gateway) with minimal manual setup.
---

# Yuzhua OpenClaw Skill

## Project Introduction

Yuzhua (驭爪) is a lightweight local gesture-driven AI conversation project.

- Open palm starts recording.
- Close hand stops recording and sends the request.
- Speech recognition, VAD, and TTS run locally.
- Conversation routing is connected through OpenClaw gateway.
- It is isolated from OpenClaw core runtime and does not modify OpenClaw main process behavior.

GitHub: https://github.com/juguangyuan520-dotcom/Yuzhua

## 项目简介（中文）

Yuzhua（驭爪）是一个轻量的本地手势驱动 AI 对话项目。

- 打开手掌开始录音。
- 合上手掌结束录音并发送请求。
- 语音识别、VAD、语音播报均在本地执行。
- 对话请求与回复通过 OpenClaw 网关完成对接。
- 与 OpenClaw 主运行链路隔离，不影响正在运行的 OpenClaw。

项目地址: https://github.com/juguangyuan520-dotcom/Yuzhua

## Purpose

Use this skill when the user wants to:
- install Yuzhua quickly
- start Yuzhua locally
- check whether Yuzhua and OpenClaw gateway are connected
- stop a running Yuzhua process

This skill is designed for local machines and keeps secrets in `.env`.

## Quick Commands

Run from this skill directory:

```bash
./scripts/install.sh
./scripts/start.sh
./scripts/health_check.sh
./scripts/stop.sh
```

## Paths And Environment

- `YUZHUA_HOME`: local Yuzhua project path (optional)
- `YUZHUA_REPO_URL`: repo to clone when missing (optional)

Defaults:
- `YUZHUA_HOME=~/.openclaw/workspace/apps/Yuzhua`
- `YUZHUA_REPO_URL=https://github.com/juguangyuan520-dotcom/Yuzhua.git`

## What The Scripts Do

1. `install.sh`
- clone or update Yuzhua source
- ensure `start.sh` exists and is executable
- create `.env` from `.env.example` when needed

2. `start.sh`
- run Yuzhua's own `start.sh`
- print resolved project path

3. `health_check.sh`
- query `http://127.0.0.1:8080/api/status`
- show transcriber/gateway/token/session status

4. `stop.sh`
- stop local process on port `8080`

## Notes

- Never commit `.env` or any real keys.
- For first run, users may still need to fill token values in `.env`.
- If Python dependency download fails, it is usually network/SSL/mirror related.
