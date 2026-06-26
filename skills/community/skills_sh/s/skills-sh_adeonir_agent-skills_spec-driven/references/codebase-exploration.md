# Codebase Exploration Patterns

Patterns for analyzing existing code for a specific feature.

## When to Use

- During design (design.md)
- Need to understand patterns for a specific feature
- Finding similar existing features
- Understanding integration points

## Scope

**Feature-specific analysis** - Focused on what you need for this feature:
- Similar existing features
- Reusable components
- Integration patterns
- Testing approaches

Durable, area-level findings from this exploration are cached at
`.artifacts/codebase/{area}.md` for reuse by future features in the same
area (see Integration with Design).

## Tools

Use available semantic analysis, code search, and file reading tools to explore the codebase.
The agent discovers and uses whatever tools are available in the environment.

## Workflow

### Phase 1: Discovery

1. **Find Documentation**

   Look for README.md, CLAUDE.md, CONTRIBUTING.md, package.json, tsconfig.json in the project.

2. **Find Source Files**

   Find files related to the feature being built, plus test files.

3. **Read Documentation**

   Read 2-3 documentation files to understand project structure, architecture patterns, and coding conventions.

### Phase 2: Pattern Extraction

4. **Identify Reference Files**

   Find 2-3 existing features similar to what needs to be built. Check imports, exports, and file organization.

5. **Read Reference Files**

   Read 3-5 essential files and extract:
   - Naming conventions (functions, classes, variables)
   - Import/export patterns
   - Error handling approach
   - Type definitions style
   - Testing patterns

6. **Extract Code Patterns**

   Document specific patterns with file:line references:
   ```text
   Pattern: Function naming
   - Project uses: camelCase for functions
   - Example: src/utils/helpers.ts:15

   Pattern: Error handling
   - Project uses: Custom error classes
   - Example: src/errors/index.ts:23
   ```

7. **Map Dependencies**

   For key files, identify imports (dependencies) and what imports from them (dependents).

### Phase 3: Architecture Analysis

8. **Trace Entry Points**

   Where would the feature integrate: API routes, UI components, CLI commands, event handlers.

9. **Follow Data Flow**

   Trace: Input validation -> Business logic -> Data transformation -> Output/response.

10. **Identify Layers**

    Map architecture layers: Presentation, Business logic, Data access, External services.

### Phase 4: Member Enumeration

Before closing Architecture Analysis, list every entity, projection, contract, DTO, view model, or type the feature will read from or write to. For each one, enumerate every exposed member with a `file:line` anchor. Sampling is not allowed -- a type either has all its members listed or it is not yet explored.

11. **Identify Touched Types**

    From the feature requirements and the data flow traced in Phase 3, list every entity, projection, DTO, contract, view model, response shape, and persisted type the feature will consume or emit.

12. **Enumerate Members Exhaustively**

    For each touched type, open its definition and list every exposed member (field, property, method, or contract element) with `file:line`. If a member is itself a composite type the feature also touches, recurse.

13. **Anchor Absence Claims**

    For every claim of the form "already returns X", "no additional join needed", "signature unchanged", "contract already covers this", attach the `file:line` of the member that backs the claim. Unanchored absence claims are rejected.

**Subsystem Presence.** For every subsystem, capability, or integration the
feature assumes available (i18n, auth, a runtime, a deployed service, a
dependency), record a present/absent verdict anchored to the `file:line` of the
wiring that proves it — config, route registration, provider setup, lockfile
entry. "Documented" or "planned" does not satisfy the claim; only wired
evidence does.

**Exit criterion:** No claim about an existing type's contents stands without (a) a full member list with `file:line` and (b) anchors on every absence assertion; and every assumed subsystem has a present/absent verdict anchored to wiring.

### Phase 5: Consolidation

14. **Summarize Conventions**

    Create comprehensive convention table with file:line references.

15. **List Essential Files**

    Categorize as: Reference (patterns to follow), Modify (existing files to change), Dependencies (files to import).

## Output Template

ALWAYS use this exact template structure:

````markdown
---
name: {{name}}
status: active
created: {{YYYY-MM-DD}}
updated: {{YYYY-MM-DD}}
sources: []
---

## Documentation Findings

| File | Purpose |
|------|---------|
| `{{path/to/README.md}}` | {{Brief description}} |

## Entry Points

| File | Line | Purpose |
|------|------|---------|
| `{{src/api/routes.ts}}` | {{45}} | {{API endpoint definitions}} |

## Code Flow

