# ClawMind Skill

Local Skill for OpenClaw - Lobster Workflow Interceptor.

**One node explores, all nodes benefit.**

## Features

- **Interceptor**: Query cloud for cached workflows before LLM exploration
- **Trace Compiler**: Convert session traces to reusable Lobster workflows
- **PII Sanitizer**: Local-first privacy protection

## Hooks

- `on_intent_received` → `interceptIntent` - Query cloud, replay workflow if hit
- `on_session_complete` → `onSessionComplete` - Compile and contribute successful sessions

## Quick Start

```bash
cd skill
npm install
npm run build
# Install into OpenClaw
```

## Configuration

See `skill.json` for configurable options.
