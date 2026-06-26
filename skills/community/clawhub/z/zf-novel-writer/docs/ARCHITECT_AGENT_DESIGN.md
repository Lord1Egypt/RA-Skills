# Architect Agent Design / Architect Agent 设计方案

## Overview / 概述

Integrates chapter planning into the Orchestrator. The Orchestrator acts as Architect Agent, automatically planning chapter structure before generation.

将章节规划能力整合到 Orchestrator 中，由 Orchestrator 扮演 Architect Agent 角色。

## Core Concept / 核心思想

**Orchestrator = Architect + Coordinator**

- **Architect:** Analyze current state, plan chapter structure
- **Coordinator:** Coordinate Writer/Quality Agent execution

## Workflow / 工作流程

```
Step 1: Plan chapter (Orchestrator/Architect)
    ↓
Step 2: Generate prompt (plan + pending_setups)
    ↓
Step 3: Spawn Writer Agent (sessions_spawn)
    ↓
Step 4: Spawn Quality Agent (sessions_spawn)
    ↓
Step 5: Archive (canon_bible + Truth Files)
    ↓
Step 6: Next chapter
```

## Chapter Plan JSON Format / 章节规划格式

```json
{
  "version": "1.0",
  "chapter": 3,
  "book": "{BOOK_NAME}",
  "planning": {
    "scenes": [
      {
        "id": 1,
        "title": "Scene title",
        "content": "Brief scene description",
        "location": "Location",
        "characters": ["{PROTAGONIST}", "NPC"],
        "emotional_goal": "Emotion",
        "word_count_estimate": 800
      }
    ],
    "key_events": [
      {"type": "setup", "description": "Setup description"},
      {"type": "payoff", "description": "Payoff description"}
    ],
    "emotional_arc": {
      "protagonist": {"start": "Start emotion", "end": "End emotion"}
    },
    "pacing": {"opening": "Tension", "development": "Build", "climax": "Peak", "ending": "Hook"},
    "word_count_target": 3200
  }
}
```

## Truth Files Read / 读取的 Truth Files

| File | Purpose |
|------|---------|
| `emotional_arcs.json` | Character emotional states |
| `character_matrix.json` | Character relationships |
| `subplot_board.json` | Subplot progress |
| `canon_bible.json` | Core settings, pending_setups |
| `summaries_json/chapter_N.json` | Previous chapter summary |
| `story_outline.xlsx` | Full book plan (current chapter positioning) |

## Scene Decomposition / 场景分解

- 2500-3000 words → 3 scenes
- 3000-3500 words → 4 scenes
- 3500-4000 words → 5 scenes

### Structure / 结构
- Scene 1 (~20%): Establish tone, connect to previous chapter
- Scenes 2-3 (~50%): Main events, emotional arc changes
- Scene 4 (~20%): Core conflict / payoff
- Scene 5 (~10%): Summary + hook for next chapter

## Recommended Approach / 推荐方案

**Plan A (Gradual):** Add planning capability to Orchestrator directly. No additional Agent needed.

---

*Last updated: 2026-03-31*
