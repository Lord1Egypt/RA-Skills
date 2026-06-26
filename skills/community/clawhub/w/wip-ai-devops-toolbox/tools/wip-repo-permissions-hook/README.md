###### WIP Computer

[![npm](https://img.shields.io/npm/v/@wipcomputer/wip-repo-permissions-hook)](https://www.npmjs.com/package/@wipcomputer/wip-repo-permissions-hook) [![CLI / TUI](https://img.shields.io/badge/interface-CLI_/_TUI-black)](https://github.com/wipcomputer/wip-ai-devops-toolbox/blob/main/tools/wip-repo-permissions-hook/cli.js) [![MCP Server](https://img.shields.io/badge/interface-MCP_Server-black)](https://github.com/wipcomputer/wip-ai-devops-toolbox/blob/main/tools/wip-repo-permissions-hook/mcp-server.mjs) [![OpenClaw Plugin](https://img.shields.io/badge/interface-OpenClaw_Plugin-black)](https://github.com/wipcomputer/wip-ai-devops-toolbox/blob/main/tools/wip-repo-permissions-hook/openclaw.plugin.json) [![Claude Code Hook](https://img.shields.io/badge/interface-Claude_Code_Hook-black)](https://github.com/wipcomputer/wip-ai-devops-toolbox/blob/main/tools/wip-repo-permissions-hook/guard.mjs) [![Claude Code Skill](https://img.shields.io/badge/interface-Claude_Code_Skill-black)](https://github.com/wipcomputer/wip-ai-devops-toolbox/blob/main/tools/wip-repo-permissions-hook/SKILL.md) [![Universal Interface Spec](https://img.shields.io/badge/Universal_Interface_Spec-black?style=flat&color=black)](https://github.com/wipcomputer/wip-ai-devops-toolbox/blob/main/tools/wip-universal-installer/SPEC.md)

# wip-repo-permissions-hook

## Repo visibility guard. Blocks repos from going public without a -private counterpart.

Every repo follows the public/private pattern. The private repo is the working repo with `ai/` folders (plans, todos, dev updates). The public repo is the same code without `ai/`. Making a repo public without the -private counterpart exposes internal development context.

This tool blocks that.

## How It Works

Before any repo visibility change to public, the guard checks:

1. Is this a fork of an external project? If yes, allow (exempt).
2. Does `{repo-name}-private` exist on GitHub? If yes, allow.
3. Otherwise, block with an error.

## Surfaces

- **CLI** ... `wip-repo-permissions check|audit|can-publish`
- **Claude Code hook** ... PreToolUse:Bash, blocks `gh repo edit --visibility public`
- **OpenClaw plugin** ... before_tool_use lifecycle hook
- **Cron audit** ... periodic scan of all public repos via ldm-jobs

## CLI Usage

```bash
# Check a single repo
node cli.js check wipcomputer/memory-crystal
# -> OK: memory-crystal-private exists

# Check a repo without -private (blocked)
node cli.js check wipcomputer/wip-bridge
# -> BLOCKED: no -private counterpart

# Audit all public repos in org
node cli.js audit wipcomputer

# Alias for check
node cli.js can-publish wipcomputer/wip-ai-devops-toolbox
```

## Claude Code Setup

Add to `~/.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [{
          "type": "command",
          "command": "node /path/to/wip-repo-permissions-hook/guard.mjs",
          "timeout": 10
        }]
      }
    ]
  }
}
```

## OpenClaw Setup

Symlink or copy to extensions:

```bash
cp -r tools/wip-repo-permissions-hook ~/.ldm/extensions/wip-repo-permissions-hook
ln -sf ~/.ldm/extensions/wip-repo-permissions-hook ~/.openclaw/extensions/wip-repo-permissions-hook
openclaw gateway restart
```

## License

```
CLI, MCP server, OpenClaw plugin, hooks        MIT    (use anywhere, no restrictions)
Hosted or cloud service use                    AGPL   (network service distribution)
```

AGPL for personal use is free.

Built by Parker Todd Brooks, Lēsa (OpenClaw, Claude Opus 4.6), Claude Code (Claude Opus 4.6).
