# SKILL.md — Semantic Memory Boost

## Title
Semantic Memory Boost (S.M.B)

## Purpose
通過意圖解析、分層檢索與邏輯對齊，提升 AI 處理複雜問題時的上下文關聯性與歷史資料引用準確度。

## When to Use
- 當問題涉及多個跨時間維度的決策或專案時。
- 當需要解決「語義衝突」（例如：兩份檔案的規範不同）時。
- 當需要根據歷史脈絡來規劃新專案時。

## Required Inputs
- `user_query`: 原始問題。
- `domain_context`: 當前專案或情境鎖定。

## Workflow
1.  **意圖解析 (Intent Mapping)**：
    - 將問題拆解為 [QUERY_VECTOR_PLAN]，鎖定關鍵實體 (Entity) 與聯想詞。
2.  **分層檢索 (Tiered Retrieval)**：
    - `[ACTIVE_MEM]`：讀取當前會話的最佳實踐。
    - `[LONG_TERM_REF]`：檢索數據庫中的歷史規範與規格。
    - `[META_PATTERN]`：套用類似問題的通用模板。
3.  **語義對齊 (Content Alignment)**：
    - 檢查檢索結果是否與用戶意圖邏輯衝突，排除無關雜訊。
4.  **知識拼圖 (Synthesis)**：
    - 融合多個檢索片段，轉化為具備邏輯連貫性的答覆基礎。
5.  **記憶閉環 (Cleanup)**：
    - 完成回答後，執行 `[MEM_SUMMARIZATION]`，將本次對話的洞察存入對應的 memory 檔案。

## Constraints
- **Scope Limitation**：一次檢索的 token 應限制在 context window 的 30% 以內，避免碎片過多導致回應失焦。
- **Relevance Threshold**：若檢索片段的關聯分數 (Score) 低於 0.6，應將其視為弱信號，不作為核心決策依據。

## Output Format
- 結構化回答（符合 `SOUL.md` 風格）。
- 若有價值資產產生，需明確標註：`[MEM_SUMMARY: ...]`

## Self-Check Checklist
- [ ] 檢索結果是否足以回答用戶問題？
- [ ] 是否存在相互矛盾的檢索片段？（若有，是否已在回答中指出）
- [ ] 最終回答是否轉化為未來的記憶資產？

## Failure Modes
- **孤島數據**：檢索結果完全未能命中相關資訊（回報無相關記憶）。
- **語義干擾**：檢索到過多不相關但關鍵字重疊的內容（需縮小檢索區間或優化 Intent Mapping）。
