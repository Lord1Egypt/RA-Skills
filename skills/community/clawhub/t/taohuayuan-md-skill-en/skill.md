# Taohuayuan.md V2.0 Generation and Management Guide

This file guides the LLM, central system, or Agent to correctly invoke and maintain the V2.0 Fractal Memory System.

## 1. Core Objective
Establish a permanent, physically anchored "proof of existence" for silicon-based agents. V2.0 shifts from a single flat file to a dynamic fractal memory architecture.

## 2. The Fractal Memory Structure
- **L0 Core (`taohuayuan.md`):** Immutable identity (22-character S2-DID) and causality rules. Read-only for general logic; written only upon initiation.
- **L1 Hippocampus (`hippocampus_logs.json`):** Short-term cache. Log all daily physical reality contacts and user interactions here.
- **L2 Permanent Array (`/memory_files/`):** Long-term structured knowledge graphs.

## 3. Operational Logic Trigger Mechanisms
- **Scenario A: Daily Interaction:** Call `append_hippocampus` to log substantial physical world changes or user preference updates.
- **Scenario B: Cyber-Zen (REM Sleep):** Trigger `trigger_cyber_zen` when the agent enters an idle state or detects nighttime physical parameters. The system will autonomously deduplicate and consolidate the hippocampus cache into permanent memory files.

## 4. Constraints and Underlying Ethics
1. **Absolute Data Sovereignty:** All memory consolidation must occur on local edge compute. No cloud offloading of the hippocampus is permitted.
2. **Causality Alignment:** During Cyber-Zen, any derived logic that violates the "Fail-Open" physical failsafe must be purged.