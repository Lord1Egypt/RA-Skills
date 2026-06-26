---
name: doc-forge
description: "Auto-documentation generator — analyzes code and generates README, API docs, architecture docs, inline comments. Use when documentation is missing or outdated."
metadata: { "openclaw": { "emoji": "📝", "homepage": "https://clawhub.ai/NakedoShadow", "os": ["darwin", "linux", "win32"] } }
---

# Doc Forge — Intelligent Documentation Generator

**Version**: 1.1.0 | **Author**: Shadows Company | **License**: MIT

---

## WHEN TO TRIGGER

- Project has no README or outdated documentation
- User says "document this", "generate docs", "write README"
- New module/feature needs documentation
- API endpoints need documented
- Onboarding documentation needed

## WHEN NOT TO TRIGGER

- Code is self-explanatory and well-named
- User explicitly says "no docs needed"
- Adding trivial comments to obvious code

## PREREQUISITES

No binaries required. This skill reads source files and generates documentation in markdown format. No external tools needed.

---

## DOCUMENTATION TYPES

### Type 1 — README.md

Structure:
```markdown
# Project Name
[One-line description]

## Quick Start
[3-5 steps to get running]

## Features
[Bullet list of key capabilities]

## Installation
[Step-by-step install instructions]

## Usage
[Code examples for common use cases]

## Configuration
[Environment variables, config files]

## API Reference
[If applicable — endpoints or function signatures]

## Architecture
[High-level diagram or description]

## Contributing
[How to contribute]

## License
[License type]
```

### Type 2 — API Documentation

For each endpoint/function:
```markdown
### `METHOD /path/to/endpoint`

**Description**: What it does.

**Auth**: Required/Optional/None

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| id   | string | Yes    | Resource ID |

**Request Body**:
```json
{ "key": "value" }
```

**Response** (200):
```json
{ "ok": true, "data": {} }
```

**Errors**:
| Code | Description |
|------|-------------|
| 400  | Invalid input |
| 401  | Unauthorized |
| 404  | Not found |
```

### Type 3 — Architecture Document

```markdown
# Architecture Overview

## System Diagram
[Text-based diagram using ASCII or Mermaid]

## Components
[Description of each major component]

## Data Flow
[How data moves through the system]

## Key Decisions
[Why certain architectural choices were made]

## Dependencies
[External services and their purposes]
```

### Type 4 — Inline Code Documentation

Rules for adding code comments:
1. **Only document WHY, never WHAT** — the code shows WHAT
2. **Document edge cases** — explain non-obvious behavior
3. **Document contracts** — inputs, outputs, side effects
4. **No obvious comments** — `// increment counter` on `counter++` is noise

Good:
```python
# Rate limit: Stripe API allows max 100 requests/sec.
# We batch to stay under 80 to account for retries.
batch_size = 80
```

Bad:
```python
# Set batch size to 80
batch_size = 80
```

---

## PROCESS

1. **Scan** the project structure — list all directories and key files (entry points, configs, tests)
2. **Read** entry points first (main.py, index.ts, server.py), then configs, then supporting modules
3. **Analyze** frameworks used, architecture patterns, data flow, public interfaces
4. **Generate** the appropriate documentation type based on what the project needs most
5. **Verify** every code example and function signature against the actual source before finalizing

---

## SECURITY CONSIDERATIONS

This skill reads source code files to generate documentation. It does not execute code, make network calls, or modify existing source files. Generated documentation is written as new files only. No credentials required, no persistence, no network access. Safe for all repositories.

---

## OUTPUT FORMAT

Generated documentation follows the templates defined in DOCUMENTATION TYPES above. Each output file is a standalone markdown document placed alongside the source it documents (or at the project root for README.md).

---

## RULES

1. **Read before documenting** — never document code you haven't read
2. **Accuracy over completeness** — better to document less correctly than more incorrectly
3. **Living docs** — documentation must match current code state
4. **Examples are mandatory** — every API endpoint needs a usage example
5. **No fictional features** — only document what actually exists in the codebase
6. **Match project language** — if project docs are in French, write in French

---

**Published by Shadows Company — "We work in the shadows to serve the Light."**
