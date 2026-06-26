# Codebase Mode — Templates Reference

## Vault Folder Structure

```
StudyVault/
  00-Dashboard/          # MOC + Quick Reference + Getting Started
  01-Architecture/       # System overview, request flow, data flow
  02-<Module1>/          # Per-module notes
  03-<Module2>/
  ...
  NN-DevOps/             # Build, deploy, CI/CD, env config
  NN+1-Exercises/        # Onboarding exercises
```

## Dashboard MOC Template

```markdown
---
module: dashboard
path: 00-Dashboard
keywords: MOC, onboarding, architecture, <project-name>
---

# <Project Name> — Onboarding Map

#dashboard #onboarding

## Architecture Overview
- Pattern: <architectural pattern>
- Tech stack: <languages, frameworks, key libraries>
- → [[System Architecture]]
- → [[Request Flow]]

## Module Map
| Module | Purpose | Key Entry Point | Notes |
|--------|---------|-----------------|-------|
| <name> | <1-line purpose> | `<path>` | [[Module Note]] |

## API Surface
| Method | Path / Command | Module | Notes |
|--------|---------------|--------|-------|
| GET | `/endpoint` | <module> | [[API Note]] |

## Getting Started
1. Prerequisites: ...
2. Install: `<install command>`
3. Configure: copy `.env.example` → `.env`
4. Run: `<run command>`
5. Test: `<test command>`

## Tag Index
| Tag | Description | Rule |
|-----|-------------|------|
| `#arch-*` | Architecture concepts | Top-level pattern tags |
| `#module-*` | Module-specific | One per module |

## Onboarding Path
> Recommended reading order for new developers:

1. [[System Architecture]] — big picture
2. [[Request Flow]] — how a request moves through the system
3. [[Module A]] → [[Module B]] → ... — module deep dives
4. [[Exercises]] — hands-on practice
```

## Quick Reference Template

```markdown
---
module: dashboard
path: 00-Dashboard
keywords: quick-reference, commands, setup
---

# Quick Reference

#dashboard #quick-reference

## Key Commands
| Action | Command |
|--------|---------|
| Install deps | `<command>` |
| Run dev | `<command>` |
| Run tests | `<command>` |
| Build | `<command>` |
| Lint | `<command>` |

## Environment Setup
1. ...

## Important File Locations
| File / Dir | Purpose |
|------------|---------|
| `<path>` | <description> |

## Common Debugging
| Symptom | Where to Look | → Note |
|---------|---------------|--------|
| <problem> | `<file/log>` | [[Module Note]] |
```

## Module Note Template

```markdown
---
module: <module-name>
path: <relative-path-from-project-root>
keywords: <3-5 English keywords>
---

# <Module Name> (<Importance: ★~★★★>)

#module-<name> #<pattern-tag>

## Purpose
<1-3 sentences: what this module does and why it exists>

## Key Files
| File | Role |
|------|------|
| `<relative-path>` | <description> |

## Public Interface
| Export | Type | Description |
|--------|------|-------------|
| `<name>` | function/class/endpoint | <what it does> |

## Internal Flow

```text
<ASCII diagram showing data/control flow within this module>
```

## Dependencies
| Direction | Module / Service | Via |
|-----------|-----------------|-----|
| **Uses** | <dependency> | `<import/call>` |
| **Used by** | <dependent> | `<import/call>` |

## Configuration
| Env Var / Config Key | Purpose | Default |
|---------------------|---------|---------|
| `<VAR>` | <description> | `<default>` |

## Testing
- Run: `<test command for this module>`
- Pattern: <unit/integration/e2e>
- Coverage notes: ...

## Related Notes
- [[Other Module]]
- [[Architecture Note]]
```

## API Note Template

```markdown
---
module: <module-name>
path: <relative-path>
keywords: API, <endpoint-keywords>
---

# <Endpoint Group> API

#api-<group> #module-<name>

## Endpoints
| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/path` | required | <description> |

## Request / Response

### <Endpoint Name>

**Request**:
```json
{
  "field": "type — description"
}
```

**Response (success)**:
```json
{
  "field": "type — description"
}
```

**Error cases**:
| Status | Condition | Response |
|--------|-----------|----------|
| 400 | <condition> | `{ "error": "..." }` |

## Related Notes
- [[Module Note]]
- [[Other API Note]]
```

## Onboarding Exercise Template

```markdown
---
module: exercises
path: <NN+1>-Exercises
keywords: practice, onboarding, <topic>
---

# <Topic> — Onboarding Exercises

#practice #onboarding #module-<name>

## Related Modules
- [[Module Note 1]]
- [[Module Note 2]]

---

## Exercise 1 — Code Reading [trace]
> Trace what happens when <specific trigger>. List the files and functions involved in order.

> [!answer]- View Answer
> 1. `<file>` → `<function>` — <what happens>
> 2. `<file>` → `<function>` — <what happens>
> 3. ...

---

## Exercise 2 — Configuration [config]
> How would you change <specific setting>? Which files need modification?

> [!answer]- View Answer
> - File: `<path>`
> - Change: <description>
> - Related env var: `<VAR>`

---

## Exercise 3 — Debugging [debug]
> If <symptom> occurs, where would you look first? Describe your investigation steps.

> [!answer]- View Answer
> 1. Check `<file/log>` for ...
> 2. Verify `<config>` is ...
> 3. Common cause: ...

---

## Exercise 4 — Extension [extend]
> How would you add <new feature/endpoint>? Describe the files you'd create or modify.

> [!answer]- View Answer
> 1. Create `<path>` — <purpose>
> 2. Modify `<path>` — <what to add>
> 3. Add test in `<path>` — <what to test>
> 4. Register in `<path>` — <wiring>

---

> [!summary]- 학습 포인트 요약
> | Topic | Key Takeaway |
> |-------|-------------|
> | <topic> | <insight> |
```

## Formatting Rules

- `[[wiki-links]]` for all cross-references
- `> [!tip]`, `> [!important]`, `> [!warning]` callouts for key information
- ASCII diagrams for flows, architecture, and module interactions
- Tables over prose for structured information
- **Bold** for critical terms and file paths in descriptions
- Code blocks with language hints for commands and snippets
- **Localization**: Fold callout labels (e.g., `View Answer`) should match team language. Korean: `정답 보기`, English: `View Answer`
