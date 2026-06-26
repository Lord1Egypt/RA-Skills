# Session Handoff Document Template

> This template defines the structure for a project handoff document.
> When generating a handoff, fill in each section with project-specific content.
> **Never include personal information** — use placeholders for names, paths, and credentials.

---

## 1. Project Identity

| Field | Value |
|-------|-------|
| Project name | `<project-name>` |
| One-line description | `<description>` |
| GitHub | `https://github.com/<owner>/<repo>` |
| ClawHub slug | `<slug>` (if applicable) |
| Current version | `<X.Y.Z>` |
| Project directory | `<absolute-path-to-project>` |
| Tech stack | `<language> / <framework> / <tools>` |
| License | `<license-type>` |

---

## 2. Decision Chain (Why This Approach)

| Decision | Chosen | Rejected alternatives | Reason |
|----------|--------|----------------------|--------|
| `<decision-1>` | `<chosen>` | `<rejected>` | `<why>` |
| `<decision-2>` | `<chosen>` | `<rejected>` | `<why>` |

---

## 3. Data Flow & Execution Pipeline

```
┌──────────┐    ┌──────────┐    ┌──────────┐
│ Step 1    │ →  │ Step 2    │ →  │ Step 3    │
│ <name>    │    │ <name>    │    │ <name>    │
│ <input>   │    │ <process> │    │ <output>  │
└──────────┘    └──────────┘    └──────────┘
```

**Data format flow**:
- `<step-1>` → `<output-file-format>`
- `<step-2>` → `<output-file-format>`
- `<step-3>` → `<output-format>`

**Trigger modes**:
- Interactive: `<how>`
- Cron/Scheduled: `<how>`

---

## 4. Capability Boundary

### Can Do
- `<capability-1>`
- `<capability-2>`

### Cannot Do (Current Limitations)
- `<limitation-1>`
- `<limitation-2>`

### Dependency Constraints
| Dependency | Constraint | Impact |
|------------|-----------|--------|
| `<dep-1>` | `<constraint>` | `<impact>` |
| `<dep-2>` | `<constraint>` | `<impact>` |

---

## 5. Project File Structure

```
<project-name>/
├── <file-1>                  # <description>
├── <file-2>                  # <description>
├── <dir-1>/
│   └── <file>                # <description>
└── <dir-2>/
    └── <file>                # <description>
```

---

## 6. Platform Status

### GitHub Repository
- Repo: `<owner>/<repo>`
- Release: `<version>` (<status>)
- File count: `<N>`

### ClawHub (if applicable)
| Version | Security | Notes |
|---------|----------|-------|
| `<latest>` | CLEAN/SUSPICIOUS | `<notes>` |

---

## 7. Environment Variables

| Variable | Purpose | Status |
|----------|---------|--------|
| `<VAR_1>` | `<purpose>` | Configured / Needs user config |
| `<VAR_2>` | `<purpose>` | Configured / Needs user config |

---

## 8. Session Code Changes Summary

| File | Change | Reason |
|------|--------|--------|
| `<file-1>` | `<what changed>` | `<why>` |
| `<file-2>` | `<what changed>` | `<why>` |

---

## 9. Knowledge File Index (Load on Demand)

| Need | File to Read | Priority |
|------|-------------|----------|
| `<scenario-1>` | `<path>` | Must-read |
| `<scenario-2>` | `<path>` | On-demand |

---

## 10. User Preferences

| Preference | Description |
|-----------|-------------|
| Language | `<language>` |
| Work style | `<style>` |
| Code style | `<style>` |
| Security sensitivity | `<level>` |

---

## 11. Branchable Directions

| # | Direction | Type | Files Involved | Prerequisites | Complexity |
|---|-----------|------|---------------|---------------|------------|
| A | `<direction-1>` | Research / Engineering / Ops | `<files>` | `<prereqs>` | Low/Med/High |
| B | `<direction-2>` | Research / Engineering / Ops | `<files>` | `<prereqs>` | Low/Med/High |

---

## 12. Startup Prompt for New Session

(Generated from `references/startup-prompts.md` based on target IDE)

---

## 13. IDE-Specific Context (Optional — fill based on target IDE)

### For WorkBuddy

#### Identity Files
| File | Path | Description |
|------|------|-------------|
| SOUL.md | `~/.workbuddy/SOUL.md` | Persona definition |
| IDENTITY.md | `~/.workbuddy/IDENTITY.md` | Identity configuration |
| USER.md | `~/.workbuddy/USER.md` | User profile |

#### Memory System
| File | Path | Description |
|------|------|-------------|
| Project memory | `.workbuddy/memory/MEMORY.md` | Project-level memory |
| Daily logs | `.workbuddy/memory/YYYY-MM-DD.md` | Daily session logs |
| Global memory | `~/.workbuddy/MEMORY.md` | User global memory |

#### Installed Skills
| Skill | Version | Status |
|-------|---------|--------|
| `<skill-1>` | `<version>` | Active |
| `<skill-2>` | `<version>` | Active |

#### Scheduled Tasks (Automations)
| Task | Cron | Status | Description |
|------|------|--------|-------------|
| `<task-1>` | `<cron>` | Active/Paused | `<description>` |

#### Channel Configuration
| Channel | Config | Status |
|---------|--------|--------|
| IMA knowledge base | `<kb-id>` | Configured / Needs setup |
| Feishu channel | `<channel-config>` | Configured / Needs setup |

#### MCP Connectors
| Connector | Status |
|-----------|--------|
| `<connector-1>` | Connected / Disconnected |

### For TRAE SOLO

#### Rules
| File | Path | Description |
|------|------|-------------|
| Project rules | `.trae/rules/` | Auto-loaded project rules |

#### Scheduled Tasks
| Task | Cron | Status |
|------|------|--------|
| `<task-1>` | `<cron>` | Active/Paused |

### For Cursor

#### Rules
| File | Path | Description |
|------|------|-------------|
| Project rules | `.cursor/rules/` or `.cursorrules` | Auto-loaded project rules |

### For Claude Code

#### Rules
| File | Path | Description |
|------|------|-------------|
| Project rules | `CLAUDE.md` | Project-level instructions |
