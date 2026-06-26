# AI Memory Guard 🛡️

[中文文档](./README.md)

**Prevent memory loss in AI Agents.** A safety net against context gaps, designed from real memory failure incidents.

## The Problem

AI Agents suffer from memory loss:
- Long conversations → early context forgotten
- Session restarts → everything lost
- Token limits → important info truncated
- No warning when memory gaps occur

## The Solution

Memory Guard provides:

1. **Memory Checkpoints** - Auto-save critical information at key moments
2. **Gap Detection** - Alert when context continuity breaks
3. **Recovery Protocol** - Steps to restore lost context
4. **Memory Audit** - Track what was remembered vs. forgotten

## Quick Start

```markdown
# In your SKILL.md

## Memory Guard Protocol

Before important actions:
1. Check memory state: `memory_check()`
2. If gap detected → pause and recover
3. Save checkpoint after critical decisions
```

## Based on Real Failures

This skill was designed after experiencing actual memory loss events where AI Agents:
- Forgot user preferences mid-conversation
- Lost track of multi-step tasks
- Repeated questions already answered
- Made decisions contradicting earlier context

## Use Cases

- Long-running AI Agent sessions
- Multi-turn complex tasks
- Critical decision-making workflows
- Any scenario where memory continuity matters

## License

MIT
