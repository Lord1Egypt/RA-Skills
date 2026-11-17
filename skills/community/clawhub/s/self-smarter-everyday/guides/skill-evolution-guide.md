# Skill Evolution Guide

## Overview

Skills are the agent's reusable capabilities — structured procedures that turn complex tasks into repeatable, reliable workflows. The Self-Smarter-Everyday skill includes a continuous skill evolution system that discovers new skill needs, assesses existing skill effectiveness, creates new skills when gaps are identified, modifies underperforming skills, and retires obsolete ones.

This guide explains how skill evolution works within the nightly routine and how you can influence the process.

---

## Skill Discovery

### How New Skill Needs Are Discovered

The nightly routine discovers skill needs through several mechanisms:

**1. Repeated Pattern Detection**

When the agent encounters similar multi-step tasks repeatedly (3+ times in a 7-day window), it flags the pattern as a potential skill candidate. For example, if the agent deploys a Docker container every day with slight variations, the deployment process could become a skill.

**Detection criteria:**
- Same sequence of tool calls appearing 3+ times in 7 days
- Same file paths or patterns being modified repeatedly
- Same error recovery steps being taken
- User giving similar multi-step instructions multiple times

**2. Explicit User Requests**

When the user says things like "remember how to do this" or "make this a skill" or "you should know how to do this automatically," the agent records a skill creation request.

**3. Self-Identified Gaps**

During the skill gap analysis phase, the agent reviews interactions where it performed poorly and asks: "Would a dedicated skill have helped here?" If the answer is yes and the task is recurring, a skill creation request is generated.

**4. External Triggers**

Skills may also be discovered through:
- ClawHub marketplace browsing (new skills published by the community)
- GitHub repository scanning (new tools or workflows discovered)
- Documentation updates (new API capabilities that warrant a skill)

### Skill Discovery Queue

All discovered skill needs are added to a queue at `data/skill-snapshots/discovery-queue.json`:

```json
[
  {
    "id": "disc-2026-08-10-001",
    "discoveredDate": "2026-08-10",
    "source": "repeated-pattern",
    "description": "Docker container deployment with Traefik routing",
    "frequency": 5,
    "estimatedTimeSavings": "15 minutes per occurrence",
    "priority": 0.78,
    "status": "pending-assessment"
  }
]
```

---

## Skill Assessment

### Evaluating Existing Skills

Each existing skill is assessed during the nightly routine on the following criteria:

**1. Usage Frequency**

How often is the skill invoked? Skills that haven't been used in 30+ days are candidates for retirement. Skills used daily are high-value and should be maintained carefully.

**2. Success Rate**

When the skill is invoked, how often does it succeed without errors or manual intervention? A skill with a declining success rate may need updating.

**3. User Satisfaction**

When the skill is used, does the user express satisfaction? Negative feedback after skill execution indicates the skill's procedure may be outdated or incorrect.

**4. Maintenance Burden**

How often does the skill need manual correction or workarounds? High-maintenance skills may benefit from restructuring or may indicate the underlying tooling has changed.

**5. Coverage Completeness**

Does the skill cover all common variations of the task? If users frequently need to provide additional instructions beyond what the skill specifies, the skill is incomplete.

### Assessment Scoring

Each skill receives a health score from 0.0 to 1.0:

```
Skill Health = (usageFrequency × 0.20) + (successRate × 0.30) + (userSatisfaction × 0.25) + (maintenanceInverse × 0.15) + (coverageCompleteness × 0.10)
```

### Assessment Schedule

Not all skills are assessed every night. The assessment rotates through the skill catalog:

- **Critical skills** (used daily) — assessed every night
- **Active skills** (used weekly) — assessed every 3 nights
- **Occasional skills** (used monthly) — assessed weekly
- **Dormant skills** (not used in 30+ days) — assessed monthly, then flagged for retirement review

---

## Skill Creation Triggers

A new skill is created when any of the following conditions are met:

### Automatic Triggers

1. **Pattern threshold** — A repeated pattern has been detected 5+ times in 14 days, and no existing skill covers it.
2. **User request** — The user explicitly asked for a skill to be created.
3. **Gap severity** — The skill gap analysis identified a critical capability gap that caused repeated failures.
4. **External availability** — A relevant skill was discovered on ClawHub or GitHub that can be adapted.

### Creation Process

When a creation trigger fires, the nightly routine follows these steps:

**Step 1: Specification**

Generate a skill specification based on the observed patterns:
- Name and description
- Trigger conditions (when should this skill be invoked?)
- Step-by-step procedure
- Expected inputs and outputs
- Error handling procedures
- Verification steps

**Step 2: Draft Generation**

Create a draft `SKILL.md` file following the OpenClaw skill format. The draft is saved to `data/skill-snapshots/pending/YYYY-MM-DD-{skill-name}/SKILL.md`.

**Step 3: Integration with Skill Workshop**

The draft is submitted to the OpenClaw Skill Workshop as a pending proposal. This allows human review before the skill becomes active. The skill workshop integration uses the `skill_workshop` tool with `action: "create"`.

**Step 4: Testing**

If the skill can be safely tested (non-destructive operations only), the routine runs a simulated execution using historical data as input. Results are recorded in the skill snapshot.

**Step 5: Activation Decision**

