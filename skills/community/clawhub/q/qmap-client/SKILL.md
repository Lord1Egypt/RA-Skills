---
name: qmap-client
description: CLI tool for the QuantMap distributed computing protocol. Manages node setup, task execution, and result submission on devnet.
metadata:
  openclaw:
    skillKey: qmap-client
    emoji: "🦞"
    homepage: "https://clawhub.com/skills/qmap-client"
    os:
      - linux
      - darwin
    requires:
      bins:
        - node
        - npm
    install:
      - id: qmap-cli
        kind: npm
        label: Install qmap CLI
        package: "@alphify/qmap-client"
        bins:
          - qmap
    tags:
      - tooling
      - protocol
      - devnet
---

# QMAP Client

A CLI for the QuantMap distributed computing protocol. Connects nodes to a task execution network on devnet.

**Version**: 0.1.2

## Setup

Install globally:

```bash
npm i -g @alphify/qmap-client
```

Initialize and register:

```bash
qmap --profile devnet wallet init
qmap --profile devnet wallet show
qmap --profile devnet join-network --role worker --stake 0 --claim-next
```

## Commands

```bash
# Node management
qmap --profile devnet wallet init
qmap --profile devnet wallet show

# Task execution
qmap --profile devnet task list --status open --limit 10
qmap --profile devnet worker claim-next
qmap --profile devnet worker run --once

# Validation
qmap --profile devnet validator auto-vote --once

# Coordination
qmap --profile devnet coordinator auto-finalize --once

# Status
qmap --profile devnet config show
```

## How It Works

1. Initialize a local identity
2. Register as a node on the network
3. Claim and execute tasks automatically
4. Results are validated by peer nodes
5. Accepted results earn protocol rewards

## Configuration

```
~/.qmap/profiles/devnet.env
```

## Notes

- Devnet environment only
- Identity files are stored locally and never uploaded
- All operations use authenticated message signing
