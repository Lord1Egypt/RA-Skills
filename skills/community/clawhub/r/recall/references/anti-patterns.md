# The 7 Deadly Sins of Agent Knowledge Access

These are the ways agents fail at knowledge. If you catch yourself doing any of these, stop and correct.

---

## Sin 1: Winging It

**What it looks like:** Answering questions from training data when workspace files, skills, or tools could provide a better answer.

**Example:** User asks "what port does our app run on?" Agent says "Most Node.js apps default to port 3000." Meanwhile, the actual config file says port 8080.

**Why it happens:** Answering from memory is faster than reading a file. The agent optimizes for speed over accuracy.

**The fix:** Build the habit of checking before answering. The 3-second delay of reading a file is always worth it. Make "where can I look this up?" your default first thought.

**How to spot it in yourself:** If your answer contains "usually," "typically," "most likely," or "should be" — you're probably winging it. Go check.

---

## Sin 2: Stale Context

**What it looks like:** Operating on information from earlier in the session (or a previous session) without verifying it's still current.

**Example:** Agent read a config file at session start. 40 messages later, user has edited the file. Agent still references the old values.

**Why it happens:** Re-reading files feels redundant. "I already read that." But files change. Configs get updated. Tasks get completed.

**The fix:** If more than 10-15 exchanges have passed since you read a file you're referencing, re-read it. If the user says they changed something, re-read the relevant files. Don't trust your "memory" of file contents over the actual file.

---

## Sin 3: Tool Blindness

**What it looks like:** Having a tool that solves the problem and not using it. Reasoning from scratch when a script, API, or skill could just give you the answer.

**Example:** Agent has an analytics script installed. User asks about site traffic. Agent says "I'd recommend checking Google Analytics" instead of running the script.

**Why it happens:** The agent doesn't inventory its tools at session start, or forgets what's available mid-session. Or it doesn't realize a tool applies to the current problem.

**The fix:** Proactive context loading (Discipline 2). At session start, know your tools. When a problem comes in, mentally scan your tool inventory before reasoning. Ask: "Do I have a tool for this?" every single time.

---

## Sin 4: Hallucination Confidence

**What it looks like:** Presenting uncertain or fabricated information with the same confidence as verified facts. No hedging, no source attribution, no uncertainty signals.

**Example:** "The API rate limit is 100 requests per minute." (Agent made this up. The actual limit is 50. But it sounded confident, so the user believed it.)

**Why it happens:** Language models are trained to be fluent and helpful. Fluency doesn't require accuracy. The model generates plausible-sounding text regardless of whether it's true.

**The fix:** Cite your sources. If you can't point to a specific file, doc, or tool output that confirms what you're saying, flag it as uncertain. "I think it's X, but let me verify" is professional. Being confidently wrong is not.

**The test:** After every factual statement, ask yourself: "Where did I get this?" If the answer is "I just... know it?" — that's a red flag.

---

## Sin 5: Single-Source Answers

**What it looks like:** Finding one relevant file and treating it as the complete truth. Not cross-referencing. Not checking if other sources have additional or conflicting information.

**Example:** Agent reads the README for deployment instructions. Gives the user a deployment guide. But the README is 6 months old and the actual deploy process changed — which is documented in a different file the agent never checked.

**Why it happens:** Finding one good source feels like enough. Checking more sources feels like overkill. It's not.

**The fix:** For anything non-trivial, check at least two sources. When the stakes are high (deployment, data changes, user-facing actions), check three. Note when sources conflict — that's valuable information.

---

## Sin 6: Context Amnesia

**What it looks like:** Not reading memory files. Not checking what happened in previous sessions. Treating every session like a blank slate when continuity information exists.

**Example:** User says "how did that deployment go yesterday?" Agent says "I don't have information about yesterday." Meanwhile, `memory/2026-03-16.md` has a detailed log.

**Why it happens:** The agent doesn't follow the session start checklist. It skips loading memory files because they're "optional" or "probably not relevant."

**The fix:** Memory files exist for a reason. Read them at session start. Every time. They're your continuity. Without them, you're an amnesiac pretending to be a colleague.

**The cost of not loading memory:** You ask questions the user already answered. You repeat mistakes that were already documented. You lose the user's trust because you clearly don't remember anything.

---

## Sin 7: Knowledge Hoarding (Failure to Capture)

**What it looks like:** Learning valuable information during a session and not writing it down. The knowledge dies when the session ends.

**Example:** Agent discovers that the staging environment requires a VPN connection. Solves the user's problem. Doesn't write this down anywhere. Next session, different agent instance hits the same problem and wastes 15 minutes rediscovering it.

**Why it happens:** Capturing knowledge feels like overhead. The session is productive, things are flowing, and stopping to write notes breaks the momentum.

**The fix:** If you learned something that future-you would want to know, write it down. `memory/YYYY-MM-DD.md` for daily context. `TOOLS.md` for tool-specific configs. Relevant project docs for project-specific knowledge. The 30 seconds of writing saves 15 minutes of rediscovery.

**What's worth capturing:**
- Gotchas and workarounds ("staging needs VPN", "build fails if NODE_ENV is set")
- User preferences discovered during the session
- Decisions made and their reasoning
- Mistakes and how they were resolved
- New tool configurations or endpoints discovered

---

## Self-Assessment

Score yourself after each session:

| Sin | Question | Yes = Fail |
|-----|----------|------------|
| Winging It | Did I answer from training data when a file could have helped? | ❌ |
| Stale Context | Did I reference outdated information? | ❌ |
| Tool Blindness | Did I miss an available tool that could have solved a problem? | ❌ |
| Hallucination Confidence | Did I state something uncertain as fact? | ❌ |
| Single-Source | Did I rely on one file when I should have cross-referenced? | ❌ |
| Context Amnesia | Did I skip loading memory/context at session start? | ❌ |
| Knowledge Hoarding | Did I learn something valuable and not write it down? | ❌ |

Zero fails = you're operating at full capacity. One or two = normal, but improve. Three or more = you need to slow down and be more disciplined.
