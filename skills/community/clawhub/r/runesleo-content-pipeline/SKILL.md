---
name: Content Pipeline
version: 1.0.0
description: |
  4-stage content pipeline orchestrator: Research -> Ideate -> Write -> Queue.
  Give it a topic, it researches existing discussions, generates hook angles,
  writes a draft, and queues it for review. Inspired by @shannholmberg's
  4-Agent content system (Research -> Ideate -> Write -> Orchestrate).
  Designed for creators who build in public and want systematic content production.
when_to_use: when creating original content that needs research, angle selection, and drafting from scratch
trigger: /pipeline
languages: all
attribution: Inspired by @shannholmberg's 4-Agent content system. Pipeline architecture is original.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - Agent
  - AskUserQuestion
---

# Content Pipeline Orchestrator

> **One command, from topic to review-ready draft.**
> Research -> Ideate -> Write -> Queue

## When to use vs. not

**Use pipeline** (original content that needs research):
- Writing from scratch on a topic you haven't deeply explored
- Need to survey existing discussion, find data, pick an angle
- Example: "write about the impact of MoE on local inference" / "year-end market review"

**Don't use pipeline** (already have material):
- Quoting someone else's post -> just write directly
- Replying/commenting -> just write directly
- Polishing an existing draft -> just edit directly
- These scenarios waste 4-5x tokens through the pipeline with zero benefit

## File locations

Configure these paths for your project:

| File | Purpose |
|------|---------|
| `./content-queue.json` | Idea lifecycle state |
| `./research/` | Research results (by date + slug) |

## Commands

Parse user input, match first hit:

| Input | Command | Action |
|-------|---------|--------|
| `/pipeline <topic>` | **run** | Full pipeline: research -> ideate -> write -> queue |
| `/pipeline url <url>` | **url** | Extract from URL -> ideate -> write -> queue |
| `/pipeline seed <idea>` | **seed** | Add raw idea to queue as seed |
| `/pipeline status` | **status** | Show queue grouped by status |
| `/pipeline review <id>` | **review** | Show a draft for review |
| `/pipeline approve <id>` | **approve** | Mark as approved |
| `/pipeline adapt <id> <platform>` | **adapt** | Generate platform variant |
| `/pipeline publish <id>` | **publish** | Mark as published + timestamp |
| `/pipeline clean` | **clean** | Archive items published 30+ days ago |

---

## Queue data model

**File**: `./content-queue.json`

```json
{
  "ideas": [
    {
      "id": 1,
      "topic": "AI Agent end-to-end automation",
      "status": "drafted",
      "platform": "twitter",
      "created": "2026-03-03T15:00:00Z",
      "updated": "2026-03-03T15:05:00Z",
      "research_file": "research/20260303-ai-agent-automation.md",
      "hook_angle": "Builder perspective: Writing is easy, Research is the bottleneck",
      "draft": "This person built a full...",
      "variants": {},
      "source_url": null,
      "feedback": [],
      "published": null
    }
  ],
  "next_id": 2
}
```

**Status flow**: `seed -> researched -> drafted -> approved -> published -> archived`

### Queue read/write rules

1. **Read**: Read `./content-queue.json`
2. **Write**: Write back complete JSON (single-user, no concurrency issue)
3. **ID assignment**: Use `next_id`, increment after write
4. **Timestamps**: ISO 8601 with timezone

---

## Command details

### /pipeline <topic> -- Full Pipeline

**Input**: topic (keywords or short phrase)

#### Stage 1: Research

1. Search for existing discussion on the topic using available search tools:
   - Twitter/X search for relevant posts and threads
   - Web search for articles and data
   - Any domain-specific sources you have access to
2. Compile findings into a research file:
   ```
   ./research/YYYYMMDD-{slug}.md
   ```
   slug = topic keywords, lowercase with hyphens, max 30 chars

**Research file format**:
```markdown
# Research: {topic}
**Date**: YYYY-MM-DD
**Sources**: [list search methods used]

## Key findings
- [Finding 1 + source attribution]
- [Finding 2 + data/numbers]
- [Finding 3 + opposing viewpoint]

## Notable posts/articles
1. @user1 (N likes): "Core point summary"
2. @user2 (N likes): "Core point summary"

## Data points
- [Specific numbers, comparisons, statistics]

## Opposing viewpoints
- [Contrarian takes, if any]

## Source links
- [List of original URLs]
```

#### Stage 2: Ideate

1. Read the research file
2. Generate 3 hook angles based on the research:

