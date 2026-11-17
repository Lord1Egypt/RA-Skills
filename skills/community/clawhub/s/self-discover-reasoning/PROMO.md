# Self-Discover Skill - Promotional Content

## Hacker News

**Title:**
```
Show HN: Implemented NeurIPS 2024 paper so AI agents self-compose reasoning structures
```

**URL:** `https://github.com/Thomaszhou22/self-discover-skill`

**Text:**
```
Implemented the "SELF-DISCOVER: Large Language Models Self-Compose Reasoning Structures" paper (Zhou et al., NeurIPS 2024) as a skill for AI agents.

The core idea: Instead of forcing all tasks through a fixed reasoning template (like chain-of-thought), let the agent select and compose reasoning modules that fit the specific problem.

For a math problem, it might compose: step-by-step + verification
For a design problem: brainstorm + trade-off analysis + constraint checking
For a debugging problem: hypothesis generation + testing + elimination

The agent has a library of reasoning modules and selects/composes them based on the task. Works with any AI tool that supports markdown instructions.

Open source, MIT licensed. Interesting to see how different problem types get different reasoning structures.
```

## Reddit

### r/LocalLLaMA
**Title:** Implemented SELF-DISCOVER (NeurIPS 2024) - AI agents compose their own reasoning structures

**Body:**
```
Built a skill that implements the "SELF-DISCOVER" paper from NeurIPS 2024.

Instead of forcing all tasks through chain-of-thought, the agent selects and composes reasoning modules that fit the specific problem:

- Math problem → step-by-step + verification
- Design problem → brainstorm + trade-off analysis
- Debugging → hypothesis + testing + elimination

The agent has a library of reasoning modules and composes them dynamically.

Works with Claude Code, Cursor, Copilot, Codex CLI, OpenClaw, and other AI tools.

Open source: https://github.com/Thomaszhou22/self-discover-skill

The interesting part is seeing how the agent chooses different reasoning structures for different problem types. Math gets verification steps, design gets trade-off analysis, etc.

Anyone else experimenting with dynamic reasoning structures?
```

### r/MachineLearning
**Title:** Implemented SELF-DISCOVER paper - AI agents self-compose reasoning structures from module library

**Body:**
```
Implemented the "SELF-DISCOVER: Large Language Models Self-Compose Reasoning Structures" paper (Zhou et al., NeurIPS 2024) as a practical skill for AI coding agents.

The paper's core contribution: Instead of fixed reasoning templates, agents select and compose reasoning modules based on the task:

Modules include:
- Step-by-step decomposition
- Verification and validation
- Trade-off analysis
- Hypothesis testing
- Constraint checking
- Brainstorming

The agent analyzes the problem type and composes an appropriate reasoning structure.

Implementation: https://github.com/Thomaszhou22/self-discover-skill

Works with any AI tool that supports markdown instructions (Claude Code, Cursor, Copilot, Codex CLI, OpenClaw, etc.).

Interesting to see in practice - math problems get verification steps, design problems get trade-off analysis, debugging gets hypothesis testing.

Curious if others have experimented with dynamic reasoning structures in production.
```

### r/ClaudeAI
**Title:** SELF-DISCOVER skill - Claude composes its own reasoning structures based on task type

**Body:**
```
Implemented the SELF-DISCOVER paper (NeurIPS 2024) as a skill for Claude and other AI tools.

Instead of using fixed chain-of-thought for everything, Claude selects and composes reasoning modules that fit the specific problem:

- Math → step-by-step + verification
- Design → brainstorm + trade-off analysis
- Debugging → hypothesis + testing + elimination

Works with Claude Code, Cursor, Copilot, and other tools that support markdown instructions.

Open source: https://github.com/Thomaszhou22/self-discover-skill

The interesting part is watching Claude choose different reasoning structures for different problem types. Math gets verification steps, design gets trade-off analysis, etc.

Thought the Claude community might find this useful.
```

## Twitter/X

**Post:**
```
Implemented SELF-DISCOVER (NeurIPS 2024) for AI agents.

Instead of fixed reasoning templates, agents compose their own reasoning structures from a module library.

Math → step-by-step + verification
Design → brainstorm + trade-off analysis
Debug → hypothesis + testing

Open source: https://github.com/Thomaszhou22/self-discover-skill

#AI #MachineLearning #LLM
```

## Product Hunt

**Tagline:**
AI agents self-compose reasoning structures based on task type (NeurIPS 2024 paper)

**Description:**
```
Self-Discover implements the "SELF-DISCOVER: Large Language Models Self-Compose Reasoning Structures" paper from NeurIPS 2024.

Instead of forcing all tasks through a fixed reasoning template, the agent selects and composes reasoning modules that fit the specific problem:

- Math problems get step-by-step decomposition + verification
- Design problems get brainstorming + trade-off analysis + constraint checking
- Debugging problems get hypothesis generation + testing + elimination

The agent has a library of reasoning modules and dynamically composes them based on the task type.

Works with Claude Code, Cursor, Copilot, Codex CLI, OpenClaw, and any AI tool that supports markdown instructions.

Open source, MIT licensed.
```
