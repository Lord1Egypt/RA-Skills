# Soul Memory System v3.5.2 - Release Notes

## 🚀 版本亮點 (v3.5.2)

本次升級重點在於實現**長期記憶庫的智慧歸檔**與**自動化語境注入**，徹底解決了記憶膨脹與手動更新的痛點。

### 🛠️ 核心功能增強

| 功能 | 說明 |
| :--- | :--- |
| **增量合併架構 (Incremental Merge)** | 通過 `soul"..."` 標籤，將記憶碎片自動歸檔至 `soul_memory.md`，保留歷史軌跡而非暴力覆蓋。 |
| **智慧去重 (Smart De-duplication)** | 引入 `difflib.SequenceMatcher`，相似度超過 90% 的記憶條目將被判定為冗餘並自動跳過寫入。 |
| **自動上下文注入 (Context Injection)** | 系統現在能偵測特定關鍵詞（如 `QST`），自動從 `soul_memory.md` 中提取相關標籤區塊並注入思考環境。 |
| **時間戳標記** | 所有歸檔區塊自動添加 `(Updated: YYYY-MM-DD HH:MM)`，確保知識的新鮮度可視化。 |

### 🔧 優化項目

- **程式碼結構**：新增 `modules/soul_merge.py` 處理歸檔逻辑。
- **Core 更新**：`core.py` 整合 `soul_merge`，實現原子化的記憶更新與索引觸發。
- **GitHub 同步**：代碼與 README 已完整同步至 GitHub 倉庫 `kingofqin2026/Soul-Memory-`。

### 🧬 使用建議

陛下現在可以直接使用 `soul"標籤名"` 進行記憶歸檔。系統會自動處理去重與注入。例如：
```
soul"QST-理論" 最近審計證明馬赫數計算存在擬合問題...
```
系統將自動觸發 `merge_memory`，並在下一次對話中自動聯動此記憶。

---
*記錄於 2026-03-13 09:40 UTC*
