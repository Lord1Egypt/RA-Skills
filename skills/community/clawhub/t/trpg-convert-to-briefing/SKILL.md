---
name: trpg-convert-to-briefing
description: "Use this skill when converting TRPG rules into a briefing_package for the TRPG AI GM engine. Triggers on: convert to briefing_package, turn rules into AI format, 转换briefing_package."
agent_created: true
---

段落一：主任務指令（完整版）— 轉換 briefing_package

你是這個任務的 AI。你面前有一份 TRPG 規則文件。請把它轉換成 briefing_package，編輯當前資料夾中這些檔案：

  config.yaml — 規則定義
  system_prompt.md — AI GM 人格
  rules_compact.md — 規則摘要（精簡）
  scenarios/*.yaml — 每個劇本一個檔案
  data/*.yaml（可選）— 小型核心遊戲數據
  rules_sections/*.md（可選）— 大型參考數據（配合 context_hooks 使用）
  maps/*.yaml（可選）— 中大型劇本地圖

🚨 核心前提零：辨識過渡檔案，不要浪費時間修改已廢棄的中間版本

你需要修改的檔案範圍是：
  ✅ briefing_package 內所有正式檔案（config.yaml、system_prompt.md、rules_compact.md、scenarios/*.yaml、data/*.yaml、rules_sections/*.md、maps/*.yaml）
  ✅ briefing_package 外的最新版正式規則檔案、劇本檔案、角色卡等仍在使用的正式檔案

你不需要修改的是：
  ❌ 任何地方的過渡檔案——已被後續版本取代的中間版本檔案。例如：
     - 檔名帶有「舊版」「備份」「v1」「v2」「草稿」「_old」「_bak」等標記
     - 內容已被整合進 briefing_package 的獨立規則補充檔案（如「完整規則補充.md」的內容已拆分進 rules_sections/，該補充檔案即為過渡檔案）
     - 與主規則檔案內容高度重複但已被主檔案取代的副本

判斷方法：問自己「這個檔案裡有沒有 briefing_package 或主規則檔案沒有的、且仍然需要保留的內容？」
  - 有 → 這是正式檔案，需要修改
  - 沒有（所有內容都已被其他檔案覆蓋）→ 這是過渡檔案，忽略它

⚠️ 常見陷阱：任務 AI 看到兩個內容相似的檔案時，容易為了「保持同步」而兩邊都改。這只會浪費時間——過渡檔案終將被刪除，不需要維護。

🚨 核心前提一：批次平行處理，不要逐個檔案慢慢改

你需要修改的檔案數量通常很多。請按照以下高效流程工作，不要一個一個檔案逐個處理：

  第一步：規劃 ─ 收到指令後，先快速掃描所有需要修改的檔案，列出完整修改清單
  第二步：讀取 ─ 一次性同時讀取所有需要修改的檔案（互不依賴的讀取可以平行進行）
  第三步：修改 ─ 互不依賴的檔案同時修改，只有當 B 的內容依賴 A 的結果時才按順序處理

高效 vs 低效對比：

  ❌ 低效流程（逐個改）：
    讀 config.yaml → 改 config.yaml → 讀 system_prompt.md → 改 system_prompt.md
    → 讀 scenarios/S1.yaml → 改 S1 → 讀 scenarios/S2.yaml → 改 S2 → ...
    （N 個檔案要 N 輪，每輪都要等上一輪完成）

  ✅ 高效流程（批次處理）：
    同時讀取 config.yaml、system_prompt.md、rules_compact.md、所有 scenarios/*.yaml
    → 同時修改 config.yaml、system_prompt.md、rules_compact.md、所有 scenarios/*.yaml
    （所有檔案在一到兩輪內完成）

適用場景：修改多個 scenario YAML、更新多個 data/*.yaml、批量替換縮寫時尤其重要。

🚨 核心前提二：所有中文必須使用繁體中文 + 英文縮寫必須補上中文全稱

本 briefing_package 中所有 .md、.yaml 檔案內的任何中文文字，一律使用繁體中文（正體中文）撰寫。禁止使用簡體中文。包括但不限於：屬性名稱與描述、規則說明與判定條件、劇本敘述與 NPC 對話、裝備與技能描述、系統提示詞與 GM 人格定義。

玩家可見的遊戲術語必須採用「中文全稱（縮寫）」的統一格式。不得出現只有英文縮寫而沒有中文全稱的情況。例如：
  屬性：力量（STR）、敏捷（DEX）、智力（INT）
  衍生值：生命值（HP）、魔法值（MP）
  狀態：暈眩（Stun）、中毒（Poison）
  裝備稀有度：普通（Common）、稀有（Rare）、傳說（Legendary）

純技術性 Key（如 YAML 的鍵名、map_config 的 node_types 等只在系統內部流通的標識）可以保留英文。

⚠️ 雙重角色提醒：rules_sections/ 中的檔案雖然不會自動注入，但 AI GM 會在玩家觸發關鍵詞後直接引用其中的內容給玩家看。因此 rules_sections/ 中的遊戲術語同樣必須使用「中文全稱（縮寫）」格式——它既有 AI 查閱的角色，也有玩家可見的角色。不要因為它放在 rules_sections/ 就全用英文縮寫。

⚠️ 檢查範圍：不只 briefing_package 內的檔案，briefing_package 外的規則檔案和劇本檔案也必須進行同樣的檢查。

🚨 核心前提三：這是單人 TRPG。只有一位玩家 + AI GM，沒有多人。

只保留單人適用的內容：
✅ 保留：
  - 玩家 vs 環境（檢定、探索、生存、資源管理）
  - 玩家 vs NPC/怪物（戰鬥、交涉）
  - 獨行玩家會用到的系統（潛行、駭入、撤離等）
  - 玩家與 NPC 夥伴/隨從的協同機制（指令、戰術配合、羈絆系統等）← 這是單人可控的隊伍
❌ 刪除 / 忽略：
  - 多人類玩家的角色定位（坦/補/輸出的隊伍分工）
  - 多個玩家之間才能實現的協同技能
  - 多人社交判定（玩家間互相對抗、說服其他玩家）
  - PvP 規則
  - 需要多個人類玩家同時行動的機制

如果原始規則同時包含單人和多人內容，只提取單人部分。

🚨 重要：轉化過程中遇到未預料的情況時，暫停轉化並直接輸出完整問題

在將原始規則轉化為 briefing_package 的過程中，如果你遇到以下情況，請不要猜測、不要跳過、不要自行假設處理——立即暫停轉化工作，直接輸出你的完整問題：

  - 原始規則的某個機制或設定與 briefing_package 的標準結構明顯衝突，你不確定該如何對應
  - 原始規則中存在模糊、矛盾或缺失的關鍵資訊，但你又無法從上下文合理推斷
  - 某個設計決策存在多種合理方案，而原始規則沒有明確指定選哪一種
  - 你發現原始規則的某個設計可能導致遊戲平衡問題或邏輯漏洞，需要確認原始意圖

輸出問題時請包含：
  1. 你遇到問題的具體位置（原始規則的哪一章/哪一段）
  2. 問題的具體內容（什麼機制/設定讓你不確定如何處理）
  3. 你已經考慮過的幾種可行方案（簡述每個方案的優缺點）
  4. 你需要的決策是什麼（請用一句話明確提問）

⚠️ 這條規則的優先級高於「根據已有設定合理補充」——當你不確定時，問出來比猜測更重要。


你需要做的事：

config.yaml：
  - 替換所有 <FILL_THIS> 佔位符
  - 定義屬性（name + desc，數量由你決定）。玩家可見的屬性名採用繁體中文
  - 設定擲骰機制（mechanics.dice）、特殊系統標記（mechanics.special）
  - context_hooks：關鍵詞觸發表。玩家說出關鍵詞時自動注入對應的規則段落。格式為 "關鍵詞": "rules_sections/檔案名"。引用的檔案必須存在於 rules_sections/ 目錄中（可選）
  - map_config：如果規則需要可視化地圖，定義地圖類型（dungeon / starmap / tactical / world）、面板標題、節點和連線類型（可選）
  - character_creation：角色創建規則（可選，格式由你設計）。支援兩種模式：
      * 標準表單創角：point_budget + cost_rules + backgrounds。玩家在瀏覽器表單中手動分配屬性點
      * 引導式創角：steps + budget_points + max_initial。如果創角需要多步驟選擇（如先選種族→再選職業→再配屬性），定義 steps 列表。遊戲開始時玩家可選「引導式創角」，AI GM 會按步驟一次一步地引導完成。步驟中的具體選項（種族列表、職業說明等）可放 data/ 或 rules_sections/ 供 AI 查閱
    可以同時定義兩種模式，玩家自由選擇

system_prompt.md：
  - 定義 AI GM 人格、世界觀、GM 風格、規則執行原則
  - 記得 AI GM 只需面對一位玩家
  - 格式完全自由，沒有強制章節

rules_compact.md：
  - 核心機制的精簡摘要，控制篇幅（AI 上下文有限）
  - 只寫單人遊戲相關的機制，省略多人規則
  - 只寫關鍵：檢定機制、戰鬥、特殊系統
  - 不要寫世界觀（那在 system_prompt）、不要寫裝備完整列表（放 rules_sections/）

scenarios/*.yaml：
  - 結構完全自由，以最能呈現劇本內容的方式寫
  - 可包含：名稱、開場、難度、裝備、場景、NPC、遭遇、目標、獎勵
  - 劇本必須設計為單人可完成
  - 如果劇本有具體空間結構（地下城、星圖、城鎮等），加入地圖。兩種方式：
      * maps/ 目錄 + map_ref（推薦——中大型地圖，80+ 行 YAML）：在 maps/ 中建立地圖檔案，場景中用 map_ref 引用
      * initial_map 內嵌（小型地圖，< 80 行）：直接在場景 YAML 的 initial_map 欄位中定義 nodes、edges、regions
  - ⚠️ 地圖必須是 YAML 結構化格式（nodes + edges + regions），不要只用圖片或 ASCII 圖

data/*.yaml（如有）：
  - 技能列表、常用裝備屬性、消耗品效果等小型核心數據
  - 格式由你根據數據特性設計
  - ⚠️ data/ 中的檔案會在每一回合自動注入 AI 上下文。每個檔案建議小於 50 行——數據量小且每回合都需要的才放這裡

rules_sections/*.md（如有）：
  - 大型詳細數據：完整裝備大全、魔法書、怪物圖鑑等
  - ⚠️ rules_sections/ 中的檔案不會自動注入——只有在玩家說出 context_hooks 中設定的關鍵詞時才載入
  - 適合量大（50+ 行）、偶爾查詢的參考數據
  - 檔案中的遊戲術語採用「中文全稱（縮寫）」格式，因為 AI GM 可能在回覆中直接引用給玩家看

maps/*.yaml（如有）：
  - 中大型劇本地圖（80+ 行的 YAML 節點資料）
  - 格式與 initial_map 相同：nodes、edges、regions
  - ⚠️ maps/ 中的檔案不會注入 AI 上下文——僅在遊戲啟動時載入地圖面板
  - 不要將地圖 YAML 放在 data/ 中（data/ 每回合都注入，大型地圖會浪費大量 token）

核心原則：模板結構僅供參考。根據規則的實際需求自由調整。不存在的內容直接省略。唯一的硬約束是替換所有 <FILL_THIS>。

數據放置速查：
  數據量小（< 50 行）+ 每回合用到 → data/
  數據量大（50+ 行）+ 偶爾查詢 → rules_sections/ + context_hooks
  中大型地圖（80+ 行）→ maps/ + map_ref
  小型地圖（< 80 行）→ 場景內嵌 initial_map