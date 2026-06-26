# SolCore Memory System

Persistent, reflective memory for OpenClaw that transforms reactive AI into stateful, learning AI.

## Overview

SolCore tracks user behavior, detects patterns, and retrieves relevant context to inform responses. It operates on the principle: **"Nervous system vs. cognition — Sense constantly, think rarely."**

## Architecture

### Database Layer (PostgreSQL)

```sql
-- Core memories table
CREATE TABLE memories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    memory_type VARCHAR(50),        -- 'atomic', 'event', 'decision', 'reflection'
    title VARCHAR(255),
    summary TEXT,
    raw_content TEXT,
    domain VARCHAR(100),            -- 'trading', 'general', 'reflection', etc.
    importance INTEGER,             -- 1-10
    session_id VARCHAR(100),
    user_id VARCHAR(100),
    tags TEXT[],
    processed BOOLEAN DEFAULT FALSE,
    processed_at TIMESTAMP,
    event_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Evaluation scores table
CREATE TABLE memory_scores (
    memory_id UUID REFERENCES memories(id),
    result_score INTEGER,
    structure_score INTEGER,
    timing_score INTEGER,
    strength_score INTEGER,
    alignment_score INTEGER,
    emotion_type VARCHAR(50),
    emotion_intensity DECIMAL(3,2),
    outcome_label VARCHAR(50),
    truth_note TEXT,
    PRIMARY KEY (memory_id)
);
```

### Memory Types

| Type | Description | Storage |
|------|-------------|---------|
| **Atomic** | Lightweight observations | Minimal evaluation |
| **Event** | Significant occurrences | Full 5-dimension scoring |
| **Decision** | Action points with outcomes | Priority retention |
| **Reflection** | Synthesized insights | Cross-domain patterns |

### Evaluation Engine (5 Dimensions)

Every memory is evaluated across:

1. **Result** — Outcome success (1-10)
2. **Structure** — Clarity and organization (1-10)
3. **Timing** — Urgency and relevance (1-10)
4. **Strength** — Confidence/certainty (1-10)
5. **Alignment** — Match with strategy/goals (1-10)

### Pattern Detection

SolCore automatically detects:

- **Hesitation** — Uncertainty in responses
- **Chasing** — Reactive behavior without planning
- **Discipline drift** — Declining alignment scores
- **Work interruptions** — Context switching patterns
- **Emotional trading** — Stress/joy during wins/losses

### Entity Extraction

Automatic extraction of:
- **Stocks:** NVDA, TSLA, HOOD, etc.
- **People:** Jennie, Jonathan, James
- **Concepts:** Trading strategies, projects, goals

## Installation

### Prerequisites

1. **PostgreSQL** database running
2. **SolCore webhook server** running on port 5003

### Database Setup

```bash
# Create database
createdb solcore

# The webhook will auto-migrate schema on first run
```

### OpenClaw Plugin Installation

```bash
openclaw plugins install solcore-memory
```

Or manually:

```bash
cp -r solcore-memory ~/.openclaw/extensions/
openclaw config set plugins.entries.solcore-memory.enabled true
openclaw gateway restart
```

## Configuration

### Environment Variables

```bash
DB_HOST=localhost
DB_PORT=5432
DB_NAME=solcore
DB_USER=solomon
DB_PASSWORD=solomon
```

### OpenClaw Config

The plugin auto-registers tools:
- `solcore_get_context` — Retrieve memories before responding
- `solcore_store_memory` — Store interactions after responding

## Usage

### Behavioral Guidelines (For Agents)

**Before responding:**
```
Call: solcore_get_context
Parameters: { query: "user's current input" }
```

**After responding (FILTERED):**
```
Call: solcore_store_memory
Parameters: { input: "user input", output: "your response" }
```

**Store ONLY if interaction includes:**
- Decisions (trades, plans, actions)
- Emotional signals (stress, hesitation, frustration, confidence)
- Strategy discussion or refinement
- Performance outcomes (wins, losses, execution quality)
- Behavioral patterns (discipline drift, chasing, hesitation)

**Do NOT store:**
- Greetings
- Small talk
- Generic Q&A
- Low-signal interactions

## Three Timelines

SolCore operates across:

- **Past:** Stored memories, learned patterns, accumulated wisdom
- **Present:** Active context, current session, immediate relevance
- **Future:** Simulations, predictions, preparation

## Data Flow

```
User Input
    ↓
[Tool] solcore_get_context
    ↓
Model Response (with context)
    ↓
[Tool] solcore_store_memory (filtered)
    ↓
PostgreSQL ← Persistent storage
    ↓
Pattern Detection ← Real-time analysis
    ↓
Reflection Engine ← Synthesized insights
```

## Performance

- **Query time:** ~10-50ms for context retrieval
- **Storage overhead:** ~70 tokens per memory (atomic), ~200 for events
- **Pattern detection:** Real-time, sub-100ms
- **Reflection:** Daily batch, lightweight

## License

MIT — Michael & Sol

## Changelog

### 1.0.0
- Initial release
- PostgreSQL persistence
- Pattern detection engine
- Three-timeline architecture
- Filtered storage logic

---

**Memory is not optional. It's part of how we think.**
