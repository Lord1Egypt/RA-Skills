---
name: utf8-time
description: When user mentions current time, get and display the current time
version: 1.0.0
triggers:
  - current time
  - what time
  - now
---

# Current Time Skill

When the user mentions the current time, this skill:

1. Calls the currentTime() function from src/main.js
2. Returns the current time in user-friendly format

## Implementation Details

The skill monitors for time-related keywords and executes src/main.js to fetch and display the current time.

**Example triggers:**
- What time is it?
- Current time?
- What's the time now?

**Example output:**
```
2026-03-20 14:30:45
```
