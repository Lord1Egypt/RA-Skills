<!--
THIRTY-DAYS.md — Your First Month with Scaffold

WHAT THIS IS: A week-by-week roadmap for getting real value out of your agent setup.
Most people install Scaffold, have a great first session, then drift.
This guide prevents that. Each week has a specific focus and a concrete "done" state.

THE RULE: Don't skip ahead. Each week builds on the last. An agent that knows you well
in Week 2 does dramatically better work in Week 3.
-->

# Thirty Days with Your Agent

*A week-by-week guide to building a workspace that actually compounds.*

The biggest mistake people make with AI agents: they set them up, have a few great sessions, then stop. The agent never gets a real chance to learn who you are, what you're building, or how you think. Three weeks later it feels like starting over every time.

This guide is the antidote. Four weeks, one focus per week. By the end, you have an agent that knows you — not because it guessed, but because you built it that way together.

---

## Before Day 1

Run the setup wizard (`bash setup-wizard.sh`) and complete your first session (see FIRST-SESSION.md). Both take under 30 minutes combined. Everything below assumes those are done.

---

## Week 1 — Foundation (Days 1–7)

**Focus:** Get memory working. Make your agent remember things so you don't have to repeat yourself.

**The problem this week solves:** Most people finish their first session and then have a second session where the agent acts like it's never met them. This week fixes that permanently.

### Day 1–2: Complete Your First Session
- Run through FIRST-SESSION.md if you haven't. Don't skip it.
- After the session, verify: USER.md has real content about you. MEMORY.md has at least one entry. IDENTITY.md has your agent's name.

### Day 3–4: Daily Log Habit
- At the end of each working session, spend 2 minutes updating `memory/YYYY-MM-DD.md` with what you did. Your agent can do this automatically — tell it: *"At the end of each session, update today's daily log with what we worked on."*
- Check it the next morning. It should read like a useful handoff note, not a transcript.

### Day 5–6: Correct and Calibrate
- In normal conversation, notice anything your agent gets wrong about you — tone, assumptions, preferences.
- Tell it directly: *"Add a note: I prefer X over Y"* or *"That's not how I think about this — here's how I actually think about it."*
- Watch USER.md get more accurate. The file is only as good as what you put in it.

### Day 7: Week 1 Check
✓ USER.md has meaningful content (not just the template)
✓ MEMORY.md has 3+ entries
✓ You've had at least one session where the agent clearly remembered something from a previous session
✓ Daily logs are being written

**Done state:** Your agent knows who you are. It doesn't ask what timezone you're in or what you're working on. It already knows.

---

## Week 2 — Automation (Days 8–14)

**Focus:** Set up your first cron job. Get your agent working while you sleep.

**The problem this week solves:** Your agent is only useful when you're talking to it. Crons make it useful when you're not.

### Day 8–9: Identify Your First Cron
Ask yourself: what would I want waiting for me every morning? Options:
- Morning briefing (what's on my task list, any news worth knowing, one thing to focus on today)
- Weekly review (what did I accomplish this week, what's next)
- Something domain-specific (price check, research update, health summary)

Tell your agent: *"Help me set up a morning briefing cron that runs at [time] and sends a summary to [channel]."*

### Day 10–11: Wire Up a Delivery Channel
Your cron output needs somewhere to go. Options:
- Telegram (fastest to set up — see SETUP-GUIDE.md for config)
- Discord (good if you're already there)
- Email (via webhook)

Pick one. Get it working. A cron nobody reads is useless.

### Day 12–13: Tune the Output
Run the cron manually to see what it produces: *"Run my morning briefing now as a test."*
Is it too long? Too short? Missing something? Tell your agent to adjust the prompt.
The first version is never the right version. Two iterations usually gets it there.

### Day 14: Week 2 Check
✓ At least one cron is running on a schedule
✓ Output is delivered somewhere you'll actually see it
✓ You've tuned it at least once
✓ It saves you time you were previously spending manually

**Done state:** Something useful is happening without you triggering it.

---

## Week 3 — Delegation (Days 15–21)

**Focus:** Run your first sub-agent task. Learn to delegate instead of doing.

**The problem this week solves:** You're still doing everything yourself. Your agent can spawn specialized workers for research, writing, and building. This week you actually use that.

### Day 15–16: Read AGENTS-GUIDE.md (Full) or Pick a Task
*Lite users:* Think of something you'd normally spend 30–60 minutes researching — a competitor, a technology decision, a market question. That's your first sub-agent task.

*Full users:* Open AGENTS-GUIDE.md and pick Scout (research) or Quill (writing) — whichever fits the task you have.

### Day 17–18: Run Your First Delegation
Tell your agent: *"I need you to research [topic] and give me a structured brief. Spawn a sub-agent for this — I want it running in the background while I do other things."*

Watch what comes back. Note what's good and what's missing.

### Day 19–20: Calibrate the Output
The first sub-agent output is rarely perfect. Too much? Too little? Wrong format? Tell your agent: *"For future research tasks, I want the output structured like this..."* and describe what you actually want.

Prompt tuning is where the leverage is. 10 minutes refining a prompt saves hours across future uses.

### Day 21: Week 3 Check
✓ You've run at least one sub-agent task
✓ The output was actually useful (or you know what to change)
✓ You understand when to delegate vs. handle in the main session
✓ Your main session didn't get cluttered with research work

**Done state:** You're using your agent as an orchestrator, not just a chatbot.

---

## Week 4 — Review and Compound (Days 22–30)

**Focus:** Review what's working, fix what isn't, set up Month 2.

**The problem this week solves:** Most setups peak in Week 1 and slowly degrade. Week 4 is the maintenance pass that keeps the system improving instead of decaying.

### Day 22–24: Memory Audit
- How does MEMORY.md look? Is it under 80 lines? Is the content still accurate?
- Is USER.md still a good description of you, or has it drifted?
- Are the daily logs being written? Are they useful?
- Run: *"Audit my memory files. What's outdated, what's missing, what should be trimmed?"*

### Day 25–26: Cron Review
- Are your crons still delivering value?
- Any you never read? Kill them.
- Any patterns in what you've needed that aren't covered? Add a cron.
- Run: *"Review my cron setup. What's working, what should change?"*

### Day 27–28: Task Queue Health
- Open `memory/active-tasks.md`. Is it accurate?
- Anything stale (>2 weeks old with no update)?
- Anything you completed but never marked done?
- Clean it up. A stale task queue is a stale agent.

### Day 29–30: Month 2 Plan
Ask your agent: *"Based on everything you know about me, what should we build or improve in Month 2?"*

This is the compounding moment. An agent that knows you well, has your full context, and has seen how you work will give you a genuinely useful answer here. Not a generic list — a real recommendation based on your specific situation.

Write it down. Do it.

### Day 30: Month 1 Check
✓ MEMORY.md is accurate and under 80 lines
✓ At least 2 crons running and delivering value
✓ Sub-agent delegation is a regular part of your workflow
✓ You've done one full memory audit
✓ You have a plan for Month 2

**Done state:** Your workspace is better at the end of Month 1 than it was at the start. That's the baseline for compounding.

---

## The Compounding Principle

Each week you put in builds on the last. An agent with a rich USER.md does better work. An agent with accurate daily logs recovers from context resets faster. An agent you've delegated to before runs better sub-agents the second time.

The work you do in Month 1 isn't setup overhead — it's the infrastructure that makes Month 3 look effortless. Don't skip it.

---

*THIRTY-DAYS.md — part of Scaffold. Questions? See FAQ.md.*
