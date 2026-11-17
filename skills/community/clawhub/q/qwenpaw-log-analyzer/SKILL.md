---
name: qwenpaw-log-analyzer
description: QwenPaw 日誌分析與故障排查。用於分析 QwenPaw 日誌、檢測錯誤與警告、提供修復建議，並輸出結構化報告。
metadata:
  version: "1.0.0"
  openclaw:
    requires:
      bins:
        - qwenpaw
        - python3
        - grep
        - tail
      env: []
---

# QwenPaw Log Analyzer

分析 QwenPaw 日誌，快速定位錯誤、警告與異常模式。

## 適用時機

- QwenPaw 閃退或無法啟動
- 技能/插件載入失敗
- 效能異常或延遲升高
- 安全事件排查

## 不做的事

- 不自動修改日誌檔案
- 不上傳日誌到外部服務
- 不處理需要額外權限的系統日誌

## 分析範圍

- `~/.qwenpaw/logs/`
- `~/.qwenpaw/state/`
- QwenPaw app 日誌
- 安全掃描日誌
- 插件載入日誌

## 使用方式

```bash
# 分析最近日誌
qwenpaw log-analyze --tail 100

# 分析特定檔案
qwenpaw log-analyze --file /path/to/qwenpaw.log

# 產生報告
qwenpaw log-analyze --report
```

## 報告格式

```markdown
## QwenPaw Log Analyzer Report

- Log File: <路徑>
- Analyzed At: <時間>
- Total Lines: <數量>
- Errors: <數量>
- Warnings: <數量>

### Issues
1. <問題描述> - <次數>
2. <問題描述> - <次數>

### Suggestions
1. <修復建議>
2. <修復建議>
```
