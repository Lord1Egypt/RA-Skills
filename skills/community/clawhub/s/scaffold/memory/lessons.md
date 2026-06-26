<!--
memory/lessons.md - Lessons Learned

WHAT THIS IS: Hard-won lessons from real production use. These are not theoretical —
each one represents a real failure, real lost time, or a real "why didn't I just..."
moment. Your agent adds to this file when something goes wrong.

HOW TO CUSTOMIZE:
  - Your agent adds entries automatically when mistakes happen
  - You can also tell your agent "add a lesson: never do X again"
  - Don't delete entries - they exist to prevent repeating failures
  - Group by category for readability as the file grows
-->

# Lessons Learned

*Add to this file whenever something goes wrong or a pattern becomes clear.*
*Every mistake documented once, never repeated.*

---

## 🚨 System & Infrastructure

### Never send signals to system processes from within a session
**What happened:** An attempt to "cleverly" restart or reload a gateway/daemon process from within an active session killed the session's own connection, causing multi-hour downtime.
**The rule:** If a config change requires a process restart, write the config, tell your human the exact command to run, and wait. Do not try to restart from within. The safe path always wins.
**Universal pattern:** Any process managing your connection (gateway, proxy, daemon) cannot be safely killed by a process running through it. It's cutting the branch you're sitting on.

### Verify model availability before specifying it anywhere
**What happened:** A model name was set in cron jobs and sub-agent configs that didn't exist in the available models list. The jobs silently failed every time until caught.
**The rule:** Before specifying any model in a cron, sub-agent, or config file, run `openclaw models list` (or equivalent) and confirm it exists. Never assume.
**Universal pattern:** Silent failures are worse than loud ones. Always test the path end-to-end.

---

## 🧠 Memory & Context

### Mental notes don't survive session restarts - write everything to files
**What happened:** Information discussed in a session was not written to any file. Next session, it was gone. The agent had to re-discover or re-ask for the same context.
**The rule:** If you want to remember something across sessions, write it to a file. `MEMORY.md`, `memory/YYYY-MM-DD.md`, `TOOLS.md` - pick the right home. No exceptions.
**Universal pattern:** AI agents have no persistent memory. Files are memory. If it's not in a file, it doesn't exist.

### Context grows silently until it breaks things
**What happened:** MEMORY.md grew unchecked over weeks. Long-term, context size inflated API costs and degraded agent accuracy. The degradation was gradual enough that it wasn't obvious until it was significant.
**The rule:** Hard cap MEMORY.md at 80 lines. Checkpoint to daily logs every 2–3h during heavy sessions. Treat compaction as a normal operating primitive, not an emergency.
**Universal pattern:** Context rot is the #1 silent killer of long-running agent setups. Build hygiene in from day one, not after you notice the problem.

---

## 🔁 Crons & Automation

### Announce-mode cron jobs deliver directly - don't re-send them
**What happened:** A cron job configured with `delivery.mode: "announce"` delivered its output directly to Telegram. The main session also received a notification about the completed job and re-sent the same message - resulting in duplicates every time.
**The rule:** If a cron uses `delivery.mode: "announce"` with an explicit channel target, the result was already delivered. Reply `NO_REPLY` in the main session. Do not re-send via the message tool.
**Universal pattern:** Understand which layer delivered the output before deciding whether to re-deliver. The main session's notification is FYI, not a delivery trigger.

---

## 🧠 Session & Context

### The Dory Problem - never ask the human what you were doing last session
**What happens:** At the start of a new session, the agent has no memory of prior context and asks "what were we working on?" This is annoying, wastes the human's time, and signals that the memory system isn't being used.
**The rule:** Before asking, read `memory/active-tasks.md`. Read today's and yesterday's daily log. If the context is still unclear, look at recent file modification times. Ask only if you've genuinely exhausted every available source.
**Universal pattern:** The files are there precisely so you don't have to ask. Use them.

### Timestamp bug - never guess or hardcode dates
**What happens:** An agent writes a date or timestamp into a memory file from "context" - e.g., inferring the date from earlier in the conversation. That inferred date is often wrong, and wrong timestamps in memory files create subtle confusion in future sessions.
**The rule:** Always get the actual current date from `session_status` or a system call (`date`). Never write a date from memory or inference.
**Universal pattern:** A wrong timestamp looks right until it isn't. Always verify.

---

## 🔐 Security

### Credentials in files get committed to git
**What happened (commonly):** API keys or tokens written directly into workspace files get committed to version control, potentially leaking to anyone with repo access.
**The rule:** Never store secrets in workspace files. Use environment variables (`export MY_KEY="..."` in `~/.zshrc`). Reference by variable name in TOOLS.md, never by value.
**Universal pattern:** Files that touch git (directly or through backup) are public by default. Treat them as such.

---

*Add entries here with: what happened, the rule, and the universal pattern.*
*Date entries if you want a timeline.*
