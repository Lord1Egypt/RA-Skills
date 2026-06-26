---
name: scenario-planning
description: >
 Perform project management what-if (scenario) analysis to simulate risks, delays, and resource changes. Use when planning schedules, assessing uncertainty, or evaluating project impacts in tools like Excel, MS Project, or Primavera.
---

# What-if Scenario Planning (WISA)

## When to Use
Use this skill when:
- A project plan needs risk simulation before execution
- The user asks “what if this changes?” in a project context
- There is uncertainty in schedule, cost, or resources
- The user is working in Excel, MS Project, or similar tools

---

## Core Objective
Simulate alternate project scenarios by modifying key variables (duration, resources, cost) and evaluate their impact on:
- Project timeline
- Critical path
- Total cost
- Resource utilization

---

## Execution Steps

### Step 1: Establish Baseline Plan
Ensure a complete baseline exists:
- Tasks with durations
- Dependencies (network/PERT)
- Resources assigned
- Cost estimates

If missing → ask user to define baseline first.

---

### Step 2: Identify Variables
Extract or ask for uncertain variables:
- Resource availability
- Task duration variability
- Budget constraints
- External risks (delays, logistics, approvals)

Focus only on high-impact variables (max 3 per scenario).

---

### Step 3: Define Scenario
Create a structured scenario:

Format:
- Scenario Name:
- Variable Change:
- Duration/Impact Change:
- Time Window (if applicable):

Example:
- Resource A unavailable for 3 days starting Day 10

---

### Step 4: Modify Project Model

If Excel:
- Adjust input cells (duration/resource %)
- Use:
  - Scenario Manager
  - Data Tables

If MS Project / Primavera:
- Duplicate baseline
- Modify:
  - Task duration
  - Resource allocation
  - Dependencies if needed

---

### Step 5: Simulate Impact
Recalculate project plan and capture:
- New project duration
- Critical path changes
- Cost variation
- Delayed milestones

---

### Step 6: Compare with Baseline
Create structured comparison:

| Metric | Baseline | Scenario |
|--------|----------|----------|
| Duration |        |          |
| Cost |            |          |
| Critical Path |   |          |

---

### Step 7: Evaluate Acceptability
Decide:
- Acceptable → proceed with scenario plan
- Not acceptable → propose mitigation:
  - Add resources
  - Re-sequence tasks
  - Increase buffer

---

### Step 8: Recommend Action
Always provide:
- Impact summary
- Decision recommendation
- Optional mitigation strategies

---

## Output Format

Return results in this structure:

### Scenario Summary
- Scenario:
- Key Change:

### Impact Analysis
- Duration Change:
- Cost Impact:
- Critical Path Impact:

### Recommendation
- Decision:
- Suggested Actions:

---

## Rules

- Do NOT simulate without a baseline
- Limit scenarios to avoid combinatorial explosion
- Prefer clarity over complexity
- Always quantify impact (time/cost)
- If data is missing → ask user before proceeding

---

## Notes

- This is deterministic scenario analysis (WISA)
- For probabilistic analysis, suggest Monte Carlo simulation
- Best used during planning and scheduling phase

---

## Validation

Before finalizing:
- Ensure dependencies are preserved
- Check calculations consistency
- Validate assumptions with user context
- Confirm outputs are realistic (no negative durations, etc.)