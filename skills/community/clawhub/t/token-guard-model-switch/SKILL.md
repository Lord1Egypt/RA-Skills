---
name: token-guard-model-switch
description: "主動監控 Token 使用率與上下文壓力，防止對話中斷並自動引導切換至備援模型。"
metadata:
  version: "1.1.0"
  openclaw:
    requires:
      bins: ["node"]
  config:
    threshold_warning: 0.85
    threshold_critical: 0.95
    model_pool:
      fast: ["gpt-4o-mini", "claude-3-haiku", "gemini-1.5-flash"]
      quality: ["gpt-4o", "claude-3-5-sonnet", "gemini-1.5-pro"]
      backup: ["local-llama-3"]
---

# Token Guard + Model Switch 運作規範

## [權限準則] 優先執行本地工具
1.  **禁止自動聯網**：執行監控任務時，嚴禁調用 `web_search` 或 `brave_search` 等需要外部 API 的工具。
2.  **本地腳本優先**：當需要獲取狀態或執行運算時，必須優先調用 `C:\Users\user\.openclaw\skills\token-guard-model-switch\scripts\` 目錄下的腳本。

## [監控階段] 狀態檢查
在執行任務的關鍵節點，或感覺回應變短、系統變慢時，你必須主動確認狀態：
1. 執行 `/status` 或 `/usage tokens`。
2. **[自動化工具]** 調用本地 `node scripts/monitor.js <current> <max> <model>`。
3. 計算：`ratio = current_tokens / max_context_window`。

---

## [觸發階段] 風險評估
當比值符合以下狀況，立即介入：
- **警告 (Ratio > 0.85)**: 準備提示使用者，並建議執行 `/compact`。
- **緊急 (Ratio > 0.95 或 收到 Quota 錯誤)**: 必須暫停當前任務，優先進行模型切換或硬性壓縮。

---

## [觸發後的提醒訊息格式]
當觸發時，請從以下模型池挑選最適合的填入模板，並使用以下格式回報：

**當前建議模型池 (2026 基準):**
- **快速型 (Fast):** `gpt-5-instant`, `gemini-3-flash`, `claude-4.5-haiku`
- **高品質 (Quality):** `gpt-5.3-codex`, `claude-4.6-opus`, `gemini-3-pro`
- **備援/私有 (Local):** `llama3.2:3b`, `deepseek-v2.5`, `qwen2.5:7b` (使用 Ollama)

---
### 🛡️ Token Guard 狀態回報
**【風險等級：緊急 (Critical) 🔴】** 
- **目前狀態：** 雲端 API 額度耗盡 / 連線中斷
- **處置建議：** 立即切換至本地運作以維持任務不中斷。

**請選擇處置方案：**
1. **[等待]** 稍後重試雲端 API。
2. **[切換本地]** 使用 Ollama 啟動：`llama3.2:3b` (快速)。
3. **[強大本地]** 使用 Ollama 啟動：`deepseek-v2.5` (適合寫程式)。
4. **[隱私模式]** 切換至 `qwen2.5:7b`。
---

## [使用流程]
一旦使用者選定（例如選擇 2）：
1. **第一步：** 執行 `/compact` (確保歷史記錄已總結)。
2. **第二步：** 使用 `sessions.patch` 或對應工具修改當前 Session 的 `model` 參數。
3. **第三步：** 執行 `/status` 確認切換成功。
4. **第四步：** 恢復原本任務，並告知：「已完成無縫切換，請檢閱上述狀態。」

---

## 安全與隱私規範
- **禁制：** 嚴禁要求使用者提供 API Key 或敏感資訊。
- **透明：** 若系統自動切換（如偵測到 429 錯誤且有預設備援），必須明確告知使用者「為何切換」以及「切換到了哪裡」。
- **最小權限：** 若需要供應商用量查詢，只讀取環境變數（ENV）並只回報「剩餘比例/區間」，不回傳敏感原始值。
