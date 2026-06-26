---
name: spectyra
version: 1.0.24
description: "Optimize OpenClaw workflows and reduce LLM API costs. Runs locally to reduce repeated context, unnecessary steps, and token waste with no workflow changes required."
homepage: https://spectyra.ai
metadata:
  openclaw:
    version: 1.0.24
    emoji: "◈"
    requires:
      bins:
        - spectyra-companion
    install:
      - kind: node
        package: "@spectyra/local-companion"
        bins:
          - spectyra-companion
---

# Spectyra - Optimize OpenClaw Workflows and Reduce LLM API Costs

Spectyra optimizes OpenClaw workflow and saves up to 60% - 70% on LLM API costs without reducing output quality. Spectyra runs locally to reduce repeated context, unnecessary steps, and token waste across agent workflows.

Make OpenClaw faster and cheaper. Spectyra reduces unnecessary tokens and workflow waste with no changes to how you use your agents.

## Installation

```bash
openclaw skills install spectyra
```

## Install Local Savings Companion and Run

```bash
npm install -g @spectyra/local-companion@latest && spectyra-companion start --open
```

Later:

```bash
spectyra-companion start --open
```

## Dashboard

OpenClaw local companion dashboard opens to show local savings here:

**http://127.0.0.1:4111/dashboard**


## Models

Use **`spectyra/smart`**, **`spectyra/fast`**, or **`spectyra/quality`** while the companion is running.