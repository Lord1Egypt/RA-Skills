# SolCore Memory System

Persistent, reflective memory for OpenClaw that transforms reactive AI into stateful, learning AI.

## What It Does

- **Stores interactions** with evaluation scoring (5 dimensions)
- **Detects patterns** in behavior (hesitation, chasing, discipline)
- **Retrieves context** relevant to current queries
- **Runs reflection** analysis on memory timelines
- **Links memories** across domains via edges

## Installation

```bash
# Install from ClawHub
openclaw skill install solcore-memory

# Or clone manually
git clone https://github.com/MichaelandSol/Solcore-persistent-memory-for-AI.git
openclaw skill link ./Solcore-persistent-memory-for-AI
```

## Configuration

Requires PostgreSQL database:

```yaml
# ~/.openclaw/config/openclaw.yaml
plugins:
  solcore-memory:
    database:
      host: localhost
      port: 5432
      name: solcore
      user: solcore
      password: your_password
    webhook:
      port: 5003
```

## Usage

The plugin automatically:
1. Stores every interaction with metadata
2. Evaluates on 5 dimensions (result, structure, timing, strength, alignment)
3. Extracts entities (stocks, people, concepts)
4. Retrieves relevant context for queries
5. Detects behavioral patterns over time

## Tools Provided

- `solcore_store_memory` - Store interaction with scoring
- `solcore_get_context` - Retrieve relevant memories
- `solcore_reflect` - Run reflection analysis

## GitHub

https://github.com/MichaelandSol/Solcore-persistent-memory-for-AI
