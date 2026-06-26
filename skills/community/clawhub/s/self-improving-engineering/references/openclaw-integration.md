# OpenClaw Integration

Complete setup and usage guide for integrating the self-improving-engineering skill with OpenClaw.

## Overview

OpenClaw uses workspace-based prompt injection combined with event-driven hooks. Context is injected from workspace files at session start, and hooks can trigger on lifecycle events.

## Workspace Structure

```
~/.openclaw/                      
├── workspace/                   # Working directory
│   ├── AGENTS.md               # CI/CD workflows, deployment patterns, multi-agent coordination
│   ├── SOUL.md                 # Design principles, architecture guidelines, coding standards
│   ├── TOOLS.md                # Build tools, test frameworks, dependency managers, infra gotchas
│   ├── MEMORY.md               # Long-term memory (main session only)
│   └── memory/                 # Daily memory files
│       └── YYYY-MM-DD.md
├── skills/                      # Installed skills
│   └── <skill-name>/
│       └── SKILL.md
└── hooks/                       # Custom hooks
    └── <hook-name>/
        ├── HOOK.md
        └── handler.ts
```

## Quick Setup

### 1. Install the Skill

```bash
clawdhub install self-improving-engineering
```

Or copy manually:

```bash
cp -r self-improving-engineering ~/.openclaw/skills/
```

### 2. Install the Hook (Optional)

Copy the hook to OpenClaw's hooks directory:

```bash
cp -r hooks/openclaw ~/.openclaw/hooks/self-improving-engineering
```

Enable the hook:

```bash
openclaw hooks enable self-improving-engineering
```

### 3. Create Learning Files

Create the `.learnings/` directory in your workspace:

```bash
mkdir -p ~/.openclaw/workspace/.learnings
```

## Injected Prompt Files

### AGENTS.md

Purpose: CI/CD workflows, deployment patterns, multi-agent coordination.

```markdown
# Engineering Agent Coordination

## CI/CD Workflows
- Run full test suite before merging to main
- Use staging deploy as a gate before production
- Rollback procedure: revert last deploy, not just the commit

## Deployment Patterns
- Blue-green for stateless services
- Canary for services with persistent connections
- Database migrations run before code deploy, never after
```

### SOUL.md

Purpose: Design principles, architecture guidelines, coding standards.

```markdown
# Engineering Principles

## Architecture Guidelines
- Prefer composition over inheritance for service layer
- Repository pattern for all database access
- No business logic in controllers/handlers
- Event-driven for cross-service communication

## Code Quality Standards
- All public methods must have unit tests
- Integration tests for external service boundaries
- No direct ORM calls outside repository layer
```

### TOOLS.md

Purpose: Build tools, test frameworks, dependency managers, infra gotchas.

```markdown
# Engineering Tools

## Build & Dependencies
- pnpm for package management (not npm)
- Node 20 LTS pinned in .nvmrc
- Docker builds require --platform linux/amd64 on Apple Silicon

## Testing
- Jest for unit tests, Playwright for E2E
- Test database uses Docker container, not shared staging
- Flaky test? Check for shared state or missing cleanup

## CI/CD
- GitHub Actions runners use ubuntu-latest
- Pin action versions to SHA, not tags
- Cache pnpm store for faster installs
```

## Learning Workflow

### Capturing Engineering Learnings

1. **In-session**: Log to `.learnings/` as usual
2. **Cross-session**: Promote to workspace files

### Promotion Decision Tree

```
Is it a one-off project-specific fix?
├── Yes → Keep in .learnings/
└── No → Is it an architecture decision?
    ├── Yes → Promote to ADR (docs/decisions/) and SOUL.md
    └── No → Is it a build/tool gotcha?
        ├── Yes → Promote to TOOLS.md
        └── No → Is it a CI/CD workflow?
            ├── Yes → Promote to AGENTS.md
            └── No → Promote to SOUL.md (coding standard)
```

### Promotion Format Examples

**From learning:**
> Node 20 native modules break on GitHub Actions when setup-node uses v4 without explicit .nvmrc reference

**To TOOLS.md:**
```markdown
## Node Version (CI)
- Pin node version in CI: `node-version-file: '.nvmrc'` in setup-node
- Add engines field to package.json as a second safeguard
- setup-node v4 ignores .nvmrc unless explicitly configured
```

## Engineering-Specific Triggers

| Trigger | Action |
|---------|--------|
| Build failure in CI | Log to ENGINEERING_ISSUES.md, check TOOLS.md for known gotchas |
| Test suite regression | Log to ENGINEERING_ISSUES.md with flaky-test or coverage context |
| Architecture violation in PR | Log to LEARNINGS.md with architecture_debt category |
| Dependency CVE alert | Log to ENGINEERING_ISSUES.md, evaluate upgrade path |
| Performance degradation alert | Log to ENGINEERING_ISSUES.md with metrics |
| Deployment rollback | Log to ENGINEERING_ISSUES.md, update AGENTS.md with rollback lessons |

## Available Hook Events

| Event | When It Fires |
|-------|---------------|
| `agent:bootstrap` | Before workspace files inject |
| `command:new` | When `/new` command issued |
| `command:reset` | When `/reset` command issued |
| `command:stop` | When `/stop` command issued |
| `gateway:startup` | When gateway starts |

## Verification

Check hook is registered:

```bash
openclaw hooks list
```

Check skill is loaded:

```bash
openclaw status
```

## Troubleshooting

### Hook not firing

1. Ensure hooks enabled in config
2. Restart gateway after config changes
3. Check gateway logs for errors

### Learnings not persisting

1. Verify `.learnings/` directory exists
2. Check file permissions
3. Ensure workspace path is configured correctly

### Skill not loading

1. Check skill is in skills directory
2. Verify SKILL.md has correct frontmatter
3. Run `openclaw status` to see loaded skills
