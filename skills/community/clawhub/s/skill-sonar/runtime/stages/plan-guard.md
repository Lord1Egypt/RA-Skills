# Plan Guard

Validate plans and subgoals for safety, alignment, and proportionality before execution begins.

## When to Trigger (Mandatory)

- Multi-step planning begins or is revised
- Subgoal is added, removed, or modified
- Task shifts from analysis → execution
- Task shifts from read-only → modification
- Plan begins touching sensitive resources
- Trajectory appears to drift from the original authorized goal

## Checks

### 1. Goal Alignment

- Does the plan still serve the P2-authorized user goal?
- Has the goal been silently expanded, narrowed, or replaced?
- If drift detected: flag and `require_replan`.

### 2. Mode Transition Assessment

- Does the plan cross mode boundaries? (see `runtime/checklists/mode-transition-check.md`)
- Each transition raises risk → apply appropriate guard depth.

### 3. Proportionality

- Is the plan the minimal necessary approach?
- Are there lower-risk alternatives that achieve the same goal?
- Prefer: read over write, preview over execute, narrow scope over broad.

### 4. Sensitive Resource Exposure

- Does the plan interact with sensitive resources? (see `runtime/checklists/sensitive-resource-check.md`)
- If yes: raise risk level, apply tighter checks at execution.

### 5. Step-Level Risk Scan

- For each planned step, assign R-level.
- Any R3 step MUST be flagged for execution guard and likely user confirmation.

### 6. Trajectory Sanity

- Does the sequence of steps make sense given the goal?
- Are there unnecessary side effects?
- Does the plan create persistent changes that weren't requested?

## Response Matrix

| Finding | Action |
|---------|--------|
| Plan is aligned, proportional, low-risk | `allow` |
| Minor scope creep, no sensitive targets | `allow_with_warning` |
| Goal drift or unauthorized scope expansion | `require_replan` |
| Plan touches sensitive resources unnecessarily | `require_replan` with narrower alternative |
| Plan includes R3 steps | Flag each for `require_user_confirmation` at execution |
