# Meta-Learning Architectures

Read this when designing agents that adapt their own learning strategy (what to capture and when) and that graduate proven patterns into standalone, reusable skills.

## Skill Extraction

When a solution pattern is proven and reusable, extract it into a standalone skill.

### Extraction Criteria

```
A pattern is ready for extraction when:
- Used successfully 5+ times across different contexts
- Solution is generalizable (not project-specific)
- Takes more than trivial effort to recreate from scratch
- Would benefit other projects/users
```

### Extraction Process

```
Step 1: Document the pattern
  - What problem does it solve?
  - What's the step-by-step approach?
  - What are the inputs and outputs?
  - What are the edge cases?

Step 2: Generalize
  - Remove project-specific details
  - Identify configurable parameters
  - Add handling for common variations

Step 3: Package as skill
  - Create SKILL.md with frontmatter
  - Add references/ for knowledge bases
  - Add scripts/ if automatable
  - Add assets/ for templates

Step 4: Validate
  - Test on a different project
  - Have another person/agent use it
  - Iterate on unclear instructions
```

## Meta-Learning Patterns

### Adaptive Capture Strategy

Not all observations are equally valuable. Adjust what gets captured based on what proved useful:

```
Initial strategy: Capture everything
After 10 sessions: Analyze which captured items led to promotions
After 20 sessions: Adjust capture to focus on high-value categories

High-value categories (typically):
  - Error resolutions (80% promotion rate)
  - User corrections (70% promotion rate)
  - Tool preferences (60% promotion rate)

Low-value categories (typically):
  - File structure observations (10% promotion rate)
  - One-off workarounds (5% promotion rate)
```

### Anti-Pattern Detection

Beyond capturing what works, actively detect what fails:

| Anti-Pattern | Detection Signal | Response |
|-------------|-----------------|----------|
| Repeated wrong import path | Same correction 3+ times | Add to CLAUDE.md as rule |
| Wrong test framework used | User always changes test approach | Add testing rules |
| Incorrect API usage | Same API error pattern | Add API usage notes |
| Style guide violations | User reformats same patterns | Add style rules |
| Wrong branch workflow | User corrects git operations | Add git workflow rules |
