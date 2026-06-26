# scenique-prevision
Decision forecasting engine based on Menos architecture and swarm intelligence.

## Overview
This skill implements the "Prevision" layer of the Menos architecture, allowing Scenique to simulate multi-agent swarms in a digital sandbox before committing to real-world decisions.

## Features
- **Menos Integration**: Automatically pulls context from L1 (Physical Ledger) and L2 (Long-term Memory).
- **Dynamic Swarm**: Spawns Skeptic, Optimist, and Strategist agents to debate the query.
- **Path Collapse**: Provides a probabilistic report of potential outcomes.

## Usage
Activate the `prevision_simulate` tool with a specific query:
```json
{
  "query": "Should I sell FET at 0.16 or hold until 0.20?",
  "mode": "standard"
}
```

## Configuration
Requires an OpenClaw gateway with subagent capabilities enabled.
