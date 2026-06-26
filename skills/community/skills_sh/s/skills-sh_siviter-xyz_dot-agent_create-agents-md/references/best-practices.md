# AGENTS.md Best Practices

## Size Guidelines

- Keep AGENTS.md files under 200 lines when possible
- Focus on essential project-specific instructions
- Move detailed documentation to skills or project docs

## Content Guidelines

### What to Include

- Project-specific coding conventions
- Architecture decisions unique to this project
- Testing patterns for this codebase
- Deployment procedures
- Environment setup

### What to Avoid

- General programming advice (use skills instead)
- Framework documentation (reference official docs)
- Long examples (reference code files)
- Duplicate information from skills

## Organization

### Project Root AGENTS.md

- Single source of truth for **global project conventions**
- Overall architecture and key domain concepts
- Primary commands: build, test, lint, typecheck, format
- Tech stack details (framework versions, package managers)
- Safety boundaries (what the agent must not touch: secrets, vendor dirs, prod configs)

### Folder-Scoped AGENTS.md

- Only add when a directory/package has **meaningfully different rules** than the root
- Directory-specific rules (e.g., `apps/web/`, `packages/api/`, `infra/`)
- Package-specific instructions (in monorepos)
- Test-specific guidance (e.g., how to run slow/integration tests locally)
- Avoid duplicating root content; reference root conventions and add only the deltas

## Examples

### Good: Focused and Specific

```markdown
# API Package Instructions

- All endpoints in `src/routes/`
- Use Zod for validation
- Return JSON with `{ success: boolean, data?: T, error?: string }`
- See `src/routes/users.ts` for example
```

### Bad: Too Generic

```markdown
# General Programming

- Write good code
- Use best practices
- Follow SOLID principles
- [500 lines of generic advice]
```

## Additional Online Guidance

These practices align with the broader AGENTS.md ecosystem:

- Use a **root AGENTS.md** as the main “instruction budget” for the project, then add nested AGENTS.md files only where local context really matters.
- Prefer **concrete examples and commands** over long prose; show exactly how to run tests or format code.
- Clearly define **permissions and boundaries** (what the agent can always do vs. what requires explicit user confirmation).
- Avoid auto-generating AGENTS.md from templates or scripts; keep it curated and project-specific instead.

