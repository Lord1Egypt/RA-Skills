# NestJS Best Practices

A structured repository for creating and maintaining NestJS Best Practices optimized for agents and LLMs.

## Structure

- `rules/` - Individual rule files (one per rule)
  - `_sections.md` - Section metadata (titles, impacts, descriptions)
  - `_template.md` - Template for creating new rules
  - `section-description.md` - Individual rule files
- `src/` - Build scripts and utilities (in packages/nestjs-best-practices-build)
- `AGENTS.md` - Compiled output (generated)
- `CLAUDE.md` - Additional context for Claude agents

## Getting Started

1. Install dependencies:
   ```bash
   cd packages/nestjs-best-practices-build
   bun install
   ```

2. Build AGENTS.md from rules:
   ```bash
   bun run build
   ```

3. Validate rule files:
   ```bash
   bun run validate
   ```

4. Extract test cases:
   ```bash
   bun run extract-tests
   ```

## Creating a New Rule

1. Copy `rules/_template.md` to `rules/section-description.md`
2. Choose the appropriate section prefix:
   - `security-` for Security (Section 1)
   - `performance-` for Performance (Section 2)
   - `architecture-` for Architecture (Section 3)
   - `error-handling-` for Error Handling (Section 4)
   - `validation-` for Validation (Section 5)
   - `database-` for Database (Section 6)
   - `auth-` for Authentication (Section 7)
   - `api-` for API (Section 8)
   - `config-` for Configuration (Section 9)
   - `testing-` for Testing (Section 10)
   - `deployment-` for Deployment (Section 11)
   - `middleware-` for Middleware (Section 12)
   - `advanced-` for Advanced Patterns (Section 13)
3. Fill in the frontmatter and content following the agent-friendly format
4. Include "For AI Agents" section with step-by-step instructions
5. Add Quick Reference Checklist for code review
6. Run `bun run build` to regenerate AGENTS.md

## Rule File Structure

Each rule file should follow this structure:

```markdown
---
title: Rule Title Here
impact: CRITICAL
section: 6
impactDescription: Optional description
tags: tag1, tag2, tag3
---

## Rule Title Here

Brief explanation of the rule and why it matters.

> **Hint**: Helpful tip for quick implementation

## For AI Agents

Step-by-step instructions with file locations and code patterns.

### Step 1: Check Pattern

**Pattern to check:** What to look for in code

```typescript
// ❌ WRONG - Bad pattern
// ✅ CORRECT - Good pattern
```

**If found:** What to do instead

### Step 2: Implementation

**File:** `src/path/to/file.ts`

```typescript
// ✅ REQUIRED: Implementation
```

## Installation

```bash
bun add package-name
```

## Quick Reference Checklist

- [ ] Check item 1
- [ ] Check item 2

## Incorrect (Bad Pattern)

```typescript
// Bad code with explanation
```

## Correct (Good Pattern)

```typescript
// Good code with explanation
```

**Sources:**
- [Documentation Link](https://example.com)

## File Naming Convention

- Files starting with `_` are special (excluded from build)
- Rule files: `section-description.md` (e.g., `validation-dto-validation.md`)
- Section number is specified in frontmatter `section` field
- Rules are sorted alphabetically by title within each section
- IDs (e.g., 1.1, 1.2) are auto-generated during build

## Impact Levels

- `CRITICAL` - Security vulnerabilities, data loss prevention, critical functionality
- `HIGH` - Significant performance gains, major architectural improvements
- `MEDIUM` - Moderate improvements, developer experience enhancements

## Sections Overview

| Section | Prefix | Impact | Description |
|---------|--------|--------|-------------|
| 1. Security | `security-` | CRITICAL | CORS, dependency audits, security headers |
| 2. Performance | `performance-` | HIGH | Caching, compression, lazy loading |
| 3. Architecture | `architecture-` | HIGH | Module structure, separation of concerns, naming |
| 4. Error Handling | `error-handling-` | HIGH | Exception filters, structured logging |
| 5. Validation | `validation-` | CRITICAL | DTOs, ValidationPipe, custom pipes |
| 6. Database | `database-` | CRITICAL | Parameterized queries, Prisma patterns |
| 7. Authentication | `auth-` | CRITICAL | Guards, password hashing, authorization |
| 8. API | `api-` | MEDIUM | Swagger, cursor pagination |
| 9. Configuration | `config-` | CRITICAL | Environment variables, secrets management |
| 10. Testing | `testing-` | MEDIUM | Unit tests, test coverage |
| 11. Deployment | `deployment-` | MEDIUM | Health checks, graceful shutdown |
| 12. Middleware | `middleware-` | MEDIUM | Rate limiting, compression |
| 13. Advanced | `advanced-` | HIGH | Scheduled tasks, event-driven architecture |

## Agent-Friendly Format

All rules include:
- `section` field in frontmatter for proper grouping
- "For AI Agents" section with explicit step-by-step instructions
- File locations (e.g., `src/users/users.service.ts`)
- ✅ CORRECT vs ❌ WRONG patterns
- Quick Reference Checklist for code review
- Installation commands with `bun add`
- Code examples for NestJS + Prisma

## Scripts

- `bun run build` - Compile rules into AGENTS.md
- `bun run validate` - Validate all rule files
- `bun run extract-tests` - Extract test cases for LLM evaluation
- `bun run dev` - Build and validate

## Contributing

When adding or modifying rules:

1. Use the correct filename prefix for your section
2. Follow the `_template.md` structure with agent-friendly sections
3. Include "For AI Agents" section with step-by-step instructions
4. Add clear ✅ CORRECT vs ❌ WRONG examples with explanations
5. Include Quick Reference Checklist
6. Use `bun add` for installation commands
7. Run `bun run build` to regenerate AGENTS.md

## Current Statistics

- **13 sections** covering all aspects of NestJS development
- **26 rules** across security, architecture, performance, and more
- **Agent-optimized** format with step-by-step instructions
- **Prisma v7** compatibility for database rules
- **Bun runtime** support for native crypto and scheduling

## License

MIT

## Acknowledgments
Originally created by [Xiro](https://www.facebook.com/xirothedev)