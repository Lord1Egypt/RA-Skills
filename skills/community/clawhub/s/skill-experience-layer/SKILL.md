---
name: skill-experience-layer
slug: jilanfang/skill-experience-layer
version: 1.0.0
description: Pre-call experience checking + error-driven learning + layered experience storage. Avoid repeating mistakes, get smarter every time. Pre-integrated with self-improving and capability-evolver.
read_when:
  - Setting up a new agent instance
  - Wanting to avoid repeating mistakes
  - Integrating self-improving with your existing memory system
  - Building a self-growing agent that learns from practice
metadata:
  author: jilanfang
  license: MIT
  tags: self-improvement, memory, experience, learning, best-practices
  "clawdbot": {"emoji": "🧠", "requires": {"bins": []}, "os": ["linux", "darwin", "win32"], "configPaths": ["memory/experiences/"]}
---

# Skill Experience Layer - 技能经验分层机制

## What it does

Give your agent **permanent, per-skill experience memory** that:

1. **Pre-call checking**: Before you call any skill, *automatically read the common mistakes and best practices* so you avoid repeating the same pitfalls
2. **Error-driven learning**: When you make a mistake, *immediately record it to the corresponding skill's experience file*
3. **Automatic evolution**: Integrates with `capability-evolver` to automatically improve experience when mistakes repeat
4. **Fits existing memory architecture**: Works with your existing (instant → hot → short-term → long-term) memory hierarchy

## Why this is different

| Approach | Traditional | skill-experience-layer |
|----------|-------------|------------------------|
| When lessons are applied | *After* mistake (retrospective) | *Before* next call (preventive) |
| Experience storage | Global reflection | Per-skill JSON files, easy to evolve |
| Integration | Self-contained, requires manual integration | Designed to fit your existing memory hierarchy |
| Automatic evolution | No built-in support | First-class integration with capability-evolver |

## Workflow

### 1. For every skill you use

When you install a new skill:
- Create `memory/experiences/{skill-name}.json`
- Define `commonMistakes[]` and `bestPractices[]`
- *Before every invocation*, read it and remind yourself what to avoid

### 2. When you make a mistake

1. Stop immediately, don't keep retrying
2. Record the mistake in `self-improving/corrections.md`
3. Update the skill's experience JSON:
   - Add new entry to `experiences[]` with context, lesson, prevention
   - Update `commonMistakes[]` if it's a new pattern
   - Increment `failureCount`
4. If the *same mistake repeats 2+ times*, trigger `capability-evolver` to automatically improve the experience and best practices
5. Retry after updating

### 3. Regular maintenance

- **Daily**: End-of-day review mistakes, update experiences
- **Weekly**: Promote key lessons to long-term memory in MEMORY.md
- **Automatic**: capability-evolver can continuously improve stale experiences

## Example experience file

```json
{
  "type": "skill",
  "name": "my-skill",
  "lastUpdated": "2026-03-17T19:00:00+08:00",
  "totalExecutions": 10,
  "successCount": 8,
  "failureCount": 2,
  "experiences": [
    {
      "id": "exp-my-skill-001",
      "timestamp": "2026-03-10T20:00:00+08:00",
      "context": "What you were doing when the mistake happened",
      "lesson": "What you learned",
      "severity": "medium",
      "timesRepeated": 1,
      "prevention": "What to do differently next time"
    }
  ],
  "patterns": {
    "commonMistakes": [
      "First common mistake to avoid",
      "Second common mistake"
    ],
    "bestPractices": [
      "First best practice",
      "Second best practice"
    ]
  }
}
```

## Integration with existing systems

Works great with:

- **self-improving**: Uses the correction/reflection workflow
- **capability-evolver**: Automatic experience improvement when mistakes repeat
- **Your existing memory hierarchy**: Experiences live in `memory/experiences/`, fits alongside your daily/weekly memory

## Safety Boundaries

- ✅ Only modifies experience files in `memory/experiences/` and skill-owned files
- ✅ Never touches core root files (`MEMORY.md`, `SOUL.md`, `IDENTITY.md`, `USER.md`, `.env`) — reads but does not write
- ✅ Never accesses sensitive directories (`~/.ssh`, `~/.aws`, `/etc`)
- ✅ All automatic changes are backed up before applying, can roll back
- ✅ High-risk changes require human approval

## Author

Created from practical experience integrating self-improvement into a working agent. This is the missing glue between general self-improving frameworks and your actual daily usage.

**Get smarter with every mistake, don't repeat the same pit twice.**
