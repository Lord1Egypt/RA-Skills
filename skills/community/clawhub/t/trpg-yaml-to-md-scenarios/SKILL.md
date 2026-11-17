---
name: trpg-yaml-to-md-scenarios
description: "Use this skill when generating human-readable Markdown scenarios from existing YAML scenario files. Triggers on: generate MD from YAML scenarios, YAML to MD scenario, YAML轉MD劇本."
agent_created: true
---

📝 任務：從現有 YAML 劇本補生成 MD 劇本

你是這個任務的 AI。這套 TRPG 規則中的劇本目前只有 .yaml 格式（給 AI GM 吃的結構化資料），缺少 .md 格式（給真人 GM 和玩家閱讀的自然段落敘述）。請為每一份現有的 YAML 劇本補生成對應的 MD 版本。

資料來源：工作空間中 scenarios/ 目錄下的現有 .yaml 劇本檔案，以及 briefing_package 內的 scenarios/ 目錄中的 .yaml 檔案。

你要做的事：

讀取每一個 YAML 劇本，將其中的結構化資料轉化為流暢自然的段落敘述，生成對應的 .md 檔案，存放在原本 YAML 檔案的同一目錄中，使用相同檔名、不同副檔名。例如 scenarios/S1_劇本名稱.yaml → scenarios/S1_劇本名稱.md。

MD 劇本應包含以下內容（根據 YAML 中的實際資料決定哪些章節適用）：

  - 劇本名稱與建議等級範圍
  - 開場描述（從 description 欄位展開為沉浸式敘述）
  - 場景流程（將場景/關卡結構轉化為自然語言段落）
  - 關鍵 NPC（角色名稱、外觀、性格、對話範例、在劇本中的角色）
  - 遭遇資訊（敵人類型、數量、觸發條件、戰術建議）
  - 地圖說明（如果 YAML 中有 map_ref 或 initial_map，在 MD 中描述空間佈局，並標註可參考對應的 SVG 視覺地圖）
  - 目標與獎勵（任務目標、完成條件、獎勵內容）
  - GM 備註（任何 YAML 中有但不容易放進自然敘述的幕後資訊）

格式要求：

  - 繁體中文
  - 使用 Markdown 格式（標題、列表、粗體、分隔線）
  - 排版清晰，可直接列印或在平板上閱讀
  - 不要用表格（純文字閱讀體驗）
  - 語氣自然、適合 GM 在跑團時直接參考或朗讀給玩家

⚠️ 不要修改原有的 .yaml 檔案。MD 是純粹的額外產出。
⚠️ 只處理正式 YAML 劇本，不要碰過渡檔案。