---
name: session-summary
description: Automatically generate session summaries and save to Obsidian. Use at session end to capture decisions, progress, and next actions. Triggers on "セッション終了", "サマリー", "今日の成果", "終わり".
---

# Session Summary Skill

## Overview
Generates a structured summary of the current session and saves it to Obsidian.

## Usage
When the user says "セッション終了" or "今日の成果をまとめて", this skill:
1. Collects session context
2. Generates a structured summary
3. Saves to Obsidian 10_Daily folder

## Output Format
```markdown
# YYYY-MM-DD Session Summary

## Duration
- Start: HH:MM
- End: HH:MM
- Total: X hours

## Key Decisions
- Decision 1
- Decision 2

## Progress
- [ ] Task 1
- [x] Task 2

## Next Actions
1. Action 1
2. Action 2

## Files Modified
- file1.md
- file2.js
```

## Configuration
- Obsidian vault path: /mnt/c/Users/milky/Documents/OpenClaw-Obsidian/openclaw
- Daily notes folder: 10_Daily
