---
name: trpg-abbr-check-briefing
description: "Use this skill when checking and fixing English abbreviations in a briefing_package. Triggers on: check English abbreviations, fix abbreviations in briefing_package, 英文縮寫檢查, 縮寫修正."
agent_created: true
---

段落五：🔧 系統更新：檢查並替換 briefing_package 中的英文縮寫

你的 briefing_package 需要全面檢查英文縮寫，確保所有玩家可能看到的遊戲術語都有中文全稱。

核心原則：
  玩家是真人——他們看到「STR」「DEX」「HP」這些英文縮寫時不一定知道是什麼意思。
  這不是寫給程式看的技術文檔，是玩家在遊戲中會接觸到的文字。

你需要檢查並修正的事：

1. 什麼樣的英文縮寫需要改
   - 遊戲術語：屬性名、技能名、狀態名、裝備名、怪物名——任何玩家在遊戲中會看到的詞
   - 格式要求：「中文全稱（縮寫）」。例如：
     ❌ 力量：決定物理攻擊力。STR 越高傷害越大。
     ✅ 力量（STR）：決定物理攻擊力。力量（STR）越高傷害越大。
   - 不只標題和定義要改，正文中每次出現也要用全稱——玩家可能在任意位置讀到

2. 什麼樣的英文可以保留不改
   - YAML 的鍵名（例如 config.yaml 中的 name:、dice:、attributes: 等結構欄位）
   - map_config 的 type:、node_types: 等系統內部標識
   - context_hooks 的關鍵詞（玩家用中文說出即可，設定時也是用中文關鍵詞）
   - 純數值、公式、程式碼片段
   簡單判斷：「這個詞會出現在玩家看到的遊戲文字中嗎？」
   - 會 → 必須補中文全稱
   - 不會 → 可以保留英文

3. rules_sections/ 中的檔案要特別注意
   - rules_sections/ 有雙重角色：既是 AI 的參考資料，AI GM 也可能直接引用給玩家看
   - 例如玩家說「我想看裝備」，AI GM 會把規則段落中的裝備列表貼給玩家
   - 因此 rules_sections/ 中的術語同樣必須使用「中文全稱（縮寫）」格式
   - 不要因為放在 rules_sections/ 就全用英文縮寫

4. 檢查範圍
   - briefing_package 內所有檔案：config.yaml、system_prompt.md、rules_compact.md、scenarios/*.yaml、data/*.yaml、rules_sections/*.md
   - briefing_package 外的規則和劇本檔案也要一併檢查

5. 常見需要檢查的英文縮寫類別
   - 屬性（STR、DEX、CON、INT、WIS、CHA…）
   - 衍生值（HP、MP、SP、AC、DC…）
   - 狀態效果（Stun、Poison、Burn、Freeze、Bleed…）
   - 裝備稀有度（Common、Rare、Epic、Legendary…）
   - 傷害類型（Physical、Magic、Fire、Ice、Lightning、Holy、Dark…）
   - 技能類型（Active、Passive、Aura、Buff、Debuff…）
   - 檢定類型（Skill Check、Saving Throw、Attack Roll…）
   - 貨幣/資源（Gold、Silver、EXP、AP、SP…）

6. 屬性對照表的縮寫例外規則（僅限表格內）

在屬性對照表（或其他有「屬性中文名」欄位的表格）中，如果同一列的前一格已經是該屬性的中文全稱，則當前格的縮寫不重複包裝，直接用純縮寫。這是為了避免「根骨」和「根骨（GUG）」在同一列連續出現兩次。

適用此例外的縮寫：所有屬性縮寫均適用此例外規則（如 GUG、WUX、SHS 等——取決於當前規則自行定義的屬性縮寫）。不適用此例外的縮寫（仍照主規則包裝，即使在前一格已有中文名也照包）：HP、DC、CR、AC、TN、MoS、MoF、GS、EL、AOE 等所有非屬性的衍生值/系統縮寫。

判斷邏輯：對表格的每一列，從第 2 欄起逐一檢查——
  - 若當前格文字是「中文全稱（縮寫）」形式；
  - 且前一格去除 ** 粗體記號和空白後，正好等於那個中文全稱；
  - 就把當前格還原成純縮寫。

範例（Markdown 表格）：
  ❌ 根骨 | 根骨（GUG） | 修煉速度、突破檢定
  ✅ 根骨 | GUG | 修煉速度、突破檢定

範例（衍生值同理）：
  ❌ 生命值 | 生命值（HP） | 角色當前的生命值
  ✅ 生命值 | HP | 角色當前的生命值

⚠️ 只在同列已有中文全稱時才還原。若前一格不是該全稱，不要動。
⚠️ 繁簡必須一致才能觸發對應，屬性名一律使用繁體。

檢查方法：
  逐行掃讀所有 .md 和 .yaml 檔案。看到「括號內只有英文且沒有前導中文」的地方——
  這些就是需要補上中文全稱的位置。

⚠️ 過渡檔案提醒：檢查 briefing_package 內所有正式檔案 + briefing_package 外的最新版正式規則 / 劇本 / 角色卡。如果資料夾中有明顯的過渡檔案（如「舊版_」、「備份_」、「v1_」開頭，或檔名帶有「_old」「_bak」「草稿」等標記，或內容與正式檔案高度重複但已被正式檔案取代），不要浪費時間檢查和修改它們。快速判斷法：這個檔案裡有沒有正式檔案沒有的、且仍需保留的內容？沒有 → 跳過。

⚠️ 效率提示：英文縮寫替換通常涉及十幾個甚至幾十個檔案。請同時讀取所有需要檢查的檔案，批量替換縮寫後同時寫回。所有檔案的縮寫規則一致，不需要逐個檔案逐行慢慢改——同時處理才是正確做法。