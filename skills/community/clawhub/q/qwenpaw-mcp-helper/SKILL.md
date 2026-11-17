---
name: qwenpaw-mcp-helper
description: QwenPaw MCP 設定與診斷。用於檢查 MCP 配置、驗證伺服器連線、提供設定範例，並診斷 MCP 連接問題。
metadata:
  version: "1.0.0"
  openclaw:
    requires:
      bins:
        - qwenpaw
        - python3
        - curl
      env: []
---

# QwenPaw MCP Helper

檢查、診斷與改善 QwenPaw 的 MCP 設定。

## 適用時機

- 新增 MCP 伺服器前後檢查
- MCP 工具無法執行
- 配置檔語法錯誤
- 連接超時或認證失敗

## 不做的事

- 不自動安裝 MCP 伺服器
- 不處理需要額外 API Key 的 MCP 服務
- 不修改使用者密碼或金鑰

## 檢查流程

每次執行依序跑下列檢查，並產出結構化報告。

### 1. MCP 配置

```bash
cat ~/.qwenpaw/config.json | python3 -c "import sys, json; cfg=json.load(sys.stdin); print(json.dumps(cfg.get('mcp', {}), indent=2))"
```

- 預期：可讀取 MCP 區段
- 異常：格式錯誤 → 提示修復 JSON

### 2. MCP 伺服器連線

對每個設定的 MCP 伺服器執行探測：

```bash
curl -s -o /dev/null -w "%{http_code}" <mcp-server-url>
```

- 預期：200 / 401（需要認證）
- 異常：連線失敗 → 檢查 DNS、port、firewall

### 3. QwenPaw MCP 狀態

```bash
qwenpaw mcp list 2>&1
```

- 預期：正常列出 MCP 客戶端
- 異常：錯誤訊息 → 依內容給建議

### 4. 常見問題排查

- 認證失敗：檢查 env / config 中的 key
- 逾時：檢查伺服器負載與網路延遲
- 重複工具名稱：檢查多個 MCP 是否衝突

## 報告格式

```markdown
## QwenPaw MCP Helper Report

- MCP Config: <有效 / 無效>
- Servers: <數量>
- Connected: <數量>
- Failed: <數量>

### Issues
1. <問題描述>
2. <問題描述>

### Suggestions
1. <具體修復步驟>
2. <具體修復步驟>
```

## 使用範例

```bash
# 執行 MCP 檢查
qwenpaw mcp-check
```
