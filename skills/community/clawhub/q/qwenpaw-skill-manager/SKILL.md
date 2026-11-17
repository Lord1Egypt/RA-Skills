---
name: qwenpaw-skill-manager
description: QwenPaw 技能生命周期管理。用於列出、檢查、啟用、停用、更新和刪除技能，並追蹤技能使用狀態。
metadata:
  version: "1.0.0"
  openclaw:
    requires:
      bins:
        - qwenpaw
        - python3
      env: []
---

# QwenPaw Skill Manager

管理 QwenPaw 技能的完整生命周期。

## 適用時機

- 清理未使用的技能
- 批量啟用或停用技能
- 檢查技能更新
- 審計技能使用情況

## 不做的事

- 不自動安裝未經驗證的技能
- 不修改技能池內建技能
- 不處理需要登入或付費的技能市場操作

## 管理功能

### 列出技能

```bash
qwenpaw skills list
qwenpaw skills list --pool
```

### 檢查更新

```bash
qwenpaw skills update --dry-run
```

### 啟用/停用

```bash
qwenpaw skills enable <skill-name>
qwenpaw skills disable <skill-name>
```

### 刪除技能

```bash
qwenpaw skills uninstall <skill-name>
```

## 報告格式

```markdown
## Skill Manager Report

- Total Skills: <數量>
- Enabled: <數量>
- Disabled: <數量>
- Pool: <數量>

### Actions Taken
1. <操作記錄>
2. <操作記錄>

### Recommendations
1. <建議>
2. <建議>
```

## 使用範例

```bash
# 列出所有技能
qwenpaw skills list

# 檢查更新
qwenpaw skills update --dry-run
```