**Angle generation prompt** (adapt for your LLM of choice):
```
You are a content strategist. Based on the following research, generate 3 hook angles for a post.

Research:
{research file content}

Requirements:
1. Each angle includes:
   - Hook type (contrast / counterintuitive / data-driven / story / question)
   - Core thesis (one sentence)
   - Key supporting points (2-3)
   - Estimated virality score (1-5)
2. Match the creator's voice and domain expertise
3. Avoid: AI cliches, marketing speak, listicle format

Output as JSON array:
[{"type": "contrast", "thesis": "...", "supports": ["...", "..."], "score": 4}, ...]
```

3. Select the highest-scored angle
4. If multiple angles tie, present options for user to choose

#### Stage 3: Write

1. Write the draft using the selected hook angle + research data points
2. **Content format routing**:
   - Content <= 280 chars -> short post (tweet)
   - 280-2000 chars -> long post (thread)
   - > 2000 chars -> article
3. Apply your preferred writing style/voice (integrate with a style skill if you have one)
4. Verify all claims have source attribution from the research

#### Stage 4: Queue

1. Read content-queue.json
2. Create new entry:
   - `status`: "drafted"
   - `platform`: target platform
   - `research_file`: relative path
   - `hook_angle`: selected angle description
   - `draft`: written text
3. Write back content-queue.json
4. Output confirmation:
   ```
   Pipeline complete -- queued #<id>
   Topic: <topic>
   Hook: <angle summary>
   Draft: <first 80 chars>...
   Format: short / long / article
   Use /pipeline review <id> to see full content
   ```

---

### /pipeline url <url> -- From URL input

1. Fetch the URL content using available tools
2. Extract core arguments and data points
3. Skip Stage 1 (use extracted content as research)
4. Continue to Stage 2 (ideate) -> Stage 3 (write) -> Stage 4 (queue)
5. Record `source_url` in the entry

---

### /pipeline seed <idea> -- Add raw seed

1. Create queue entry:
   - `status`: "seed"
   - `topic`: the idea text
   - `draft`: null (seeds have no draft yet)
2. Output: `Seed added to queue #<id>`

Seeds are raw ideas waiting to be developed. Run `/pipeline <topic>` later to expand a seed through the full pipeline.

---

### /pipeline status -- Queue status

Read content-queue.json, output grouped by status:

```
Content Pipeline Status

Seed (N):
  #3 "Multi-agent orchestration" -- 3/3 15:00

Drafted (N):
  #1 "AI Agent automation" -- 3/3 15:05
  #2 "Market arbitrage math" -- 3/3 16:20

Approved (N):
  #5 "MCP practical experience" -- 3/2 20:00

Published (N):
  #4 "Three-layer scraping approach" -- 3/1

Total: N items | Pending: seed(N) + drafted(N)
```

Show only non-archived items. If over 20 items, show most recent 20 + total count.

---

### /pipeline review <id> -- Review

1. Find the entry in queue
2. Display full info:

```
Review #<id>

Topic: <topic>
Status: <status>
Hook: <hook_angle>
Created: <created>

--- Draft ---
<full draft text>

--- Variants ---
[list any platform variants]

--- Research ---
File: <research_file>
[first 5 key findings if research file exists]

Actions:
  /pipeline approve <id> -- approve for publishing
  /pipeline adapt <id> <platform> -- generate platform variant
```

---

### /pipeline approve <id> -- Approve

1. Change status to "approved"
2. Update `updated` timestamp
3. Output: `#<id> approved -- ready to publish`

---

### /pipeline adapt <id> <platform> -- Multi-platform adaptation

Adapt the draft for a different platform:

1. Read the entry's draft
2. Rewrite for the target platform's conventions:
   - Different character limits
   - Different audience expectations
   - Different formatting norms
3. Store in `variants.<platform>` field
4. Output: `<platform> variant generated -- /pipeline review <id> to see`

---

### /pipeline publish <id> -- Publish marker

1. Change status to "published"
2. Record `published` timestamp
3. Output: `#<id> marked as published`

---

### /pipeline clean -- Archive cleanup

1. Scan all `published` entries
2. Archive entries older than 30 days
3. Output: `Archived N old entries`

---

## Design principles

- Research and Ideate stages are **platform-agnostic** -- only the Write stage adapts for platform
- One research effort can produce content for multiple platforms ("one fish, many meals")
- Drafts should be **source-verified** before entering the queue -- no unsourced claims
- Seeds are cheap to capture, expensive to develop -- capture freely, develop selectively
- The pipeline is a framework, not a straitjacket -- skip stages when you already have what you need
