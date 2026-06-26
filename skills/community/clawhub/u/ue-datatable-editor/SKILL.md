---
name: ue-datatable-editor
description: >
  This skill should be used when the user wants to search, view, modify, validate, 
  or import Unreal Engine DataTable data — specifically AI Skills configuration stored 
  in JSON format. Trigger phrases include "修改技能", "查找技能", "技能表", "DataTable", 
  "DT表", "AI Skills", "导入UE", "技能数据", or any reference to editing .uasset DataTable 
  files through their JSON representation. This skill handles the full workflow: 
  discover project → search → modify → validate → import back to UE Engine.
---

# UE DataTable Editor

Edit Unreal Engine DataTable configuration through JSON files — auto-discover projects, search, modify, validate, and import back to the engine.

## Overview

UE projects commonly store DataTable data in `.uasset` files, with corresponding JSON source files that serve as the editable representation. This skill provides a complete workflow for discovering, modifying, and re-importing these data tables.

**This skill works with any UE project** — it automatically detects the project structure and locates DataTable JSON files. No hardcoded paths required.

### Supported DataTable Format

The JSON file should be an array of objects, each with a `Name` field as the row key:

```json
[
  { "Name": "230000", "DevName": "技能名", "LOC_Name": "NSLOCTEXT(...)", ... },
  { "Name": "230001", ... }
]
```

### Important Notes

- JSON files may be encoded in **UTF-16 LE (with BOM)**, UTF-8 BOM, or UTF-8. All scripts handle encoding automatically.
- The `.uasset` files are binary and cannot be edited directly — always modify through JSON then import.

## Workflow

### Step 0: Discover UE Project and DataTable Files

**ALWAYS run this step first** when the user has not provided a specific JSON path. Use `scripts/dt_discover.py` to auto-detect UE projects and DataTable JSON files:

```bash
# Auto-discover all UE projects and DataTable JSON files in common locations
python {SKILL_DIR}/scripts/dt_discover.py

# Search in a specific directory
python {SKILL_DIR}/scripts/dt_discover.py --root "<directory>"

# Find a specific table by name (matches JSON filename)
python {SKILL_DIR}/scripts/dt_discover.py --table "AI_Skills"

# Filter by UE project name
python {SKILL_DIR}/scripts/dt_discover.py --project "SMG"

# Output as JSON for parsing
python {SKILL_DIR}/scripts/dt_discover.py --json-output
```

**When the user provides a table name** (e.g. "修改 AI_Skills 表"), use `--table` to locate the matching JSON file:

```bash
python {SKILL_DIR}/scripts/dt_discover.py --table "<user_provided_table_name>"
```

Once the JSON file is identified, store its absolute path for use in subsequent steps.

### Step 1: Search for Target Rows

Use `scripts/dt_search.py` to locate the row(s) to modify. The `--json` parameter takes the path discovered in Step 0.

```bash
# Search by row ID
python {SKILL_DIR}/scripts/dt_search.py --json <json_path> --id 230000

# Search by name keyword
python {SKILL_DIR}/scripts/dt_search.py --json <json_path> --name "蓄力"

# Search by any field
python {SKILL_DIR}/scripts/dt_search.py --json <json_path> --field DevName --value "瞬移"

# List all rows in a Part (for AI Skills tables)
python {SKILL_DIR}/scripts/dt_search.py --json <json_path> --part 1

# Show full JSON for results
python {SKILL_DIR}/scripts/dt_search.py --json <json_path> --id 230000 --full

# List all available fields
python {SKILL_DIR}/scripts/dt_search.py --json <json_path> --list-fields
```

Present search results to the user before proceeding with modifications.

### Step 2: Modify Data

Use `scripts/dt_modify.py` to modify fields. The script automatically:
- Wraps plain text in `NSLOCTEXT()` format for localization fields
- Validates all data after modification
- Creates a timestamped backup before saving

