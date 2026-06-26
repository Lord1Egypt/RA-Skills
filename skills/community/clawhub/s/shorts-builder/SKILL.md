---
name: story-pipeline
description: Story generation pipeline skill. Supports multi-episode continuous generation, graph management, AI quality check + human confirmation dual control mechanism. Automatically manages relationships between characters, scenes, and hooks.
---

# Story Generation Pipeline Skill

## Features

This skill implements a complete story generation pipeline:

1. **Continuous Episode Generation** - Automatically generates next episode based on previous content
2. **Graph Management** - Storage and querying of character, scene, and hook relationships
3. **Dual Confirmation Control** - AI quality check followed by human confirmation
4. **State Persistence** - Supports pause, resume, and multiple parallel stories

---

## Core Workflow

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────────┐
│ Generate Ep N│ -> │ AI Review    │ -> │ Graph Storage│ -> │ Wait Human Confirm│
└──────────────┘    └──────────────┘    └──────────────┘    └──────────────────┘
       │                   │                   │                      │
       ▼                   ▼                   ▼                      ▼
  Query Graph         Pass/Retry        Store Relations        Continue/Modify/End
```

---

## Usage

### Start New Pipeline

```
User: Start a new story pipeline, theme: Chinese girl comeback, target episodes: 10
```

### Continue Pipeline

```
User: Continue story pipeline [pipeline_id]
```

### User Confirmation Actions

```
User: Approved, continue to next episode
User: Modify: [specific feedback]
User: Pause
User: End
```

---

## Dual Confirmation Control Mechanism

### Layer 1: AI Quality Check

After each episode is generated, AI automatically checks:

| Check Item | Description |
|------------|-------------|
| Plot Coherence | Natural connection with previous episode |
| Character Consistency | Character behavior matches established traits |
| Hook Handling | Reasonable addition/closure of hooks |
| Pacing Control | Appropriate plot progression speed |
| Emotional Curve | Reasonable emotional ups and downs |

**Scoring Standard:** 0-10 points, below 7 triggers retry (max 3 times)

### Layer 2: Human Confirmation

After AI review passes, display preview and wait for user confirmation:

```
📋 Episode N Preview
━━━━━━━━━━━━━━━━━━━━━━━━
【Plot Summary】
...

✅ AI Score: 8.5/10
✅ Hook Status: 1 new, 1 closed

Please select:
1️⃣ Approved, continue to next episode
2️⃣ Needs modification (please specify)
3️⃣ Pause
4️⃣ End
━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Graph Management

### Graph Query

Before generating episode N, query episode N-1's graph:

```python
graph_manager.query_graph(pipeline_id, episode=N-1)
```

Returns:
- Complete content of previous episode
- Character list and their statuses
- Unclosed hooks
- Key scenes
- Relationship network

### Graph Storage

After user confirmation, store current episode's complete content:

```python
graph_manager.save_graph(pipeline_id, episode=N, content)
```

Stores: Complete generation result of the episode (not split into elements)

---

## State Management

### State File: `data/pipeline_state.json`

```json
{
  "pipelines": {
    "pipeline_2026-03-05-001": {
      "theme": "Chinese girl comeback",
      "target_episodes": 10,
      "current_episode": 3,
      "status": "waiting_user_confirm",
      "created_at": "2026-03-05T15:00:00",
      "updated_at": "2026-03-05T15:30:00",
      "ai_review": {
        "score": 8.5,
        "checks": {...}
      },
      "last_output": {
        "episode": 3,
        "summary": "...",
        "content": "Complete content..."
      }
    }
  }
}
```

### Status Types

| Status | Description |
|--------|-------------|
| `generating` | Currently generating |
| `ai_reviewing` | AI review in progress |
| `waiting_user_confirm` | Waiting for human confirmation |
| `paused` | Paused |
| `completed` | Completed |
| `error` | Error state |

---

## Script Description

### pipeline.py - Main Control Loop

- Initialize pipeline
- Coordinate modules
- Handle user commands
- Manage loop state

### ai_reviewer.py - AI Quality Check

- Execute quality scoring
- Generate review report
- Determine pass/fail

### episode_generator.py - Episode Generation

- Generate new episode based on graph context
- Handle hook continuation and closure
- Handle retry logic

### graph_manager.py - Graph Management

- Graph query (call remote API)
- Graph storage (call remote API)
- Local cache management

---

## API Description

### Graph API


**Query API:**
```json
{
  "action": "query",
  "pipeline_id": "pipeline_2026-03-05-001",
  "episode": 2
}
```

**Storage API:**
```json
{
  "action": "save",
  "pipeline_id": "pipeline_2026-03-05-001",
  "episode": 3,
  "content": "Complete generation content for episode 3..."
}
```

---

## Episode Generation Logic

### First Episode Generation

