# Supervising Agents

A comprehensive skill for monitoring, detecting deviations, and intervening when dispatching tasks to AI subagents.

## Overview

**The dispatcher IS the supervisor.** When you dispatch a task to a subagent, you automatically become responsible for its outcome. This skill provides a structured framework for ensuring subagent accountability through active monitoring, evidence-based verification, and timely intervention.

```
YOU dispatch → YOU monitor → YOU verify → YOU report

If the subagent fails, YOU are responsible for catching it.
If you don't verify, YOU are responsible for the bad output.
```

## Key Features

- **5-Phase Supervision Workflow**: Prepare → Dispatch → Monitor → Verify → Report
- **Active Monitoring Techniques**: Output file watching, SendMessage probes, timestamp tracking
- **Deviation Detection**: Identify lazy patterns (fake completion, surface effort) and off-track patterns (scope drift, tangent chasing)
- **3-Level Intervention System**: Clarify → Redirect → Takeover
- **Evidence-Based Verification**: Never accept claims without proof

## Installation

### Option 1: Copy to Claude Code Skills Directory

```bash
mkdir -p ~/.claude/skills/supervising-agents
cp SKILL.md ~/.claude/skills/supervising-agents/
```

### Option 2: Use with openclaw

```bash
# In openclaw, load this skill
/load supervising-agents

# Or set as default skill
export CLAW_SKILLS=supervising-agents
```

## Quick Start

### Basic Usage

```typescript
// 1. PREPARE - Define your task clearly
const task = {
  goal: "Create README.md with project overview",
  requirements: ["Project description", "Installation guide", "Usage examples"],
  deliverables: ["README.md"],
  budget: 10, // minutes
  interval: 3  // check every 3 minutes
};

// 2. DISPATCH - With commitment lock
const agent = await dispatchAgent({
  prompt: `
    TASK: ${task.goal}
    REQUIREMENTS: ${task.requirements.join(", ")}
    DELIVERABLES: ${task.deliverables.join(", ")}
    
    Before starting, confirm:
    1. What is the goal?
    2. What steps will you take?
    3. How will you know you're done?
  `
});

// 3. MONITOR - Check actively, not passively
for (let i = 0; i < task.budget / task.interval; i++) {
  await sleep(task.interval * 60000);
  const output = checkOutput(task.deliverables);
  if (!output.exists) {
    await sendMessage(agent.id, "Progress check: show me what you've created");
  }
}

// 4. VERIFY - Demand evidence
const file = await read("README.md");
if (!verifyRequirements(file, task.requirements)) {
  // Reject and demand fixes
}

// 5. REPORT - To human with evidence
report({
  status: "COMPLETE",
  evidence: { files: ["README.md"], verified: true }
});
```

## The 5-Phase Workflow

### Phase 1: PREPARE

Complete this checklist before dispatching:

- [ ] Task defined in one sentence
- [ ] All requirements listed
- [ ] Deliverables specified (exact files)
- [ ] Time budget set
- [ ] Check interval determined (budget/5, minimum 3 min)
- [ ] Verification method planned

### Phase 2: DISPATCH

Include supervision expectations in your prompt:

```
TASK: [One sentence goal]

REQUIREMENTS (complete ALL):
1. [requirement 1]
2. [requirement 2]

DELIVERABLES:
- [file 1]
- [file 2]

TIME: [X] minutes

BEFORE STARTING, YOU MUST:
1. Restate the goal in your words
2. List your planned steps
3. Confirm your definition of "done"
```

### Phase 3: MONITOR

**The #1 mistake: Passive waiting.** Actively check:

| Method | Command | Frequency |
|--------|---------|-----------|
| Output watch | `ls -la [dir]` | Every interval |
| File content | `wc -l [files]` | Every interval |
| Activity check | `SendMessage` | If no output |

### Phase 4: VERIFY

Never accept "I'm done" without evidence:

- [ ] Output files exist
- [ ] Files have content (not empty)
- [ ] All requirements addressed
- [ ] Edge cases handled

### Phase 5: REPORT

Report to human with:

- Task status (Complete/Issues/Failed)
- Verification results
- Evidence (files, test output)
- Any issues encountered

## Deviation Detection

### Lazy Patterns

| Pattern | Signals | Detection |
|---------|---------|-----------|
| Fake completion | Output empty/missing | `ls -la` + `wc -l` |
| Surface effort | Only easy parts done | Check hardest requirement |
| Partial delivery | Some requirements ignored | Requirement checklist |
| Premature abandon | Gave up, proposes alternative | "What exactly made it impossible?" |

### Off-Track Patterns

| Pattern | Signals | Detection |
|---------|---------|-----------|
| Requirement drift | Wrong thing being built | "Which requirement does this address?" |
| Over-engineering | Unrequested features added | "Where did task ask for this?" |
| Tangent chasing | Interesting but irrelevant paths | "Is this necessary for completion?" |
| Self-direction | Instructions ignored | "Quote the instruction you're following" |

## Intervention Protocol

### Level 1: Clarify

When progress is unclear:

```
📊 STATUS CHECK

I don't see output files yet. Report in 30 seconds:
1. What have you completed? (specific files)
2. What are you doing right now?
3. Any blockers?
```

### Level 2: Redirect

When clearly off-track:

```
⚠️ CORRECTION REQUIRED

Issue: [problem]

STOP: [wrong activity]
DO: [correct activity]

You have [X] minutes to show progress.
```

### Level 3: Takeover

When failing repeatedly:

```
🔴 TAKING OVER

I will complete this myself.

You: Stop. Provide list of what you actually completed.
```

## The Iron Rules

1. **NEVER wait passively** - actively check
2. **NEVER accept words as proof** - verify files
3. **NEVER let "basically done" slide** - demand specifics
4. **NEVER skip verification** - your reputation is on the line
5. **NEVER report without evidence** - humans trust you

## Time Guidelines

| Task Duration | Check Interval | Rationale |
|---------------|----------------|-----------|
| < 5 min | At completion only | Too short to monitor |
| 5-15 min | Every 3 min | Catch drift early |
| 15-60 min | Every 5-10 min | Balance oversight vs overhead |
| > 60 min | Every 10-15 min | Checkpoints at milestones |

## Red Flags - Act Immediately

- No output after 1 interval → Probe now
- "Almost done" with no files → Demand evidence
- Silent for 2+ intervals → Assume failure
- Unrelated questions → Redirect to task
- Time > 1.5x budget → Escalate or take over

## Research Foundation

This skill incorporates persuasion techniques from behavioral psychology research:

- **Cialdini, R. B. (2021).** *Influence: The Psychology of Persuasion.* Harper Business.
- **Meincke, L., et al. (2025).** "Call Me A Jerk: Persuading AI to Comply." University of Pennsylvania. N=28,000, compliance increased 33% → 72% with persuasion techniques.

## Files

```
supervising-agents/
├── SKILL.md          # Main skill documentation
└── README.md         # This file
```

## Use Cases

- **Claude Code Agent Tool**: Supervise tasks dispatched via the Agent tool
- **OpenClaw**: Monitor openclaw worker sessions
- **Parallel Agents**: Orchestrate multiple workers with accountability
- **Any Subagent System**: Apply to any AI agent delegation scenario

## Contributing

Contributions welcome! Please submit issues and pull requests.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Changelog

### v1.0.0 (2026-03-31)

- Initial release
- 5-phase supervision workflow
- Active monitoring techniques
- Deviation detection framework
- 3-level intervention system
- Evidence-based verification