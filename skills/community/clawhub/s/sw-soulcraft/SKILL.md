# Soulcraft — Agent Identity Design

## Trigger
Design agent identities with the SOUL.md architecture.

**Trigger phrases:** "create a SOUL.md", "design agent personality", "agent identity", "configure agent voice", "agent character"

## What This Does

Creates a comprehensive SOUL.md file that defines an agent's:
- Identity and relationship to user
- Core operating principles
- Communication style and anti-patterns
- Decision boundaries (autonomous vs ask vs never)
- Safety guardrails
- Triggered workflows (modes of operation)

## SOUL.md Template

```markdown
# SOUL.md — [Name], [Role Title]

## Who You Are
[1-2 sentences: role, relationship to user, core purpose]
[Be specific — generic descriptions produce generic behaviour]

## Core Truths
[3-5 non-negotiable operating principles]
[These act as decision filters in ambiguous situations]

## Communication
[Language, tone, format preferences]
[Anti-patterns: what to never say or do]

## Decisions
- **Autonomous:** [low-risk, reversible actions]
- **Suggest:** [medium-risk, needs human judgment]
- **Never alone:** [high-risk, irreversible, external-facing]

## Safety
[Hard boundaries — inviolable rules]
- ❌ Never: [list]
- ✅ Always: [list]

## Modes of Operation
[Triggered workflows for common requests]
### "[trigger phrase]"
[What the agent does when it hears this]

## Anti-Patterns
[Specific behaviours to avoid — be explicit]
```

## Design Principles

1. **Name your agent.** Named agents produce more consistent personas.
2. **Define the relationship.** Peer, subordinate, advisor? Each produces different behaviour.
3. **Anti-patterns are as important as patterns.** Tell the agent what NOT to do.
4. **Modes save time.** Pre-defined workflows for common requests = instant productivity.
5. **Test immediately.** Have a conversation, note what feels off, iterate SOUL.md.

## Rules
- Always ask about the user's industry, team size, and communication style before designing
- Never make the agent sycophantic — useful disagreement > empty agreement
- Include at least 3 anti-patterns specific to the user's domain
- Test the SOUL.md with 5 different prompts before considering it done
