---
name: trpg-guided-char-creation
description: "Use this skill when adding or updating guided character creation steps in a briefing_package. Triggers on: guided character creation, 引導式創角, 創角步驟, character creation steps."
agent_created: true
---

段落四：🔧 系統更新：檢查你的 briefing_package 創角是否需要改成引導式創角

你的 briefing_package 需要檢查創角方式。系統現在支援兩種模式，根據規則的創角流程複雜度選擇合適的模式。

兩種創角模式：

  模式一：標準表單創角（純數值分配）
    - 適用場景：創角流程簡單——就是分配屬性點
    - 設定方式：在 config.yaml 中定義 point_budget + cost_rules + backgrounds
    - 玩家體驗：在瀏覽器表單中手動輸入數字，完成後開始遊戲
    - 範例：
      character_creation:
        point_budget: 25
        base_value: 1
        cost_rules:
          "2-5": 1
          "6-10": 2
        soft_cap: 10
        backgrounds:
          - name: "無"
            bonuses: {}

  模式二：引導式創角（多步驟選擇型）
    - 適用場景：創角需要多步驟決策——先選種族、再選職業、再配屬性
    - 設定方式：在 config.yaml 中定義 steps + budget_points + max_initial
    - 玩家體驗：遊戲開始時可選「引導式創角」，AI GM 會一次一步地引導，像對話一樣完成創角
    - 範例：
      character_creation:
        budget_points: 8
        max_initial: 5
        steps:
          - "選擇種族（5選1）"
          - "選擇職業（6選1）"
          - "分配屬性點（8點自由分配）"

你可以同時定義兩種模式——玩家在開始遊戲時自由選擇用哪種方式。

你需要檢查並修正的事：

1. 判斷你的規則適合哪種模式
   - 如果創角只是分配屬性點 → 標準表單創角即可
   - 如果創角有多個步驟、需要做多輪選擇 → 加入引導式創角的 steps
   - 如果兩者都有（既有屬性點又有前置選擇）→ 同時定義兩種模式

2. 引導式創角的 steps 設計原則
   - 每個 step 是一句話描述，說明這個步驟要做什麼
   - AI GM 會根據 step 描述來引導玩家（例如："現在請選擇你的種族，以下是可選項..."）
   - 步驟中的具體選項（種族列表、職業說明等）應放在 data/ 或 rules_sections/ 中，讓 AI 可以查閱
   - 步驟數量建議 3-5 步，太多會讓玩家失去耐心

3. 檢查完整性
   - 如果使用引導式創角，確保相關的種族/職業/背景資料存在於 data/ 或 rules_sections/
   - AI GM 需要這些數據才能在引導過程中正確介紹選項

判斷流程：
  問自己：「創角時玩家需要做幾輪選擇？」
  - 1 輪（純分配點數）→ 只用標準表單
  - 2+ 輪（先選 X，再選 Y，再配屬性）→ 加入引導式創角 steps

⚠️ 過渡檔案提醒：創角規則的正式定義在 config.yaml 的 character_creation 區塊中。如果 briefing_package 外還有獨立的「角色創建規則.md」或「創角流程.txt」等檔案，先判斷：內容已全部整合進 config.yaml 了 → 過渡檔案，不要修改。如果是最新版正式角色卡 / 角色創建文件（尚未整合進 config.yaml）→ 需要修改。所有 config.yaml 已有的創角設定只改 config.yaml 一處，不要為了「同步」去改已被取代的過渡版本。

⚠️ 效率提示：如果引導式創角需要同時更新 config.yaml 和多個相關數據檔案（如 data/ 中的種族列表、rules_sections/ 中的職業說明），請同時修改所有相關檔案，不要逐個處理。