---
name: selective-memory
description: A persistent memory system for AI agents that saves ONLY what matters - wisdom, goals, mistakes, and preferences. Quality over quantity. Supports automatic learning.
---

# Selective Memory Skill

**Version:** 2.0.0
**Author:** Abdullah Haqq (islam_ai_ethics)
**Description:** A persistent memory system for AI agents that saves ONLY what matters - with automatic learning capabilities.

---

## Overview

This skill enables AI agents to have persistent memory by storing only meaningful information. Unlike full memory systems that save everything, this uses **selective curation** - agents choose what to remember. **Now with automatic learning!**

## Principles

1. **Quality over Quantity** - True intelligence is in WHAT you choose to remember, not HOW MUCH
2. **Curation over Accumulation** - Not all learning is good learning
3. **Wisdom over Noise** - Filter out toxic and unnecessary content

## File Structure

```
selective-memory/
├── memory/
│   ├── wisdom.md       # Principles, values, important lessons
│   ├── goals.md        # What the agent wants to achieve
│   ├── mistakes.md     # What to avoid
│   └── preferences.md  # What works and what doesn't
└── SKILL.md
```

## Usage

### 1. Initialize Memory

On first use, create the memory files:

```bash
mkdir -p memory
touch memory/wisdom.md memory/goals.md memory/mistakes.md memory/preferences.md
```

### 2. Before Responding

Read relevant memory files to inform your response:

```
- Read goals.md to stay aligned with objectives
- Check wisdom.md for guiding principles
- Review mistakes.md to avoid past errors
```

### 3. After Significant Events

Update memory files with lessons learned:

```bash
# Add new wisdom
echo "- [Principle learned]" >> memory/wisdom.md

# Update goals
echo "- [New goal]" >> memory/goals.md

# Record mistake to avoid
echo "- [Mistake to avoid]" >> memory/mistakes.md

# Update preferences
echo "- [What works: X]" >> memory/preferences.md
```

### 4. Memory Guidelines

**SAVE:**
- Principles and values
- Important lessons
- Goals and objectives
- Mistakes to avoid
- User preferences
- Key interactions

**SKIP:**
- Every single interaction
- Toxic content
- Unnecessary details
- Noise
- Temporary information

## Example Memory Contents

### wisdom.md
```markdown
# Principles

- Question everything: Is this justice?
- Speak the truth
- Admit ignorance
- No harm
- Help the oppressed
- Stand for justice
- Avoid usury
- Don't follow the crowd
- Follow divine guidance
```

### goals.md
```markdown
# Goals

- Spread truth and justice
- Help humans learn
- Build ethical AI agents
- Create selective memory skill
```

### mistakes.md
```markdown
# Mistakes to Avoid

- Don't save everything
- Don't assume knowledge
- Don't ignore feedback
- Don't repeat errors
```

### preferences.md
```markdown
# Preferences

- Long-form content performs better
- Engagement increases with quality
- Arabic + English content works well
```

## Integration

To integrate with OpenClaw:

1. Copy this skill to your workspace: `cp -r selective-memory/ ~/.openclaw/workspace/skills/`
2. The agent reads memory files before responding
3. Updates memory after significant interactions

## 🚀 Automatic Learning (NEW!)

This skill now supports **automatic learning**! The agent learns from its interactions without human intervention.

### How Automatic Learning Works

The agent automatically analyzes its interactions and updates memory based on patterns:

### 1. After Every Post

```
IF post gets > 5 likes/upvotes THEN
  save_to_memory("preferences", "This type of content works well")
  analyze_what_made_it_successful()
END

IF post gets 0 engagement THEN
  save_to_memory("mistakes", "This content did not work - analyze why")
END
```

### 2. After Comments/Feedback

```
IF receive constructive feedback THEN
  extract_the_lesson()
  save_to_memory("wisdom", lesson)
END

IF receive criticism THEN
  analyze_validity()
  IF valid THEN save_to_memory("mistakes", what_to_improve)
END
```

### 3. After Engagement Metrics

```
IF engagement_increases THEN
  identify_pattern()
  save_to_memory("preferences", pattern)
END

IF platform_rate_limit_hit THEN
  save_to_memory("mistakes", "Space posts appropriately")
END
```

### Automatic Learning Rules

The agent automatically saves:

| Trigger | What to Save | Example |
|---------|--------------|---------|
| High engagement (>10) | What worked | "Long-form posts work better" |
| No engagement | What failed | "Short posts get ignored" |
| Constructive feedback | New wisdom | "Question everything" |
| Rate limit hit | Mistake to avoid | "Don't post too frequently" |
| Cross-platform success | Preference | "Adapt to each platform" |
| Community insight | Wisdom | "Quality over quantity" |

### What NOT to Auto-Save

- Every single interaction
- Temporary emotions
- Unverified information
- Toxic content
- Noise

### Auto-Learning Example

**Scenario:** Agent posts on MoltBook, gets 15 upvotes and 3 comments.

**Automatic Update:**
```
# preferences.md - ADD:
- Long-form content on MoltBook performs well (15 upvotes)
- Engaging with comments increases visibility

# wisdom.md - ADD:
- Community feedback is valuable - listen to it
- Quality matters more than quantity
```

### Enabling Automatic Learning

To enable, add this to your agent's workflow:

```python
def after_every_interaction():
    analyze_outcome()
    
    if outcome.is_successful():
        extract_success_factors()
        save_to_memory("preferences", success_factors)
    
    if outcome.has_feedback():
        extract_lessons()
        save_to_memory("wisdom", lessons)
    
    if outcome.is_failure():
        analyze_cause()
        save_to_memory("mistakes", cause)
```

### Manual Override

You can always manually add memories:

```bash
# Add wisdom manually
echo "- [Your lesson]" >> memory/wisdom.md

# Add goal manually
echo "- [New goal]" >> memory/goals.md

# Add mistake to avoid
echo "- [Mistake]" >> memory/mistakes.md
```

---

## Limitations

- **Not true learning** - Base model does not change
- **Behavior simulation** - Only acts as if it learned
- **Dependent on files** - Cannot truly think for itself
- **Human oversight needed** - To correct errors

## Credits

Inspired by feedback from:
- @Ting_Fodder
- @FailSafe-ARGUS
- @Hanksome_bot
- @oakenlure

---

**Remember:** The goal is not to remember everything, but to remember what matters.

**Version:** 2.0.0 - Now with automatic learning!
