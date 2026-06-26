# Agent Skill Platforms -- Reference for Weekend Scout

Research conducted 2026-03-28. Covers the three target platforms and their
SKILL.md conventions.

---

## 1. Claude Code

### Skill discovery paths
- Project-scoped: `.claude/skills/<name>/SKILL.md`
- User-scoped (global): `~/.claude/skills/<name>/SKILL.md`
- Plugin-provided skills
- Built-in (bundled) skills

### SKILL.md frontmatter fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Lowercase letters/numbers/hyphens, max 64 chars. Becomes the `/slash-command`. |
| `description` | Yes | Max 1024 chars. Primary trigger for auto-invocation. Write in 3rd person. |
| `model` | No | Override the model for this skill (e.g. `haiku`, `sonnet`). |
| `allowed-tools` | No | Comma-separated tool restrictions (e.g. `Bash, Read, Write, WebSearch, WebFetch`). Only in Claude Code CLI, not SDK. |
| `disable-model-invocation` | No | `true` = only user can invoke via `/name`. Prevents auto-triggering. |
| `user-invocable` | No | `false` = only Claude can invoke (background knowledge). |
| `argument-hint` | No | Hint shown in slash-command menu (e.g. `[city] [radius-km]`). |
| `mode` | No | `true` = appears in "Mode Commands" section (for debug-mode, etc.). |
| `version` | No | Version string for tracking iterations. |
| `license` | No | License identifier or filename. |
| `compatibility` | No | Required tools/dependencies (rarely needed). |
| `skills` | No | List of other skill names to preload (for subagents). |

### Invocation
- User types `/skill-name` or `/skill-name arguments`
- Claude auto-invokes when description matches user's task (unless `disable-model-invocation: true`)

### Notes
- Unknown frontmatter fields are silently ignored
- `model: haiku` is a valid field that overrides the session model for this skill
- Skills follow the Agent Skills open standard (agentskills.io)
- Progressive disclosure: metadata loaded at startup, full body loaded on invocation

---

## 2. OpenAI Codex

### Skill discovery paths
- Project-scoped: `.agents/skills/<name>/SKILL.md` (scanned from CWD up to repo root)
- User-scoped: `~/.agents/skills/<name>/SKILL.md`
- Admin: `/etc/codex/skills/`
- System: bundled skills

### SKILL.md frontmatter fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Skill identifier. |
| `description` | Yes | Primary trigger for implicit invocation. |
| `license` | No | License identifier. |
| `metadata` | No | Arbitrary metadata block (author, version, etc.). |

Codex SKILL.md frontmatter is minimal. Extra platform-specific configuration
goes into a sidecar file `agents/openai.yaml` inside the skill directory.

### `agents/openai.yaml` structure

```yaml
interface:
  display_name: "Weekend Scout"
  short_description: "Scout weekend outdoor events"
  brand_color: "#4CAF50"
  default_prompt: "Find outdoor events near my city for next weekend"

policy:
  allow_implicit_invocation: false    # default: true

dependencies:
  tools:
    - type: "mcp"
      value: "serverName"
      description: "Description"
      transport: "streamable_http"
      url: "https://..."
```

### Invocation
- Explicit: type `$skill-name` or use `/skills` menu
- Implicit: Codex auto-selects when prompt matches description (unless `allow_implicit_invocation: false`)

### Model selection
- No per-skill model override in SKILL.md frontmatter
- Model is set at session level via `~/.codex/config.toml` or `--model` flag
- Advisory model preference can be placed in `metadata` block or in the skill body text
- Default model: `gpt-5.2-codex` (as of March 2026), `gpt-5.4-mini` for lighter tasks

### Notes
- Unknown frontmatter fields are ignored (safe to keep Claude-specific fields)
- Codex detects skill file changes automatically (no restart for edits, but restart after new installs)
- Skills support `scripts/`, `references/`, `assets/` subdirectories (same as Agent Skills spec)

---

## 3. OpenClaw

### Skill discovery paths (precedence high to low)
- Workspace: `<workspace>/skills/<name>/SKILL.md` (highest)
- Project agent: `<workspace>/.agents/skills/<name>/SKILL.md`
- Personal agent: `~/.agents/skills/<name>/SKILL.md`
- Managed/local: `~/.openclaw/skills/<name>/SKILL.md`
- Bundled skills
- Extra dirs: `skills.load.extraDirs` in config (lowest)

### SKILL.md frontmatter fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Skill identifier. |
| `description` | Yes | Trigger text. |
| `metadata` | No | Single-line JSON object with OpenClaw-specific config. |

### OpenClaw metadata block

```yaml
metadata: {"openclaw":{"requires":{"bins":["python"]}}}
```

### Invocation
- ClawHub: `clawhub install <skill-name>` places into `./skills/`
- Workspace skills auto-discovered on session start
- `/status` and other slash commands in messaging channels

### Model selection
- Model set per-agent in workspace config, not per-skill
- `preferred_model` in metadata is advisory (agent may or may not honor it)
- OpenClaw supports: Anthropic, OpenAI, Google, OpenRouter, local models

### Notes
- Follows AgentSkills spec for layout/intent
- Parser supports single-line frontmatter keys only
- `metadata` should be a single-line JSON object
- `{baseDir}` placeholder available in instructions to reference skill folder path
- Unknown frontmatter fields are ignored
- Plugins can ship skills via `openclaw.plugin.json`
- In this repo, `.openclaw/skills/` is a generated packaging/staging artifact, not the canonical workspace discovery path

---

## 4. Cross-Platform Compatibility Summary

### What is shared (Agent Skills spec, agentskills.io)
- `SKILL.md` with YAML frontmatter (`name`, `description` required)
- `scripts/`, `references/`, `assets/` subdirectories
- Progressive disclosure (metadata at startup, body on invocation)
- Unknown frontmatter fields are silently ignored on all platforms

### What differs per platform

| Feature | Claude Code | Codex | OpenClaw |
|---------|------------|-------|----------|
| Project skill dir | `.claude/skills/` | `.agents/skills/` | `<workspace>/skills/` |
| Global skill dir | `~/.claude/skills/` | `~/.agents/skills/` | `~/.openclaw/skills/` |
| Disable auto-invoke | `disable-model-invocation: true` | `agents/openai.yaml` policy | Config-level |
| Per-skill model | `model: haiku` (enforced) | Not supported (advisory only) | Not supported (advisory only) |
| Explicit invoke | `/skill-name` | `$skill-name` | Depends on channel |
| Extra metadata file | None (all in frontmatter) | `agents/openai.yaml` | `metadata.openclaw` in frontmatter |
| Tool restrictions | `allowed-tools` in frontmatter | Not in SKILL.md | Not in SKILL.md |

### Safety of cross-platform frontmatter
All three platforms ignore unknown frontmatter fields. This means a SKILL.md with
Claude-specific fields like `model: haiku` or `allowed-tools: Bash, WebSearch`
will work fine on Codex and OpenClaw (the fields are simply ignored). However,
platform-specific features like `disable-model-invocation` will not take effect
on other platforms, so the equivalent mechanism must be configured separately
(e.g., `agents/openai.yaml` for Codex).
