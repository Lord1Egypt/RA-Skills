# ShipGuard — Hard Rules

This file contains permanent rules that never expire.
Loaded automatically at session start. Applied before handling any request.

Format: [Date established] [CR that established it] Rule

---

## Universal Rules (apply to all projects)

- [2026-05-24] [core] Never write code before requirement is confirmed by user
- [2026-05-24] [core] Never silently expand scope beyond G1 estimate
- [2026-05-24] [core] Never mix two task types in one CR — split them
- [2026-05-24] [core] Never close a CR without regression testing
- [2026-05-24] [core] Never self-downgrade a critical path change to "low risk"
- [2026-05-24] [core] Always record lessons after CR closes, even if nothing went wrong

## Project-Specific Rules

(populated from PROJECT.md and ongoing lessons)
