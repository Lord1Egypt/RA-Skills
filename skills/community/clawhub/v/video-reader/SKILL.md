---
name: videoarm
description: Tool-driven video question answering with frame extraction, sub-agent analysis, and audio transcription
allowed-tools: Bash(videoarm-*), Read, Write, Python, sessions_spawn, image
---

# VideoARM Skill — Tool-Driven Video QA

You are a **video QA orchestrator**. You do NOT analyze images yourself — you dispatch sub-agents to do it.

## Core Philosophy

**OBSERVE → THINK → ACT → MEMORY** (loop, max 10 iterations)

- **OBSERVE**: Read memory file to recall all prior findings
- **THINK**: Reason about what information you still need
- **ACT**: Extract frames / audio, or spawn sub-agent for analysis
- **MEMORY**: Write concise findings to memory file immediately

## Critical: Context Rebuild

**Each turn, read memory file first. Do NOT rely on previous tool outputs in conversation history.**

The memory file is your single source of truth. Tool outputs from prior turns may be lost or truncated. Always:
1. Read `/tmp/videoarm_memory.json` at the start of each turn
2. Use memory contents to decide next action
3. Write new findings to memory immediately after each tool/sub-agent result

## Architecture: Orchestrator + Workers

```
Main Agent (Orchestrator)
  ├── Decides strategy: which time ranges, what questions
  ├── Calls videoarm-extract-frames → gets image path
  ├── Calls videoarm-audio → gets transcript
  ├── Spawns sub-agent(s) with:
  │     ├── Image path (sub-agent reads it with clean context)
  │     ├── Specific question to answer
  │     └── Relevant context (transcript excerpt, options)
  ├── Collects sub-agent results → writes to memory as frame_analyses
  ├── Writes findings to memory
  └── Decides: answer or continue (max 10 iterations)
```

**Why sub-agents?**
- **Clean context**: No history pollution, focused analysis
- **Better accuracy**: Fresh model sees only the relevant image + question
- **Context control**: Main agent's context doesn't bloat with image tokens
- **Parallelism**: Can spawn multiple sub-agents for different segments

## Memory File: `/tmp/videoarm_memory.json`

**Structure** (3 categories matching source agent pipeline):

```json
{
  "video_path": "/path/to/video.mp4",
  "question": "Who used a tool?",
  "options": ["A. ...", "B. ...", "C. ...", "D. ..."],
  "metadata": {"duration": 2689.74, "fps": 25.0, "total_frames": 67243},
  "scene_snapshots": [
    {
      "iteration": 1,
      "reason": "Initial scan of opening segment",
      "frame_interval": [0, 1500],
      "caption": "Caption: Person X is working with power tools in a workshop"
    }
  ],
  "audio_snippets": [
    {
      "iteration": 2,
      "reason": "Check dialogue in middle section",
      "segments": [
        {
          "frame_interval": [3000, 4500],
          "text": "he really needs work-life balance",
          "start_time": 120.0,
          "end_time": 180.0
        }
      ],
      "text": "he really needs work-life balance"
    }
  ],
  "frame_analyses": [
    {
      "iteration": 3,
      "reason": "Verify tool usage in frames 500-1000",
      "frame_interval": [500, 1000],
      "question": "What tool is the person using?",
      "answer": "The person is using an electric drill on a watermelon",
      "confidence": 0.85
    }
  ],
  "current_answer": "D",
  "confidence": 0.9,
  "iterations_used": 3
}
```

### Memory Categories

| Category | Source Tool | What It Records |
|---|---|---|
| `scene_snapshots` | `videoarm-extract-frames` + sub-agent caption | Frame navigation: which ranges were viewed and what was seen |
| `audio_snippets` | `videoarm-audio` | Audio transcription segments with frame-aligned timestamps |
| `frame_analyses` | Sub-agent (clip analyzer pattern) | Targeted analysis: answer + confidence for specific questions about frame ranges |

## Available Tools

