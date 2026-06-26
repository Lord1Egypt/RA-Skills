# UE DataTable Editor

Edit Unreal Engine DataTable configuration through JSON files — auto-discover projects, search, modify, validate, and import back to the engine.

## Features

- **Auto-Discover** — Automatically finds UE projects and DataTable JSON files on your machine
- **Search** — Find rows by ID, name, keyword, or any field value
- **Modify** — Edit any field with automatic `NSLOCTEXT()` wrapping for localization fields
- **Validate** — Type checking, required field verification, ID uniqueness check
- **Import** — Generate UE Editor Python commands to import JSON back into DataTable assets

## Use Cases

- Batch editing DataTable entries (descriptions, names, parameters)
- Searching and reviewing configurations across multiple DataTable partitions
- Safely modifying `.uasset` DataTable files through their JSON representation
- Importing validated changes back into Unreal Engine

## Workflow

1. **Discover** → Auto-find UE projects and DataTable JSON files
2. **Search** → Locate target row(s) in the JSON data
3. **Modify** → Edit fields with validation and automatic backup
4. **Import** → Run the generated command in UE Editor to update the DataTable

## Quick Start

Just tell the AI what you want to do:

- "查找技能 230005"
- "修改 AI_Skills 表中技能 230000 的描述"
- "帮我看看技能表里有哪些蓄力技能"
- "修改 DT 表中 DevName 包含瞬移的技能"

The skill will automatically discover your UE project, locate the right JSON file, and guide you through the edit.

## Trigger Phrases

- "修改技能" / "查找技能" / "技能表"
- "DataTable" / "DT表" / "AI Skills"
- "导入UE" / "技能数据"

## Scripts

| Script | Purpose |
|--------|---------|
| `dt_discover.py` | Auto-discover UE projects and DataTable JSON files |
| `dt_search.py` | Search/query rows in DataTable JSON |
| `dt_modify.py` | Modify fields with validation and backup |
| `dt_import_ue.py` | UE Editor script to import JSON back into DataTable |

## Requirements

- Python 3.7+
- UE Editor (for import step only)

## License

MIT-0