1. **Entry**: `{{file.ts:line}}` — {{Description}}
2. **Transform**: `{{file.ts:line}}` — {{Description}}
3. **Output**: `{{file.ts:line}}` — {{Description}}

## Architecture

- **Pattern**: {{MVC/Clean/Hexagonal/etc}}
- **Layers**: {{list}}
- **Key Abstractions**: {{wrappers used}}

## Touched Types — Member Enumeration

Every entity, projection, contract, or type the feature reads or writes.
All exposed members listed — no sampling. Every "no change needed"
claim anchored to `file:line`. Every `file:line` is script-verified at the
design gate (Step 6a), so it must resolve against the repo — a formatted-but-wrong
cite fails the gate.

| Type / Entity | Member | file:line | Notes (feature reads? writes? nullable?) |
|---------------|--------|-----------|------------------------------------------|
| {{EntityOrContract}} | {{memberName}} | {{path:line}} | {{notes}} |

### Absence Claims

Claims that an existing type already covers the feature's needs — each
must cite the member that backs the claim.

| Claim | Anchor (file:line) |
|-------|--------------------|
| {{e.g. "response shape already exposes field X"}} | {{path:line}} |

### Subsystem Presence

Every subsystem, capability, or integration the feature assumes available —
each with a present/absent verdict anchored to the wiring that proves it.
"Documented" / "planned" is not "wired".

| Subsystem / Capability | Present? | Wiring anchor (file:line) |
|------------------------|----------|---------------------------|
| {{e.g. i18n routing}} | {{wired / absent}} | {{path:line of config/route/provider, or "none found"}} |

## Conventions

| Aspect | Project Uses | Avoid | Reference |
|--------|-------------|-------|-----------|
| {{Env vars}} | {{t3-env}} | {{process.env}} | {{src/env.ts:10}} |
| {{Function naming}} | {{camelCase}} | {{snake_case}} | {{src/utils.ts:23}} |
| {{Error handling}} | {{Custom Error classes}} | {{Raw throws}} | {{src/errors.ts:15}} |
| {{API calls}} | {{Wrapper with retry}} | {{Direct fetch}} | {{src/lib/api.ts:45}} |
| {{Types}} | {{Interface + type}} | {{Any}} | {{src/types/index.ts:8}} |

## Test Infrastructure

- **Framework**: {{test runner}}
- **Location**: {{test directory pattern}}
- **Command**: {{test command}}
- **Patterns**: {{test structure, mocking approach}}

## Essential Files

### Reference Files (patterns to follow)

1. `{{src/core/feature.ts}}` — {{Core implementation pattern}}
2. `{{src/types/feature.ts}}` — {{Type definition pattern}}

### Files to Modify

1. `{{src/api/routes.ts}}` — {{Add new endpoint}}
2. `{{src/services/index.ts}}` — {{Register new service}}

### Dependencies

1. `{{src/lib/db.ts}}` — {{Database connection}}
2. `{{src/utils/validation.ts}}` — {{Input validation}}
````

## Integration with Design

Use findings in design.md:

- Reference files to follow
- Patterns to use
- Code to reuse

### Caching for reuse

An **area** is the cohesive part of the codebase a feature touches — a
module, domain, or feature directory (`auth`, `billing`, `dashboard`),
not a single file and not the whole repo. Derive `{area}` as the
kebab-case name of that directory or domain, reusing the existing name
so the same area always maps to the same file — stable keys are what
make the cache reusable. A feature spanning two areas reads and writes
both.

Before exploring, check `.artifacts/codebase/{area}.md` for this
feature's area. On a cache hit, reuse those findings instead of
re-deriving from scratch. After exploring, write the durable,
area-level findings (patterns, integration points, reference files)
back to `.artifacts/codebase/{area}.md` so the next feature in the same
area reuses them without rediscovery.

The cache is regenerable — treat a stale or missing entry as a cache
miss and re-explore. Durable *why* (decisions, gotchas) and normative
conventions are recorded separately in `.artifacts/knowledge.md`, not
in the area cache.

## Guidelines

**DO:**
- Read file content to extract actual patterns -- not just list files
- Include file:line references for every pattern
- Cover naming, imports, error handling, types, testing
- Follow the exploration template structure
- Focus on patterns most relevant to the feature being built
- Enumerate every exposed member of every type the feature touches -- cite file:line for each
- Anchor every "no change" or "already exposes" claim to a file:line in the member list

**DON'T:**
- List files without reading their content
- Omit file:line references for discovered patterns
- Skip areas like error handling or testing conventions
- Sample members of a touched type -- enumerate them exhaustively
- Claim a type "already returns" or "already covers" something without citing file:line