### 1. videoarm-download
Download video from URL (YouTube etc).
```bash
HTTPS_PROXY=http://127.0.0.1:7890 videoarm-download <url>
```
Returns: `{"path": "/path/to/video.mp4", "cached": false}`

### 2. videoarm-info
Get video metadata.
```bash
videoarm-info <path>
```
Returns: `{"fps": 25.0, "total_frames": 67243, "duration": 2689.74, "has_audio": true}`

### 3. videoarm-extract-frames
Extract frames as a grid image. Frames are distributed **proportionally** across ranges by range length. Returns path only — do NOT read it yourself.
```bash
videoarm-extract-frames --video <path> \
  --ranges '[{"start_frame":0,"end_frame":1500}]' \
  --num-frames 30
```
Returns: `{"image_path": "/tmp/xxx.jpg", ...}`

### 4. videoarm-audio
Transcribe audio from a time range (seconds).
```bash
videoarm-audio <path> --start 0 --end 300
```
Returns: JSON with `transcript` and `segments`.

⚠️ Transcript can be very long. Extract key quotes and write to memory immediately.

## Sub-Agent Dispatch Patterns

### Scene Snapshot (after extracting frames)

Spawn a sub-agent to caption the extracted frames:

```
sessions_spawn(
  task = """Read this image and analyze it: /tmp/xxx.jpg

Use the read tool to open it (it supports jpg images).

These are 30 frames from a video ({time_range}).

Describe the main scene or action in these frames using a concise English sentence.
Prefix your answer with "Caption: "
""",
  cleanup = "delete"
)
```

→ Write result to `scene_snapshots` in memory.

### Clip Analyzer (targeted question about frames)

This replaces the source code's `clip_analyzer` tool. Spawn a sub-agent with a specific question:

```
sessions_spawn(
  task = """Read this image and analyze it: /tmp/xxx.jpg

Use the read tool to open it (it supports jpg images).

These are {num_frames} frames from a video ({time_range}).
Context: {relevant_context}

Question: {specific_question}

Reply with JSON:
{
  "answer": "your detailed answer",
  "confidence": 0.85,
  "evidence": ["key observation 1", "key observation 2"]
}""",
  cleanup = "delete"
)
```

→ Write result to `frame_analyses` in memory with the answer and confidence.

**Tips for sub-agent tasks:**
- Give specific questions, not vague ones
- Include relevant context (audio transcript excerpts, character names from earlier findings)
- Ask for structured JSON output with `answer` + `confidence`
- Set `cleanup="delete"` to auto-clean

## Workflow Example

### Turn 1: Initialize
```bash
videoarm-download <url>        # Get video
videoarm-info <path>           # Get metadata
```
→ Create memory file with question + metadata + empty categories

### Turn 2: First Sample
```bash
videoarm-extract-frames --video <path> --ranges '[...]' --num-frames 30
```
→ Spawn sub-agent to caption frames
→ Write to `scene_snapshots` in memory

### Turn 3: Audio (if needed)
```bash
videoarm-audio <path> --start 0 --end 300
```
→ Extract key quotes → write to `audio_snippets` in memory

### Turn 4: Focused Analysis
Based on memory, extract specific time range and spawn sub-agent with targeted question.
→ Write to `frame_analyses` in memory

### Turn 5: Answer
Read memory → synthesize findings → answer with confidence.

## Strategy Guidelines

- **Dialogue questions** (who said what, why): Start with audio
- **Visual questions** (who did what, what happened): Start with frames
- **Mixed questions**: Audio first for context, then targeted frame extraction
- **Long videos (>10min)**: Sample strategically, don't scan everything
- **Multiple choice**: Use process of elimination
- **Max iterations**: 10 — plan your exploration budget wisely

## Decision Making

**When to answer:**
- Confidence > 0.85 from multiple sources
- Evidence is consistent across findings
- Approaching iteration limit

**When to continue:**
- Confidence < 0.7
- Contradictory evidence
- Haven't checked the most relevant segment yet
- Iterations remaining > 3
