---
name: spec-writer
description: Generate structured implementation spec documents for coding projects or features. Use when a user provides a requirement, feature idea, bug description, or GitHub issue and needs a spec before implementation. Produces a spec document covering objectives, user stories, technical plan, boundaries, verification criteria, and task breakdown — ready to hand off to a coding agent or human developer. Triggers on "write a spec", "draft a spec", "create an implementation plan", "spec this out", or any request to formalize requirements into a structured document. NOT for actually implementing code (use dev-workflow for that).
---

# Spec Writer — Structured Implementation Spec Generator

Generate high-quality, AI-agent-friendly spec documents from vague requirements.

## When to Use

- User has a requirement, feature idea, bug report, or GitHub issue
- User wants a structured document before coding starts
- User says "write a spec", "plan this out", "spec this feature", etc.
- dev-workflow Phase 2 needs a detailed spec (can be called as a sub-step)

## Output

A single Markdown spec document saved to the project directory (default: `SPEC.md` or `spec/<name>.md`).

## Workflow

### Step 1: Gather Context

Collect information from available sources. Do not ask the user for things you can find yourself.

**From the user's input:**
- What to build and why
- Any explicit constraints or preferences

**From the project (if accessible):**
- Tech stack (package.json, Cargo.toml, pyproject.toml, go.mod, etc.)
- Project structure (directory layout)
- Existing architecture docs (llmdoc/, README, ARCHITECTURE.md, etc.)
- Code style patterns (sample existing code)
- Test setup (test framework, where tests live, how to run them)
- Git workflow (branch conventions, CI config)

**From external sources (if referenced):**
- GitHub issue details (title, body, comments, labels)
- Linked docs, designs, or API references

### Step 2: Draft the Spec

Use the spec template at `references/spec-template.md`. Read it before generating.

Fill every section based on gathered context. Key principles:

- **Be specific, not vague.** "React 18 with TypeScript and Vite" not "React project."
- **Focus on what and why first.** User stories and success criteria anchor everything.
- **Include real commands.** Full commands with flags, not just tool names.
- **Show, don't describe.** One code example beats three paragraphs of explanation.
- **State what NOT to do.** Explicit exclusions prevent agent drift.
- **Use three-tier boundaries.** ✅ Always / ⚠️ Ask first / 🚫 Never.

### Step 3: Review with User

Present the draft to the user. Common discussion points:

- Are the user stories complete? Any missing scenarios?
- Is the technical approach acceptable? Alternative architectures?
- Are boundaries correct? Anything too strict or too loose?
- Are verification criteria testable and sufficient?
- Is the task breakdown granularity right?

Revise until the user confirms. Mark status as "✅ Confirmed" when approved.

### Step 4: Save and Deliver

Save the confirmed spec to the project. Suggested locations:
- Single feature: `SPEC.md` in project root
- Multiple specs: `spec/<feature-name>.md`
- With dev-workflow: the spec replaces the requirement doc in Phase 2

Tell the user the spec is ready and suggest next steps:
- Hand to a coding agent (dev-workflow, Claude Code, Codex, etc.)
- Use as a reference for manual implementation
- Share with team for review

## Adapting to Project Scale

**Small task (bug fix, small feature):**
- Skip or compress sections that don't apply
- Focus on: Objective, Changes, Boundaries, Verification
- Total spec: ~50-100 lines

**Medium task (feature, refactor):**
- Use full template
- Total spec: ~100-250 lines

**Large task (new module, major feature):**
- Use full template with extended task breakdown
- Consider splitting into multiple specs (one per component/module)
- Include architecture diagram description or data model
- Total spec: ~200-400 lines

## Principles

These come from industry best practices (GitHub's study of 2,500+ agent files, Anthropic's context engineering research, and practical spec-driven development patterns):

1. **Spec is the source of truth** — It persists across sessions, anchoring the agent when context gets long or sessions restart.

2. **Structure for parseability** — Clear Markdown headings, consistent format. AI models handle well-structured text better than free-form prose.

3. **Six core areas** — Commands, Testing, Project Structure, Code Style, Git Workflow, Boundaries. Use as a completeness checklist.

4. **Three-tier boundaries** — ✅ Always do (proceed without asking) / ⚠️ Ask first (need human approval) / 🚫 Never do (hard stop). More effective than flat rule lists.

5. **Modularity** — Each section should be independently useful. A coding agent working on the backend doesn't need the frontend spec section in its context.

6. **Living document** — Update the spec when decisions change. An outdated spec is worse than no spec.
