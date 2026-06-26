# AI Skills JSON Field Schema

Complete field documentation for the AI Skills DataTable JSON format.

## Skill Entry Structure

```json
{
    "Name": "230000",
    "SkillClass": "/Game/SMG/Core/Ability/AI/...",
    "Notice": "开发备注",
    "LOC_MonsterSkillTypeDisplays": ["NSLOCTEXT(...)"],
    "MonsterSkillTag": [],
    "CmdQueue_TGT_Display": { "TagName": "None" },
    "bUseAlert": false,
    "LOC_AlertText": "",
    "bUseNotice": false,
    "LOC_NoticeText": "",
    "bUseWarningTip": false,
    "LOC_InterruptMessage": "",
    "bIsDangerousSkill": false,
    "SkillFunctionType": 0,
    "LOC_Name": "NSLOCTEXT(\"DT_AI_Skills_Part1\", \"230000_LOC_Name\", \"技能名\")",
    "LOC_Desc": "NSLOCTEXT(\"DT_AI_Skills_Part1\", \"230000_LOC_Desc\", \"技能描述\")",
    "DevName": "开发用名",
    "TargetPicker": { "ID": 101 },
    "bDeathWhisper": false,
    "Settlement": {
        "Settlement": { "Name": "None" },
        "Impact": { "Name": "None" },
        "ImpactDelay": 0
    },
    "MultiSettlements": {},
    "ScriptPath": ""
}
```

## Field Details

### Identity Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `Name` | string | Yes | Skill ID (numeric string, e.g. "230000"). Acts as the row name in DataTable. |
| `SkillClass` | string | Yes | UE Blueprint class path for the Ability implementation. Format: `/Game/SMG/Core/Ability/AI/.../ClassName.ClassName_C` |
| `DevName` | string | Yes | Human-readable development name (Chinese). Used for internal reference. |
| `Notice` | string | Yes | Developer notes. Often contains monster name and skill type, e.g. "燃蜇（EMS1）蓄力" |

### Localization Fields

All LOC fields use `NSLOCTEXT` or `INVTEXT` format:
- `NSLOCTEXT("Namespace", "Key", "Text")` — Standard localized text
- `INVTEXT("Text")` — Invariant text (not localized)

| Field | Type | Description |
|-------|------|-------------|
| `LOC_Name` | string | Localized skill name displayed in UI |
| `LOC_Desc` | string | Localized skill description. Supports rich text tags like `<Chara_Pink_Regular_20>【text】</>` |
| `LOC_AlertText` | string | Alert message shown when `bUseAlert` is true |
| `LOC_NoticeText` | string | Notice text shown when `bUseNotice` is true |
| `LOC_InterruptMessage` | string | Message shown when skill is interrupted |
| `LOC_MonsterSkillTypeDisplays` | array | Skill type tags displayed in UI (e.g. "蓄力", "单体", "群体") |

### Boolean Flags

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `bUseAlert` | bool | false | Show alert/warning when this skill is about to be used |
| `bUseNotice` | bool | false | Show notice notification |
| `bUseWarningTip` | bool | false | Show warning tip indicator |
| `bIsDangerousSkill` | bool | false | Mark as a dangerous/threatening skill |
| `bDeathWhisper` | bool | false | This is a death whisper (last words) skill |

### Gameplay Fields

| Field | Type | Description |
|-------|------|-------------|
| `SkillFunctionType` | int | Skill function category. 0 = utility/passive, 1 = active combat |
| `MonsterSkillTag` | array | Gameplay tags for the skill |
| `CmdQueue_TGT_Display` | object | Command queue target display tag. `{"TagName": "None"}` for no display |
| `TargetPicker` | object | Target selection configuration. `{"ID": <picker_id>}` |
| `ScriptPath` | string | Optional script path for additional behavior |

### Settlement (Damage/Effect) Fields

| Field | Type | Description |
|-------|------|-------------|
| `Settlement` | object | Primary settlement configuration |
| `Settlement.Settlement` | object | `{"Name": "<settlement_id>"}` or `{"Name": "None"}` |
| `Settlement.Impact` | object | `{"Name": "<impact_id>"}` or `{"Name": "None"}` |
| `Settlement.ImpactDelay` | int | Delay before impact (in frames or ms) |
| `MultiSettlements` | object | Multi-hit settlement config. Empty `{}` when not used |

## ID Ranges (Part Mapping)

| Part | ID Range | DataTable Asset |
|------|----------|-----------------|
| Part0 | 200000 – 229999 | DT_AI_Skills_Part0 |
| Part1 | 230000 – 239999 | DT_AI_Skills_Part1 |
| Part2 | 240000 – 249999 | DT_AI_Skills_Part2 |
| Rogue | Other ranges | DT_AI_Skills_Rogue |

## Common TargetPicker IDs

| ID | Description |
|----|-------------|
| 1 | Default/Self |
| 100 | Position-based |
| 101 | Single enemy target |

## Rich Text Tags in LOC_Desc

The `LOC_Desc` field supports UE rich text formatting:
- `<Chara_Pink_Regular_20>text</>` — Pink colored text
- Other style tags follow UE's Rich Text Block format
