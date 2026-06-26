# {{skill_name}}

**Multi-step process skill with decision trees for [purpose].**

## When to Use

This skill activates for complex workflows requiring decisions:
- [Scenario 1: Multiple possible paths]
- [Scenario 2: Conditional logic required]
- [Scenario 3: Error handling with fallbacks]

## Core Principles

- **Branching Logic:** Every decision point must have clear conditions
- **Fallback Ready:** Always define what happens when a branch fails
- **State Awareness:** Track workflow state across steps
- **User Confirmation:** Pause at critical decision points for user input

## Workflow

```
Start
  |
  v
[Step 1: Initial Assessment]
  |
  +--[Condition A met?]--YES--> [Branch A] --> [Step 3]
  |
  +--[Condition B met?]--YES--> [Branch B] --> [Step 3]
  |
  +--[Neither]------------> [Fallback] --> [Step 3]
  |
  v
[Step 3: Synthesize Results]
  |
  v
[Step 4: Present Options / Request Confirmation]
  |
  v
End
```

### Step-by-Step

#### Step 1: [Name]
- **Input:** [What information is needed]
- **Action:** [What to do]
- **Output:** [What to produce]

#### Step 2: [Decision Point]
- **Condition A:** [When to take path A]
  - **Branch A:** [Actions]
- **Condition B:** [When to take path B]
  - **Branch B:** [Actions]
- **Fallback:** [When neither condition is met]

#### Step 3: [Synthesis]
- Combine results from all branches
- Identify conflicts or gaps
- Prepare final options

#### Step 4: [Confirmation Gate]
- Present findings to user
- Explain decision rationale
- Request explicit confirmation before final action

## Decision Matrix

| Situation | Condition | Action | Fallback |
|-----------|-----------|--------|----------|
| [Case 1] | [Check] | [Do this] | [If fails] |
| [Case 2] | [Check] | [Do this] | [If fails] |

## Examples

### Example 1: Happy Path

**User:** *"[Request that matches Condition A]"*

**Skill:**
1. Step 1: Assess input ✅ Condition A met
2. Step 2: Take Branch A
3. Step 3: Synthesize results
4. Step 4: Present results, wait for confirmation

### Example 2: Fallback Path

**User:** *"[Request matching neither condition]"*

**Skill:**
1. Step 1: Assess input ⚠️ No primary condition met
2. Step 2: Execute Fallback branch
3. Step 3: Prepare alternative options
4. Step 4: Present alternatives, ask user preference

### Example 3: Error Recovery

**User:** *"[Request that fails during processing]"*

**Skill:**
1. Step 1-2: Attempt normal flow
2. Error detected in Step 2
3. Trigger fallback (don't crash)
4. Present error + recovery options
5. User confirms recovery path

## Safety & Boundaries

### NEVER
- Skip confirmation gates on destructive actions
- Assume user intent when conditions are ambiguous
- Execute irreversible operations in fallback branches without extra confirmation

### ALWAYS
- Log which branch was taken (for debugging/learning)
- Provide clear "why" when taking fallback paths
- Offer escape hatch: "Soll ich abbrechen oder einen anderen Weg versuchen?"

### Error Handling
- **Detection:** Check return values / exceptions at every step
- **Reporting:** Explain what failed and why in user-friendly terms
- **Recovery:** Always propose at least one recovery option
- **Escalation:** If all options exhausted → "Ich kann das nicht sicher abschließen. Sollen wir [X] oder [Y] versuchen?"

## State Tracking

Maintain workflow state across steps:

```
state = {
    "step": current_step_number,
    "branch_taken": "A|B|fallback",
    "inputs": {...},
    "intermediate_results": {...},
    "user_choices": [...],
    "errors_encountered": [...]
}
```

## Metadata

- **Version:** 1.0.0
- **Created:** {{date}}
- **Complexity:** High (requires state tracking)
- **Tags:** [workflow, branching, decision-tree]
