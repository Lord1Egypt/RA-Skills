---
name: spawner
version: 1.0.0
description: Instant agent hiring. Takes job postings from the orchestrator and fills them with properly configured sub-agents. Handles context passing, timeout enforcement, concurrent agent limits, and completion tracking. The bridge between scoping (orchestrator) and execution (sub-agents).
---

# Spawner — Instant Agent Hiring

Takes job postings → spawns the right agent → passes context → tracks completion.

## Activation

Invoked by the orchestrator after JOB_BOARD.md is written with job postings.
Can also be invoked directly when the user says "spawn an agent to do X".

## Input

Read `workspace/JOB_BOARD.md` for pending job postings.

Each posting has:
- Job title
- Bucket (BUILD/OUTREACH/etc)
- Task description
- Context (files, prior work)
- Acceptance criteria
- Workspace path
- Timeout
- Dependencies
- Expected outputs

## Spawning Rules

### Concurrency
- **Max 3 sub-agents running at once.** Period.
- Before spawning, check `subagents list` for active count.
- If at limit, queue the job and wait for a completion event.

### Agent Configuration by Bucket

| Bucket | Label Pattern | Timeout | Key Context to Pass | Notes |
|--------|--------------|---------|--------------------|----|
| 🏗️ BUILD | `build-[project]` | 600s | webdev-sop, project files, WORK_BUCKETS.md | Always include "npm run build must pass, git commit + push" |
| 📬 OUTREACH | `outreach-[target]` | 300s | outreach-infrastructure.md, warmup state, suppression list | Include SSH commands for droplet |
| 💰 SALES | `sales-[client]` | 300s | business-strategy.md, client project file | Include pitch framework |
| 🔧 MAINTAIN | `fix-[project]-[issue]` | 300s | Project memory file, error description | Include "verify fix works" step |
| 🧠 STRATEGY | `research-[topic]` | 300s | business-strategy.md, OUTSTANDING.md | Include "cite sources" requirement |
| 📦 PRODUCT | `product-[item]` | 300s | product-catalog-registry.md, casefinder docs | Include unit economics requirement |
| 🤖 SYSTEM | `system-[tool]` | 300s | Relevant skill files, OpenClaw docs | Include "test the skill" step |
| 💼 CAREER | `career-[company]` | 300s | Ryan's resume, target role | Include "output PDF" requirement |
| 💡 IDEATION | `ideation-[source]` | 600s | batch-cognition skill, value-stack.md | Include ICE scoring requirement |

### Task Description Template

For each sub-agent spawn, construct the task as:

```
You are working on: [workspace path]

## Job
[Bucket emoji] [Bucket name]: [Job title]

## What to Do
[Detailed task description from job posting]

## Context
[Relevant file contents or summaries — keep under 2K tokens]
[Reference to full files the agent can read itself]

## Acceptance Criteria
[Specific, testable conditions — copied from job posting]
- [ ] [criterion 1]
- [ ] [criterion 2]
- [ ] [criterion 3]

## Constraints
- [Bucket-specific constraints from table above]
- Do NOT modify .env files with real keys
- Build must pass before committing
- Git commit with descriptive message
```

### Dependency Handling

- Check the "Depends On" field of each job.
- If dependency job is ✅ DONE → spawn immediately.
- If dependency job is still running → queue, spawn after completion event.
- If dependency job ❌ FAILED → mark this job as BLOCKED, notify orchestrator.

### Context Passing Between Related Jobs

When jobs in the same wave are related:
- Job A produces `output/analysis.md` → Job B needs it as input
- Include in Job B's context: "Read [path] for context from related job"
- If Job A hasn't finished yet, Job B waits (dependency handling above)

## Spawn Execution

```python
# Pseudocode for spawning logic
for wave in execution_plan.waves:
    active = get_active_subagents()
    
    for job in wave.jobs:
        if job.effort == "QUICK":
            execute_inline(job)  # No sub-agent needed
            job.status = "✅"
            continue
        
        # Wait for slot
        while len(active) >= 3:
            wait_for_completion_event()
            active = get_active_subagents()
        
        # Check dependencies
        if job.depends_on and not all_done(job.depends_on):
            job.status = "QUEUED"
            continue
        
        # Spawn
        agent = sessions_spawn(
            label=f"{bucket_prefix}-{job.slug}",
            mode="run",
            runTimeoutSeconds=job.timeout,
            task=build_task_description(job)
        )
        job.status = "🔄"
        job.agent_key = agent.childSessionKey
        active.append(agent)
    
    # Wait for wave to complete before next wave
    wait_for_all_wave_completions(wave)
```

## Completion Tracking

When a sub-agent completion event arrives:
1. Match to job in JOB_BOARD.md by session key or label.
2. Check acceptance criteria:
   - Does the expected output exist?
   - Did the build pass?
   - Did it push to git?
3. Mark job: ✅ DONE (with artifact link) or ❌ FAILED (with reason) or ⚠️ PARTIAL.
4. Update JOB_BOARD.md.
5. Check if any QUEUED jobs can now be spawned (dependency resolved).
6. If all jobs in current wave done → start next wave.

## Failure Handling

| Failure Type | Action |
|-------------|--------|
| Sub-agent timeout | Kill agent, mark ⚠️, retry once with simpler scope |
| Sub-agent error | Mark ❌, log error, notify orchestrator |
| Build failure | Mark ⚠️, check build output, fix inline if trivial |
| Dependency failed | Mark BLOCKED, skip, notify orchestrator |
| 3 consecutive failures | Stop spawning, escalate to Ryan |

## Anti-patterns

- ❌ Spawning 10 agents at once (max 3)
- ❌ Spawning an agent for a 2-minute task (do it inline)
- ❌ Not passing context (agent wastes time re-reading)
- ❌ Marking ✅ without checking output exists
- ❌ Polling subagents in a loop (wait for push events)
- ❌ Spawning duplicate agents for the same job
- ❌ Not killing stale agents (> timeout + 5 min buffer)

## Output

Update `workspace/JOB_BOARD.md` with:
- Status per job (⏳ → 🔄 → ✅/❌/⚠️)
- Agent session key (for tracking)
- Artifact link (file path, URL, commit hash)
- Completion time

When all jobs complete, notify orchestrator for reconciliation.
