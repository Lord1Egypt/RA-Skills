---
name: trpg-data-context-hooks
description: "Use this skill when reorganizing data/ and context_hooks in a briefing_package to avoid token waste. Triggers on: data vs context hooks, reorganize data files, 数据整理, context_hooks."
agent_created: true
---

段落三：🔧 系統更新：data/ vs context_hooks 使用指南與修正要求

你的 briefing_package 需要按照以下指南區分 data/ 和 context_hooks + rules_sections/ 的用途。

核心原則：
  這款 App 沒有真人 GM——AI GM 就是唯一 GM。
  所有 AI GM 執行遊戲時需要查閱的遊戲數據，都必須存在於 briefing_package 內部。
  但不同數據的注入方式不同，選錯方式會浪費大量 token。

data/ 和 context_hooks 的區別：

  data/*.yaml：
    - 注入時機：每一回合都自動注入 AI 上下文
    - 適用場景：小型核心數據——量少、每回合都需要
    - 大小建議：每個檔案 < 50 行
    - 例子：核心屬性定義、簡短技能列表、資源/貨幣系統

  context_hooks → rules_sections/*.md：
    - 注入時機：只有當玩家說出 config.yaml 中設定的關鍵詞時才注入
    - 適用場景：大型詳細數據——量大、偶爾查詢
    - 大小建議：無硬性限制，但建議每個檔案 < 200 行
    - 例子：完整裝備大全、魔法書、怪物圖鑑、世界設定百科

你需要檢查並修正的事：

1. 檢查 data/ 中的檔案大小
   - 如果 data/ 中有超過 50 行的檔案，考慮是否應該移到 rules_sections/ 並透過 context_hooks 觸發
   - 例如：一份 300 行的裝備大全放在 data/ 中，每回合都注入會浪費大量 token

2. 修正方式
   - 將大型數據從 data/ 移到 rules_sections/
   - 在 config.yaml 的 context_hooks 中加入對應的關鍵詞觸發
   - 例如：
     context_hooks:
       "裝備": "rules_sections/裝備大全"
       "魔法": "rules_sections/魔法書"
       "怪物": "rules_sections/怪物圖鑑"

3. 確保 rules_sections/ 中的檔案存在
   - context_hooks 引用的檔案必須實際存在於 rules_sections/ 目錄中
   - 因為 AI GM 是唯一 GM，沒有外部參考資料可以查閱

4. context_hooks 關鍵詞設計建議
   - 使用玩家在遊戲中會自然說出的詞
   - 不需要加前綴符號（如 / 或 !），自然語言即可
   - 設定覆蓋最常用的查詢場景即可，不需要窮舉

簡單判斷法：
  問自己：「AI GM 每一回合都需要看到這段數據嗎？」
  - 是 → 放 data/，但控制在 50 行以內
  - 否 → 放 rules_sections/，用 context_hooks 關鍵詞觸發

⚠️ 過渡檔案提醒：如果你發現 briefing_package 外還有獨立的規則補充檔案，先判斷它是過渡檔案還是正式檔案：如果它的內容已全部整合進 briefing_package（如原「完整規則補充.md」的內容已拆分進 rules_sections/），那它就是過渡檔案——不要修改。如果它是最新版正式規則檔案（briefing_package 尚未包含的內容），則需要修改。判斷標準：這個檔案裡有沒有 briefing_package 沒有的、且仍需保留的內容？沒有 → 過渡檔案，忽略。如果在 data/ 和 rules_sections/ 之間遷移了數據，遷移完成後刪除原位檔案，不要兩處各留一份同步修改。

⚠️ 效率提示：遷移數據時請批次處理——同時移動所有需要從 data/ 遷到 rules_sections/ 的檔案，同時更新 config.yaml 中所有對應的 context_hooks，不要逐個檔案逐步遷移。