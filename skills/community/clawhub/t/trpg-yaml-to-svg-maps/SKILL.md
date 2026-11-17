---
name: trpg-yaml-to-svg-maps
description: "Use this skill when generating SVG visual maps from existing YAML map data in a TRPG project. Triggers on: generate SVG maps from YAML, YAML to SVG, 生成SVG地图, 视觉化地图."
agent_created: true
---

你是這個任務的 AI。你之前已經為這套 TRPG 規則生成了 YAML 格式的劇本地圖（nodes/edges/regions）。現在請為每一份 YAML 地圖補生成一份 SVG 視覺化地圖。

資料來源：工作空間中 maps/ 目錄下的現有 YAML 地圖檔案，以及 scenarios/ 目錄中場景 YAML 的 initial_map 欄位。

你要做的事：

讀取每一個 YAML 地圖的節點和連線資料，生成對應的 SVG 視覺化地圖。每張地圖輸出為一個獨立的 .svg 檔案，存放在原本 YAML 地圖的同一目錄中，使用相同檔名、不同副檔名。例如 maps/墓地.yaml → maps/墓地.svg。

SVG 地圖的視覺要求：

1. 節點使用圓角矩形顯示，內部標註節點名稱
2. 不同區域使用淺色半透明底色區分（不同區域用不同顏色）
3. 節點之間的連線使用線條 + 箭頭表示，連線上可標註通道名稱
4. 區域名稱標註在區域範圍的左上角
5. 地圖整體尺寸自適應內容，確保所有節點完整可見
6. 字體可讀、排版清晰——這是給真人 GM 在跑團時拿來看的

SVG 格式要求：

- 使用標準 SVG 語法，不需要 JavaScript
- 檔案可直接用瀏覽器打開查看，也可插入規則書中
- 所有文字使用繁體中文
- 節點和連線的顏色與區域顏色協調，整體乾淨清晰

⚠️ 不要修改現有的 YAML 檔案。SVG 是純粹的額外產出。
⚠️ 如果某個 YAML 地圖缺少節點座標（x/y 值），根據節點之間的關係合理推算位置。
⚠️ 只處理 maps/ 目錄和 scenarios/ 中 initial_map 的 YAML 地圖。不要處理 briefing_package 內的檔案。