```bash
# Modify LOC_Desc (auto-wraps in NSLOCTEXT)
python {SKILL_DIR}/scripts/dt_modify.py --json <json_path> --id 230000 --set-loc-desc "对随机角色造成伤害"

# Modify LOC_Name
python {SKILL_DIR}/scripts/dt_modify.py --json <json_path> --id 230000 --set-loc-name "新技能名"

# Modify any field
python {SKILL_DIR}/scripts/dt_modify.py --json <json_path> --id 230000 --set "bUseAlert=true" --set "DevName=新名称"

# Preview without saving (dry-run)
python {SKILL_DIR}/scripts/dt_modify.py --json <json_path> --id 230000 --set-loc-desc "测试" --dry-run

# Validate entire JSON
python {SKILL_DIR}/scripts/dt_modify.py --json <json_path> --validate
```

#### NSLOCTEXT Format Rules

For localization fields (`LOC_Name`, `LOC_Desc`, `LOC_AlertText`, `LOC_InterruptMessage`, `LOC_NoticeText`):
- When user provides plain text, the script auto-wraps it as: `NSLOCTEXT("<PartName>", "<SkillID>_<FieldName>", "<text>")`
- When user provides a full `NSLOCTEXT(...)` or `INVTEXT(...)` string, it is used as-is
- Use `--no-wrap` flag to disable auto-wrapping

#### Field Modification via Direct File Edit

For complex modifications (nested objects, arrays, or bulk changes), directly edit the JSON file using `replace_in_file` or `read_file` + `write_to_file` tools. Always validate after editing:

```bash
python {SKILL_DIR}/scripts/dt_modify.py --json <json_path> --validate
```

### Step 3: Import into UE Engine

After modifying and validating the JSON, generate the UE import command. The user must execute this command in the **UE Editor Output Log**:

```
py "{SKILL_DIR}/scripts/dt_import_ue.py" --json "<json_path>" --part <part_number>
```

Parameters:
- `--part 0` — Import Part0 (ID 200000–229999)
- `--part 1` — Import Part1 (ID 230000–239999)
- `--part 2` — Import Part2 (ID 240000–249999)
- `--part all` — Import all Parts
- `--asset-base "<path>"` — Override the UE asset base path (default: `/Game/SMG/Configs/DataTables/AISkills`)

**Determine the correct `--part` number from the row ID being modified.** Always provide the full command with absolute paths for the user to copy-paste.

### Step 4: Verify

After the user reports the UE import result, check the log output for:
- `Imported DataTable '...' - 0 Problems` = Success
- Any `Error` lines = Investigation needed

Refer to `references/field_schema.md` for the complete field documentation when needed.

## Quick Start Example

User says: "修改 AI_Skills 表中技能 230005 的描述"

1. **Discover**: `python {SKILL_DIR}/scripts/dt_discover.py --table "AI_Skills"`
   → Found: `D:\Projects\MyGame\Content\Configs\Json\Json_AI_Skills.json`

2. **Search**: `python {SKILL_DIR}/scripts/dt_search.py --json "<found_path>" --id 230005`
   → Shows current skill data

3. **Modify**: `python {SKILL_DIR}/scripts/dt_modify.py --json "<found_path>" --id 230005 --set-loc-desc "新的描述文本"`
   → Modifies and validates

4. **Import**: Provide UE command for the user to run in editor

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| No UE project found | Project not in search paths | Use `--root` to specify project directory |
| No DataTable JSON found | JSON file not in Content directory | Check project structure, provide path manually |
| `UnicodeDecodeError` | Wrong encoding detection | Scripts auto-detect; if issues persist, check file BOM bytes |
| `fill_data_table_from_json_string` fails | JSON fields don't match RowStruct | Validate JSON, check for missing/extra fields |
| `DataTable not found` | Wrong asset path | Use `--asset-base` to specify correct UE asset path |
| P4 checkout failure | File locked by another user | Coordinate with team or force checkout |
