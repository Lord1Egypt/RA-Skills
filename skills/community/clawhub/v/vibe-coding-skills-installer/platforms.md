# Platform Reference

Quick-reference for agent platform directory conventions and install differences.

## Skills Directory Paths

| Platform | Global Skills | Project Skills | Config Root |
|----------|--------------|----------------|-------------|
| Cursor | `~/.cursor/skills/` | `.cursor/skills/` | `~/.cursor/` |
| Claude Code | `~/.claude/skills/` | `.claude/skills/` | `~/.claude/` |
| Codex | `~/.agents/skills/` | `.agents/skills/` | `~/.agents/` |
| Windsurf | `~/.windsurf/skills/` | `.windsurf/skills/` | `~/.windsurf/` |
| Gemini CLI | `~/.gemini/skills/` | `.gemini/skills/` | `~/.gemini/` |
| OpenCode | `~/.opencode/skills/` | `.opencode/skills/` | `~/.opencode/` |
| Copilot | N/A | `.github/copilot/skills/` | N/A |
| Cline | `~/.cline/skills/` | `.cline/skills/` | `~/.cline/` |
| Amp | `~/.config/amp/skills/` | `.agents/skills/` | `~/.config/amp/` |
| Roo Code | `~/.roo-code/skills/` | `.roo-code/skills/` | `~/.roo-code/` |
| Aider | `~/.aider/skills/` | `.aider/skills/` | `~/.aider/` |

## Per-Skill-Set Install Methods by Platform

### OpenSpec

| Step | Command | Platform-dependent? |
|------|---------|---------------------|
| Install CLI | `npm install -g @fission-ai/openspec@latest` | No |
| Init project | `openspec init` | No |
| Workflow skills | Clone + copy to `$PROJECT_SKILLS/openspec-*` | Yes (target dir) |

Workflow skills source: `https://github.com/samotage/cursor-openspec-workflows`

### gstack

| Platform | `--host` value | Clone target |
|----------|---------------|--------------|
| Claude Code | `claude` | `~/.claude/skills/gstack` |
| Cursor | `cursor` | `~/.cursor/skills/gstack` |
| Codex | `codex` | `~/.agents/skills/gstack` |
| OpenCode | `opencode` | `~/.opencode/skills/gstack` |

Source: `https://github.com/garrytan/gstack`

Prerequisites: git, bun v1.0+

### Superpowers

| Platform | Install Method |
|----------|---------------|
| Cursor | `/add-plugin superpowers` |
| Claude Code | `/plugin install superpowers@claude-plugins-official` |
| Codex | `git clone https://github.com/obra/superpowers.git ~/.agents/skills/superpowers` |
| OpenCode | Agent fetches `https://raw.githubusercontent.com/obra/superpowers/refs/heads/main/.opencode/INSTALL.md` |
| Others | `git clone` to platform's global skills dir |

Source: `https://github.com/obra/superpowers`

## Environment Dependencies

| Dependency | Required by | Check command | Min version |
|------------|------------|---------------|-------------|
| node | OpenSpec | `node --version` | v20.19.0 |
| npm | OpenSpec | `npm --version` | — |
| git | gstack, Superpowers (clone) | `git --version` | — |
| bun | gstack | `bun --version` | v1.0 |
