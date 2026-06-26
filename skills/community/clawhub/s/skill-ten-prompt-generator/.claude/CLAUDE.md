# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Prompt Engineering Skills System** - a collection of 10 specialized agent skills for AI prompt engineering across different domains. Each skill is an expert in its specific scenario, providing structured frameworks, best practices, and templates for crafting effective AI prompts.

## Project Structure

```
skill-ten-prompt-generator/
├── .claude/
│   ├── CLAUDE.md                    # This file
│   ├── SKILL_ROUTING.md             # Scenario routing guide with decision trees
│   └── skills/                      # 10 specialized agent skills
│       ├── video-prompt-generator/
│       ├── image-prompt-generator/
│       ├── coding-prompt-assistant/
│       ├── json-prompt-architect/
│       ├── data-analyst-prompter/
│       ├── humanizing-expert/
│       ├── creative-writing-coach/
│       ├── research-agent/
│       ├── voice-conversation-coach/
│       └── long-running-orchestrator/
├── skills.md                        # Agent Skills documentation (Chinese)
├── prompt_new.md                    # Comprehensive prompt guide (Chinese)
└── README.md (if present)
```

## The 10 Skills

Each skill is a self-contained expert with its own `skill.md` file containing:

1. **video-prompt-generator** - AI video generation prompts (Sora 2, Veo 3.1). 7-layer structure, camera movement terminology, physics description.
2. **image-prompt-generator** - AI image generation prompts (Flux, Midjourney, Nano Banana). Work-order protocol, S-E-L-C framework.
3. **coding-prompt-assistant** - AI programming prompts (Cursor, Claude Code). .cursorrules, TDD flow, Plan-Review-Execute.
4. **json-prompt-architect** - Structured JSON prompt design. Schema design, modular templates, negative constraints.
5. **data-analyst-prompter** - Data analysis prompts. Code execution mode, metadata injection, EDA-first.
6. **humanizing-expert** - De-AI text processing. Negative word lists, style cloning, burstiness injection.
7. **creative-writing-coach** - Creative writing & roleplay. Corpus injection, cognitive modeling, inner monologue.
8. **research-agent** - Deep research & search. Recursive planning, source hierarchy, critical red-teaming.
9. **voice-conversation-coach** - Real-time voice/dialogue. Brevity protocol, recast correction, pressure interview.
10. **long-running-orchestrator** - Long-running agents. Initialization-execution separation, state serialization.

## Skill Routing Logic

When users request help with prompt engineering, identify their scenario using the decision tree in `SKILL_ROUTING.md`:

```
User Request
    ↓
[Keyword Matching]
    ↓
Video/Sora/Veo          → video-prompt-generator
Image/Flux/MJ           → image-prompt-generator
Programming/Cursor      → coding-prompt-assistant
JSON/Structured         → json-prompt-architect
Data analysis/Python    → data-analyst-prompter
De-AI/Humanizing        → humanizing-expert
Writing/Roleplay        → creative-writing-coach
Research/Search         → research-agent
Voice/Dialogue          → voice-conversation-coach
Agent/Long-running      → long-running-orchestrator
```

## When to Use This System

Invoke the appropriate skill when users ask for:

- Video generation prompts (Sora, Veo, Runway)
- Image generation prompts (Flux, Midjourney, Stable Diffusion)
- .cursorrules or programming assistance
- JSON schema design for prompts
- Data analysis workflows
- Making AI text sound more human
- Roleplay or creative writing
- Research methodology
- Voice conversation setup
- Long-running agent design

## Key Concepts

### Structured Prompting
All skills emphasize **structured approaches** over free-form natural language:
- Video: 7-layer structure (Subject, Action, Environment, Camera, Lighting, Style, Technical)
- Image: S-E-L-C framework (Subject, Environment, Lighting, Camera)
- Coding: P-R-E pattern (Plan-Review-Execute)

### Negative Constraints
Most skills include negative prompt engineering:
- Video: Avoid morphing, distortion, frozen backgrounds
- Image: Worst quality, distortion, bad anatomy
- Humanizing: Blacklist for "AI-ese" words (delve, leverage, tapestry)

### Framework-Based Workflows
- **TDD Prompting**: Write tests first, then implementation
- **Work-Order Protocol**: What to change, what to change to, what to keep same
- **State Serialization**: Checkpoints for long-running tasks

## File Conventions

- Each skill has a `skill.md` file with YAML frontmatter (name, description)
- Skills are discovered automatically by Claude Code from `.claude/skills/`
- Descriptions should include trigger keywords for routing
- Use semantic naming (e.g., `camera_movement_type` not `cmt`)

## Language Considerations

- Documentation files are primarily in Chinese (skills.md, prompt_new.md)
- Skill content is in Chinese for better local context
- Code examples and technical terms remain in English
- When invoking skills, be prepared for Chinese output

## Common Development Tasks

There are no build, test, or lint commands for this repository. It's a documentation/skills system.

When adding or modifying skills:
1. Create/edit the skill directory under `.claude/skills/`
2. Include proper YAML frontmatter with `name` and `description`
3. Update `SKILL_ROUTING.md` if adding new categories
4. Update this file if architecture changes significantly
