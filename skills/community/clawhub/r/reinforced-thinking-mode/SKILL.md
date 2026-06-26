---
name: reinforced-thinking-mode
description: Multi-round independent deep thinking. Each round produces complete, final-quality solutions. Non-iterative, no TODOs, no angle constraints—pure divergent thinking.
---

# Reinforced Thinking Mode

## When to Use

Activate when user needs deep, multi-angle analysis:
- Keywords: "deep thinking", "multi-angle", "comprehensive evaluation", "design solution", "architecture planning"
- Intent: Complex system design, strategic decisions, innovation, risk assessment

**Complexity → Rounds:**
- Simple (factual, clear): 2-3 rounds
- Medium (feature design, trade-offs): 4-5 rounds
- Complex (architecture, strategy): 5-7 rounds
- Wicked (undefined, conflicting): 7-10 rounds

## Core Principle

**N independent, complete thinking sessions—not iterative refinement.**

Each round must be: *"If this were the last round, I am completely satisfied."*

### Mental Model

✅ **Think:** "This is my only chance—give it everything"

❌ **Never think:** "I'll improve this next round"

---

## Hard Constraints

### File Access
- **Each round reads ONLY:** `problem.md` + `round_{i-1}.md` (Round 1: only problem.md)
- **Never** read other rounds' details

### Forbidden Words
Never use in solution files: `TODO`, `to be improved`, `next round`, `later`, `refine further`

### Information Gaps
- Uncertain facts → Search immediately
- Uncertain requirements → Ask user immediately
- **Never** assume and continue

---

## Execution Flow

### Phase 1: Initialize

1. **Assess complexity** → Determine rounds (simple 2-3, medium 4-5, complex 5-7, wicked 7-10)
2. **Create directory** `reinforced-thinking/`
3. **Write problem definition** `problem.md`: background, current state, core problem, constraints, success criteria

---

### Phase 2: Iterate (Each Round)

For round X:

1. **Read files**: `problem.md` + `round_{X-1}.md` (Round 1: only problem.md)
2. **Reset mindset**: Think from a fresh angle, don't copy previous approach
3. **Choose angle freely**: Overturn previous round if necessary
4. **Write solution** `round_X.md`, including:
   - Independence declaration
   - Core insight
   - Solution design
   - Expected results
   - Risks and mitigations
   - Why solution is complete
5. **Self-review**: Check for forbidden words, completeness, executability
6. **If failed → Redo step 4
7. **Early termination check** (round 2+):
   - Compare core approach and solution with previous round
   - If similarity > 70%, lack of innovation → **Recommend early termination**
   - Write termination recommendation in current round for user decision

---

### Phase 3: Synthesize

1. Read all rounds + problem.md
2. Analyze unique value, conflicts, complements of each solution
3. **Red team review**: Critical examination of each solution
   - Assumption flaws: What assumptions does the solution rely on? What if they fail?
   - Vulnerability risks: Potential loopholes or bypasses?
   - Failure modes: In what scenarios will it fail?
   - Adversarial testing: If someone deliberately sabotages, where is the weakest point?
4. Generate final report `final_report.md` (including red team review conclusions)

### Phase 4: Cleanup

Automatically delete intermediate files (problem.md, round_*.md), only keep final_report.md.

If retention needed, specify in), only keep final prompt.

---

## Quality Assurance

### Mandatory Redo Rules

If ANY of these conditions trigger, MUST redo current round:
1. Contains forbidden words (TODO, to be improved, next round, later, refine further)
2. Not final quality, needs "future supplements"
3. Read files other than problem.md and round_{X-1}.md
4. Solution incomplete

### Checklist (Each Round)

- [ ] Chose different angle from previous round
- [ ] Did not copy previous solution
- [ ] No forbidden words
- [ ] If last round, I would be satisfied
- [ ] All details included, can implement directly
- [ ] Only read problem.md and previous round

---

## Common Errors and Fixes

| Error | Example | Fix |
|-------|---------|-----|
| Carry context | "Based on R1's UX and R2's tech..." | Only write "Based on problem.md and R3's approach..." |
| Leave TODOs | "Details next round" | Give core design details now |
| Assume facts | "Users probably want X" | Search to confirm or ask user |
| Preset direction | "Next round: security angle" | Let each round choose freely |
| Iterative thinking | "Improve on R1" | Each round is independent, think from scratch |
| No details | "See related docs" | Write complete details directly in file |

---

## Best Practices

- **Divergent thinking**: No angle matrix—choose any perspective freely
- **True independence**: Only read problem.md + previous round, not all history
- **All-out each round**: Don't hold back for "next iteration"
- **Transparency**: Show chosen angle and reasoning in each round
- **Early termination**: If 2 consecutive rounds lack innovation or similarity > 70% with previous round, recommend early termination
