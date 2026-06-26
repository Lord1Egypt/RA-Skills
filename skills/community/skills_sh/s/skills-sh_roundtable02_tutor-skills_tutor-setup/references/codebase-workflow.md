# Codebase Mode — Onboarding Vault Workflow

> Generates a StudyVault that helps new developers understand and navigate a source code project.
> All scanning and output MUST stay within CWD.

## Phase C1: Project Exploration

1. **Scan project structure**: `Glob` for source files, config files, test files. Build a file tree.
2. **Identify tech stack**: Detect languages, frameworks, build tools, package managers from config files.
3. **Read key files**: README, CONTRIBUTING, entry points (`main.*`, `index.*`, `app.*`), config files.
4. **Map project layout**: Record directory purposes (e.g., `src/`, `test/`, `config/`, `scripts/`).
5. **Present findings** to user for confirmation before proceeding.

## Phase C2: Architecture Analysis

1. **Identify architectural patterns**: layered, hexagonal, microservice, monolith, serverless, etc.
2. **Map module boundaries**: Which directories/packages form distinct modules or domains?
3. **Trace request flow**: For a typical request (HTTP, event, CLI), trace the path through the code.
4. **Identify key abstractions**: Interfaces, base classes, shared utilities, middleware, interceptors.
5. **Map dependencies**: Internal module dependencies + external service integrations.
6. **Document data flow**: How data enters, transforms, persists, and exits the system.
7. **Build architecture summary**: Create a concise diagram (ASCII) + description for the vault.

## Phase C3: Tag Standard

Define tag vocabulary before creating notes:
- **Format**: English, lowercase, kebab-case
- **Categories**: `#arch-*` (architecture), `#module-*` (modules), `#pattern-*` (patterns), `#config-*` (config), `#api-*` (API), `#test-*` (testing)
- **Registry**: Only registered tags allowed. Present registry to user for approval.

## Phase C4: Vault Structure

Create `StudyVault/` per [codebase-templates.md](codebase-templates.md) folder structure:
- `00-Dashboard/` — MOC, Quick Reference, Getting Started
- `01-Architecture/` — System overview, request flow, data flow
- `02-XX/` through `NN-XX/` — One folder per module/domain
- `NN+1-DevOps/` — Build, deploy, CI/CD, environment config
- `NN+2-Exercises/` — Onboarding exercises

## Phase C5: Dashboard Creation

Create `00-Dashboard/` with:

### MOC (Map of Content)
- **Architecture Overview**: Link to architecture notes
- **Module Map**: Table of all modules with purpose + links
- **API Surface**: Summary of endpoints/commands/events
- **Getting Started**: Setup instructions, dev workflow, key commands
- **Tag Index**: Tag registry with hierarchy rules
- **Onboarding Path**: Recommended reading order for new developers

### Quick Reference
- Key commands (build, test, deploy, lint)
- Environment setup steps
- Common debugging tips
- Important file locations

## Phase C6: Module Notes

One note per module/domain. Per [codebase-templates.md](codebase-templates.md). Key rules:

- YAML frontmatter: `module`, `path`, `keywords` (MANDATORY)
- **Purpose**: What this module does (1-3 sentences)
- **Key Files**: Table of important files with descriptions
- **Public Interface**: Exported functions/classes/endpoints
- **Internal Flow**: How data moves through this module (ASCII diagram)
- **Dependencies**: What this module depends on + what depends on it
- **Configuration**: Relevant env vars, config keys
- **Testing**: How to run tests for this module, test patterns used
- **Related Notes**: Links to related modules and architecture notes

For API-heavy modules, create separate API notes per [codebase-templates.md](codebase-templates.md).

## Phase C7: Onboarding Exercises

Create exercises that guide new developers through the codebase. Per [codebase-templates.md](codebase-templates.md).

- **Code Reading**: "Trace what happens when X occurs" — answer in fold callout
- **Configuration**: "How would you change Y?" — answer with file paths + snippets
- **Debugging**: "Where would you look if Z breaks?" — answer with investigation steps
- **Extension**: "How would you add feature W?" — answer with architectural approach
- Minimum 5 exercises per major module
- All answers use `> [!answer]- <label>` fold callout (localize label to team language, e.g., "정답 보기" for Korean, "View Answer" for English)

## Phase C8: Interlinking

1. `## Related Notes` on every module note
2. MOC links to every module note + exercise file
3. Cross-link modules that depend on each other
4. Architecture notes reference specific module implementations
5. Exercises reference the modules they cover
6. Quick Reference links to relevant module notes

## Phase C9: Self-Review (MANDATORY)

Verify against [quality-checklist.md](quality-checklist.md) **Codebase Mode** section. Fix and re-verify until all checks pass.