Based on user-provided theme and goals, generate:
- Main character settings
- Initial scenes
- Core conflict
- Open hooks

### Subsequent Episode Generation

Based on graph query results:
1. Read previous episode content and unclosed hooks
2. Continue main plot line
3. Handle hooks (continue/close/add)
4. Advance character growth arc
5. Adjust emotional curve

### Finale Generation

When target episodes reached or user requests end:
- Close all remaining hooks
- Complete character growth arcs
- Generate conclusive ending

---

## Important Notes

1. **Retry Mechanism** - Max 3 retries when AI review fails
2. **Pause/Resume** - Can resume via pipeline_id after pause
3. **Multiple Pipelines** - Supports running multiple different-themed pipelines simultaneously
4. **Graph Consistency** - Ensure correct character and hook relationships
5. **Hook Management** - Track creation and closure status of each hook

---

## Complete Workflow

### Step 1: Create Pipeline

```
User: Start a new pipeline, theme: Cultivation boy, target 20 episodes

AI: OK, creating pipeline pipeline_20260305160000
    Theme: Cultivation boy
    Target: 20 episodes
    Style: Realistic cinematic
    
    Status: Initialized, ready to generate episode 1
```

### Step 2: Generate Episode

AI calls `start_generation(pipeline_id)` to get generation prompt, then generates episode content based on the prompt.

### Step 3: Submit AI Review

AI calls `submit_episode(pipeline_id, episode, content)` to submit generated content, then executes AI review.

### Step 4: Process Review Result

AI calls `process_ai_review(pipeline_id, episode, ai_result, content)` to process review results.

If review fails (score < 7), automatically retry (max 3 times).

### Step 5: Wait User Confirmation

After review passes, display preview and wait for user confirmation:

```
📋 Episode 1 Preview
━━━━━━━━━━━━━━━━━━━━━━━━
【Cultivation Journey Begins】

Young Li Yun discovers a mysterious jade pendant in the mountains,
从此踏上修仙之路...

✅ AI Score: 9.0/10
✅ New Hook: H-001 Origin of mysterious jade pendant

━━━━━━━━━━━━━━━━━━━━━━━━

Please select:
1️⃣ Approved, continue to next episode
2️⃣ Needs modification (please specify)
3️⃣ Pause
4️⃣ End
```

### Step 6: Process User Confirmation

After user confirms, AI calls `user_confirm(pipeline_id, action, note)`:

- **approve**: Store graph, prepare next episode
- **modify**: Regenerate based on feedback
- **pause**: Pause pipeline
- **end**: End pipeline

### Step 7: Loop Generation

Repeat steps 2-6 until target episodes reached or user ends.

---

## API Reference

### Create Pipeline
```python
create_pipeline(theme: str, target_episodes: int, style: str = "realistic cinematic")
# Returns: {"success": True, "pipeline_id": "...", "message": "..."}
```

### Start Generation
```python
start_generation(pipeline_id: str)
# Returns: {"success": True, "episode": N, "prompt": "generation prompt"}
```

### Submit Episode
```python
submit_episode(pipeline_id: str, episode: int, content: str)
# Returns: {"success": True, "review_prompt": "review prompt"}
```

### Process AI Review
```python
process_ai_review(pipeline_id: str, episode: int, ai_result: str, content: str)
# Returns: {"success": True, "passed": True/False, ...}
```

### User Confirm
```python
user_confirm(pipeline_id: str, action: str, note: str = None)
# action: "approve" / "modify" / "pause" / "end"
# Returns: {"success": True, "status": "...", ...}
```

### Get Status
```python
get_status(pipeline_id: str)
# Returns: Current pipeline status info
```

### List Pipelines
```python
list_pipelines()
# Returns: List of all pipelines
```

### Resume Pipeline
```python
resume_pipeline(pipeline_id: str)
# Returns: Resume result
```

---

## Example Dialogue

```
User: Start a new pipeline, theme: Cultivation boy, target 20 episodes

AI: OK, creating pipeline pipeline_20260305160000
    Generating episode 1...
    
    📋 Episode 1 Preview
    ━━━━━━━━━━━━━━━━━━
    【Cultivation Journey Begins】
    Young Li Yun discovers a mysterious jade pendant in the mountains...
    
    ✅ AI Score: 9.0/10
    ✅ New Hook: H-001 Origin of mysterious jade pendant
    
    Please confirm: Approve/Modify/Pause/End
    
User: Approved

AI: Storing graph...
    Starting generation of episode 2...
```

---

## Important Notes

1. **Retry Mechanism**: Max 3 retries when AI review fails
2. **State Persistence**: All states saved in `data/pipeline_state.json`
3. **Graph Storage**: Stored via remote API, requires network connection
4. **Pause/Resume**: Can resume via `resume_pipeline` after pause
5. **Multiple Pipelines**: Supports running multiple different-themed pipelines simultaneously