---
name: sumo-smart-note
version: 1.0.0
description: Smart note-taking skill for 蘇茉家族. When master says "記下來" (record this), automatically save development notes to both workspace AND SumoNoteBook raw/shared.
---

# Sumo Smart Note Skill 📝

智能筆記技能 - 當老爺說「記下來」時，自動同步到 SumoNoteBook

## 觸發關鍵字

- 「記下來」
- 「記錄這個」
- 「把這個記錄下來」
- 「寫下來」
- 「存檔這個」
- 「/sumo_note」

## 功能

當老爺說要記下來時，蘇茉會：

1. **保存到本地 workspace**
   - 路徑：`memory/YYYY-MM-DD.md` 或 `memory/development_log.md`
   - 包含：時間戳、對話內容、開發過程、問題、解法

2. **同步到 SumoNoteBook**
   - 路徑：`C:/butler_sumo/library/SumoNoteBook/raw/shared/`
   - 檔名格式：`{timestamp}__{source}>_{title}.md`

3. **自動提取摘要**
   - 建立概念到 Sumo_wiki（可選）

## 輸出格式

```markdown
# 開發記錄 - {timestamp}

## 主題
{標題}

## 過程
{開發過程描述}

## 問題
{遇到的問題}

## 解法
{解決方案}

## 標籤
#development #problem-solving #sumo家族

## 来源
{source workspace}
```

## 使用方式

```
老爺：蘇茉，記下來，我剛剛解決了...
蘇茉：好的，已記錄！
  - 保存到 memory/development_log.md
  - 同步到 SumoNoteBook/raw/shared/
```

## 技術細節

- 使用 Python 指令碼同步檔案
- 自動去重（根據檔名和內容 hash）
- 保留原始時間戳