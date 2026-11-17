---
name: qwenpaw-backup-manager
description: QwenPaw 資料備份與還原。用於備份技能、設定、會話歷史與記憶，並在需要時快速還原。
metadata:
  version: "1.0.0"
  openclaw:
    requires:
      bins:
        - qwenpaw
        - tar
        - gzip
      env: []
---

# QwenPaw Backup Manager

備份與還原 QwenPaw 的重要資料，包含技能、設定、會話歷史與記憶。

## 適用時機

- 升級前備份
- 遷移工作目錄
- 災難恢復
- 定期歸檔

## 不做的事

- 不自動上傳到外部雲端
- 不處理需要登入、API Key 或付費的備份服務

## 備份範圍

- `~/.qwenpaw/skill_pool/`
- `~/.qwenpaw/workspaces/`
- `~/.qwenpaw/memory/`
- `~/.qwenpaw/config.json`
- `~/.qwenpaw/sessions/`

## 使用方式

```bash
# 建立備份
qwenpaw backup create --name my-backup

# 列出備份
qwenpaw backup list

# 還原備份
qwenpaw backup restore --name my-backup
```

## 報告格式

```markdown
## Backup Report

- Backup Name: <名稱>
- Created At: <時間>
- Size: <大小>
- Items: <清單>

### Restore
<是否成功>
```
