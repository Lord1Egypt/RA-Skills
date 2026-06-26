---
name: adk-docs
description: guidelines for creating, reviewing, updating, and searching ADK documentation - use when users ask about writing, maintaining, or auditing ADK bot docs
license: MIT
---

# ADK Documentation Management

Use this skill when helping users create, review, update, or maintain documentation for their ADK projects. Users write guides and docs for their own bots and features — code examples should come from their project and the official ADK repo.

## When to Use This Skill

Activate this skill when users:

- Want to create documentation for their bot ("Document my order workflow", "Write a guide for my custom actions")
- Need to review existing project docs for accuracy ("Check if my docs are still correct")
- Want to update docs after changing their bot ("I refactored the checkout flow, update the docs")
- Need to check if docs are in sync with their code ("Are my docs current?")
- Want to search their project documentation ("Find docs about my payment handler")
- Ask about documentation standards or templates
- Mention `/adk-document`

## Available Documentation

| File                                                         | Description                                                       |
| ------------------------------------------------------------ | ----------------------------------------------------------------- |
| [references/doc-standards.md](./references/doc-standards.md) | Document types, templates, quality checklists, and health metrics |

## Available Commands

| Command (and suggested subcommand)               | Description                                           |
| ------------------------------------------------ | ----------------------------------------------------- |
| `/adk-document create [topic]`                   | Create documentation for a feature in the user's bot  |
| `/adk-document review [doc-path]`                | Review project docs for accuracy and completeness     |
| `/adk-document update [doc-path] [what-changed]` | Update project docs after code changes                |
| `/adk-document sync [optional-doc-path]`         | Check if project docs are in sync with the bot's code |
| `/adk-document search [search-term]`             | Search project documentation for specific topics      |

## Shared Principles

### 1. AI-Optimized Structure

- Clear section headers (`##`, `###`, `####`) so ripgrep can find sections
- Table of contents at top with anchor links
- Right-sized for document type (see doc-standards reference)
- Keyword-rich section names — no vague "Advanced Topics" or "Other"

### 2. Code-First Approach

- Every concept needs a working code example from actual project code
- Include file paths with line numbers for verification
- Primary sources for examples (in priority order):
  1. The user's own ADK project (look for `agent.config.ts` in the workspace) — BEST
  2. The official ADK repo examples (clone or find locally)
  3. ADK runtime usage (`@botpress/runtime` packages)
- Never invent or speculate examples — all code must be verifiable

### 3. Critical Distinctions

- ADK primitives (from `@botpress/runtime`) vs Botpress SDK primitives
- `this.send()` in conversations vs `client.createMessage()` in workflows
- Messages (persistent, stored) vs Events (ephemeral, not stored)
- Agnostic APIs vs channel-specific features

### 4. No Speculation

- Do NOT add Common Mistakes or Best Practices sections unless the user explicitly provides them
- Use `❌ WRONG` / `✅ CORRECT` only when documenting actual reported errors
- Workflows and examples must be verified from actual code, not imagined

### 5. Writing Style

- **Direct and actionable** — "Use `this.send()`" not "You might want to consider..."
- **Technically accurate** — test examples against actual ADK code
- **Assumes intelligence** — provide context and guidance, not hand-holding
- **No marketing fluff** — straight to the technical substance

## How to Answer

When a user asks about documentation without invoking a specific command:

1. **Load the `adk` skill (& more, if needed)** for ADK context and knowledge
2. **Identify what they need** — creating, reviewing, updating, syncing, or searching
3. **Point them to the right command** or help directly using the principles above
4. **Reference doc-standards** for template and quality guidance

## Documentation Location

Documentation is written in the user's own project. Ask the user where they want docs saved if not obvious (common locations: `./docs/`, `./guides/`, or project root).

## Discovering Code Sources

Discover the user's project and the official ADK repo for examples:

```javascript
// Find ADK projects in the workspace
Glob({ pattern: '**/agent.config.ts' })

// Find ADK runtime usage in the user's project
Grep({ pattern: 'from [\'"]@botpress/runtime', output_mode: 'files_with_matches' })

// Look for existing project documentation
Glob({ pattern: './{docs,guides}/**/*.md' })

// Find official ADK examples if available locally
Glob({ pattern: '**/adk/examples/**/*.ts' })
```

## Cross-References

- **`adk` skill** — Core ADK knowledge (actions, workflows, conversations, etc.)
- **`adk-evals` skill** — Testing and eval documentation
- **`adk-frontend` skill** — Frontend integration documentation
- **`adk` skill `integrations.md` reference** — Integration lifecycle documentation
