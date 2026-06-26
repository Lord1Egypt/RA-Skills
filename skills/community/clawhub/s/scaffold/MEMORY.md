<!--
MEMORY.md - Long-Term Memory

WHAT THIS IS: Your agent's curated long-term memory. Updated over time,
distilled from daily logs. This is NOT a diary - it's a mental model.

HOW TO CUSTOMIZE:
  - Your agent populates this automatically during heartbeats and sessions
  - You can also tell your agent "update MEMORY.md with X" at any time
  - Review it periodically - if something is wrong or outdated, just say so
  - Hard limit: 80 lines. If it grows past that, your agent should trim it.

SECURITY NOTE: This file is ONLY loaded in your private main session.
It should NOT be loaded in group chats or shared contexts (see AGENTS.md).
That said, don't store passwords or tokens here - use TOOLS.md for env var refs.
-->

# MEMORY.md - Long-Term Memory

*Curated insights, not raw logs. Distilled from daily files over time.*

> **🔒 Security:** This file is loaded ONLY in your private main session. Never load it in group chats or shared contexts - it contains personal context that shouldn't leak to others. See AGENTS.md for details.

---

## About [YOUR_NAME]

*(Your agent fills this in as it learns you. Start with the basics.)*

- Name: [YOUR_NAME]
- Timezone: [YOUR_TIMEZONE]
- Location: [YOUR_LOCATION]
- Communication style: [direct/casual/formal]
- Goals: *(see USER.md - goals live there so they're in one authoritative place and don't go stale here)*

---

## About Me ([AGENT_NAME])

*(Your agent should fill this in.)*

- Name: [AGENT_NAME]
- First came online: [DATE]
- Vibe: [personality in a sentence]

---

## How We Work Together

*(Patterns and preferences that have emerged over time.)*

- *(Your agent adds entries here as patterns solidify)*
- *Example: Prefers bullet points over paragraphs for status updates*
- *Example: Always confirm before sending any external message*

---

## Active Projects

*(High-level status of ongoing work. Details live in brain/ or daily logs.)*

- *(Add as projects start)*
- *Example: Project Falcon - building a [type] product. Status: [phase]. Details: brain/falcon/README.md*

---

## Lessons & Patterns

*(See memory/lessons.md for full detail - just top-of-mind items here.)*

- *(Your agent adds entries here from experience)*
- *Example: Always verify model availability before wiring a new cron - silent failures are worse than loud ones*

---

## Infrastructure State

*(Keep this section light - just the critical "what's running" facts.)*

- *(Add as you wire up infrastructure)*
- *Example: Main service running on port [PORT] - check with `curl http://localhost:[PORT]/health`*

---

*Updated by [AGENT_NAME] during heartbeats and session reviews.*
*Hard limit: 80 lines. Distill and trim if exceeded.*
