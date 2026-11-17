---
name: trpg-maps-update
description: "Use this skill when updating or fixing the map system in an existing briefing_package. Triggers on: update maps, fix map system, add map_config, 地圖系統更新, 补上地图."
agent_created: true
---

段落二：🔧 系統更新：補上並檢查 briefing_package 的地圖系統

你的 briefing_package 需要支援地圖功能。以下是更新要求：

1. 建立 maps/ 目錄（如果還不存在）
   - 在 briefing_package 中建立 maps/ 資料夾
   - 用來存放中大型劇本地圖（80+ 行的 YAML 節點資料）

2. 將大型地圖從 data/ 移到 maps/
   - 如果你的 data/ 中有地圖 YAML（含 nodes、edges、regions 結構），請移到 maps/
   - ⚠️ 地圖不應該放在 data/——data/ 中的檔案每回合都注入 AI 上下文，大型地圖會嚴重浪費 token
   - maps/ 中的檔案不會自動注入，僅在遊戲啟動時載入地圖面板

3. 場景 YAML 改用 map_ref
   - 將場景 YAML 中原有的 initial_map 修改為 map_ref（如果地圖超過 80 行）
   - 格式：map_ref: "maps/地圖檔案名"（不含 .yaml 副檔名）
   - 例如：map_ref: "maps/墓地"

4. config.yaml 中加入 map_config（可選但推薦）
   - 如果規則需要可視化地圖，在 config.yaml 中加入 map_config 區塊：
     map_config:
       type: "dungeon"        # 地圖類型：starmap / dungeon / tactical / world
       title: "地圖面板標題"    # 地圖面板標題
       node_types:            # 節點類型及顏色（可選）
         - name: "入口"
           color: "#22c55e"
         - name: "主室"
           color: "#3b82f6"
       edge_types:            # 連線類型（可選）
         - name: "通道"
           color: "#6b7280"

5. 地圖 YAML 的標準格式（maps/ 和 initial_map 通用）：
   nodes:
     - id: "node_id"
       label: "節點顯示名稱"
       x: 0; y: 0; type: "節點類型"; explored: true
   edges:
     - from: "node_a"; to: "node_b"; type: "連線類型"
   regions:
     - name: "區域名稱"; color: "rgba(R,G,B,0.1)"; nodes: ["node_a", "node_b"]

⚠️ 地圖必須是 YAML 結構化格式，不要只用圖片或 ASCII 圖。
⚠️ 小型地圖（< 80 行）可保留在場景 YAML 的 initial_map 中，不需要強制移到 maps/。

⚠️ 過渡檔案提醒：如果 briefing_package 外還有獨立的舊地圖檔案（如「地圖_v1.yaml」、「舊版地圖/」等），它們是已被整合進 maps/ 的過渡檔案——不要修改它們。只改 briefing_package 內的正式地圖和場景 YAML，以及 briefing_package 外的最新版正式劇本地圖。如果發現 data/ 中還有舊的地圖 YAML 未被移走，將內容移到 maps/ 後直接刪除 data/ 中的那份，不要兩邊都保留同步修改。

⚠️ 效率提示：如果有多個場景 YAML 需要更新 map_ref，或多張地圖需要從 data/ 移到 maps/，請同時處理所有相關檔案，不要逐個場景逐張地圖慢慢改。