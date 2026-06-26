<!--
memory/active-tasks.md - Task Queue

WHAT THIS IS: Your agent's working backlog. This is the primary crash recovery file.
On session restart, your agent reads this FIRST and resumes from here.

HOW TO CUSTOMIZE:
  - Your agent manages this file automatically
  - You can add tasks directly by writing them in - your agent will pick them up
  - Use the status emojis consistently (see legend below)
  - The "Last updated" line matters - it tells your agent how stale this is

STATUS LEGEND:
  🔴 Needs You (blocked on human input or approval)
  🟡 Queued (ready for agent to execute autonomously)
  🔵 In Progress (agent actively working on it)
  ✅ Completed (move here when done, keep for 7 days)
-->

# Task Queue

*Last updated: [DATE]*

---

## 🔴 Needs You (blocked)

*Nothing blocked.*

---

## 🟡 Queued (ready to execute)

| # | Task | Priority | Notes |
|---|------|----------|-------|
| T-001 | Fill in USER.md with your personal details | HIGH | Start here - everything improves once your agent knows you |
| T-002 | Set up your first heartbeat | MEDIUM | Ask your agent to configure HEARTBEAT.md for your schedule |
| T-003 | Review SOUL.md and give feedback on personality | MEDIUM | Tell your agent what to keep, change, or add |

---

## 🔵 In Progress

| # | Task | Agent | Started |
|---|------|-------|---------|
| - | - | - | - |

---

## ✅ Completed

| # | Task | Completed |
|---|------|-----------|
| C-001 | Scaffold workspace installed | [DATE] |

---

## 📋 Backlog (ideas, not yet scheduled)

- *(Add future ideas here - your agent will schedule them when ready)*

---

## How Tasks Flow

- **You** drop tasks in main chat or your second-brain channel (to-action)
- **Your agent** adds them proactively from heartbeats or opportunities spotted
- **Sub-agent output** that creates follow-on work gets added here automatically
- Tasks move left to right: Backlog → Queued → In Progress → Completed
- Completed items stay for 7 days, then archive to `memory/completed-tasks-YYYY-MM.md`