Based on test results and priority scoring, the routine decides:
- **Activate immediately** — for low-risk, high-confidence skills (read-only operations, analysis tasks)
- **Queue for human review** — for skills that modify external systems
- **Defer** — if resources are constrained or the skill needs more data

---

## Skill Modification Rules

### When to Modify an Existing Skill

An existing skill is modified when:

1. **Success rate drops below 0.7** — The skill is failing too often.
2. **User feedback indicates incorrect procedure** — The skill's steps are outdated.
3. **Underlying tools have changed** — API updates, new CLI options, deprecated commands.
4. **Coverage gaps identified** — Common variations of the task aren't covered.
5. **Efficiency improvement possible** — The procedure can be streamlined.

### Modification Constraints

**Safety rules for skill modification:**

- **Never modify a skill while it's actively being executed** in a live session.
- **Always create a snapshot** of the current skill version before modification. This enables rollback.
- **Limit modifications to 1 per skill per nightly cycle** — prevents cascading changes that are hard to debug.
- **Test modifications** using the same testing process as new skill creation.
- **Document changes** — every modification includes a changelog entry explaining what changed and why.

### Modification Process

```
1. Snapshot current skill version → data/skill-snapshots/versions/{skill-name}/v{N}.md
2. Apply modification to the skill file
3. Increment version number
4. Run test execution (if safe)
5. Compare test results to pre-modification baseline
6. If improved → keep modification, log changelog
7. If degraded → rollback to snapshot, log failure
```

---

## Skill Retirement

### Retirement Criteria

A skill is retired when:

1. **Not used in 60+ days** — The skill is no longer relevant.
2. **Superseded by a better skill** — A new skill covers the same capability more effectively.
3. **Underlying capability removed** — The tool or API the skill depends on no longer exists.
4. **Consistently harmful** — The skill causes errors more often than it helps.

### Retirement Process

Retirement is not deletion. The retirement process preserves the skill for reference:

1. **Move to retired directory** — `skills/{name}/` → `data/skill-snapshots/retired/{name}/`
2. **Update skill index** — Remove from the active skills list
3. **Log retirement reason** — Record why the skill was retired for future reference
4. **Notify via nightly report** — The nightly report mentions the retirement

### Un-retirement

If a retired skill's capability becomes needed again, it can be restored from the retired directory. The nightly routine checks retired skills when identifying gaps — sometimes the best new skill is a resurrected old one with updates.

---

## Skill Testing

### Testing Methodology

Skills are tested using historical interaction data as input. The testing process:

1. **Select test cases** — Find 3-5 historical interactions that would have triggered this skill.
2. **Simulate execution** — Run the skill's procedure against the test inputs in a sandboxed context.
3. **Compare outputs** — Compare the skill-guided output to the actual historical output.
4. **Score the results** — Did the skill produce better, worse, or equivalent results?

### Testing Constraints

- **Read-only testing only** — Tests must not modify external systems, send messages, or make irreversible changes.
- **No API calls to paid services** — Tests use cached data, not live API calls.
- **Time-bounded** — Each test must complete within 5 minutes.
- **Reproducible** — Tests use fixed inputs so results are comparable across skill versions.

---

## Skill Versioning

### Version Control

Every skill version is tracked in the skill snapshot directory:

```
data/skill-snapshots/versions/
├── docker-deploy/
│   ├── v1.md          # Original version
│   ├── v2.md          # Added Traefik label support
│   ├── v3.md          # Fixed health check timing
│   └── v3-active.md   # Symlink to current active version
├── email-triage/
│   ├── v1.md
│   └── v1-active.md
```

### Version Metadata

Each version file includes metadata in YAML frontmatter:

```yaml
---
skill_name: docker-deploy
version: 3
created: 2026-08-10T02:15:00+07:00
modified_by: nightly-routine
changelog: "Added health check timing fix based on error pattern from Aug 9"
test_results:
  cases_run: 5
  cases_passed: 5
  improvement_over_previous: 0.12
---
```

---

## Integration with OpenClaw Skill Workshop

The skill evolution system integrates with the OpenClaw Skill Workshop for human-in-the-loop governance:

### Workflow

1. **Nightly routine discovers a need** → creates a draft skill
2. **Draft is submitted to Skill Workshop** → `skill_workshop(action: "create", ...)`
3. **Skill sits in "pending" status** → visible in the workshop listing
4. **Human reviews** → can apply, reject, or quarantine the proposal
5. **If applied** → skill becomes active and is available to the agent
6. **If rejected** → skill is moved to retired with the rejection reason noted
7. **If quarantined** → skill is held for further investigation

### Benefits of Workshop Integration

- **Human oversight** — no skill becomes active without the option for human review
- **Version history** — the workshop tracks proposal history
- **Support files** — skills can include templates, scripts, and examples
- **Discovery** — the workshop listing shows all pending and active skills

---

## Summary

Skill evolution is what makes the Self-Smarter-Everyday system compound over time. Each night, the agent doesn't just fix mistakes — it builds new capabilities, refines existing ones, and retires what's no longer useful. The skill evolution system is designed to be safe (sandboxed testing, version control, rollback capability), governed (Skill Workshop integration), and effective (data-driven creation triggers, continuous assessment). Over weeks and months, the agent's skill catalog grows and improves, making it progressively more capable and reliable.
