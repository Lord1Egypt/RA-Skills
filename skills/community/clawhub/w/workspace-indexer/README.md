# Workspace Indexer

Automatically maintain a comprehensive index of your OpenClaw workspace directories.

## Features

- 🔍 **Memory-First Approach** - Searches memory files before scanning directories
- 🌳 **Intelligent Recursion** - Recognizes project containers vs. project roots
- 📝 **Detailed Descriptions** - Includes purpose, running status, memory references, and search keywords
- 🤖 **AI-Driven** - Pure prompt-based skill, no code required
- ⏰ **Daily Updates** - Designed for automated daily maintenance

## Usage

Trigger manually:
```
"更新 workspace 索引"
"update workspace index"
```

Or set up daily automation in `HEARTBEAT.md`:
```markdown
## Workspace 索引维护
每天检查 workspace 目录变化，如有新增或变更则更新索引
```

## Output

Generates `WORKSPACE_INDEX.md` in your workspace root with detailed directory descriptions.

## Requirements

- OpenClaw with `memory_search` tool enabled
- Workspace context files (MEMORY.md, memory/*.md)

## License

MIT
