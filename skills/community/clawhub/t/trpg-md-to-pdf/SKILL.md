---
name: trpg-md-to-pdf
description: "Use this skill when converting TRPG markdown files (rulebooks, scenarios, catalogs) to PDF format. Triggers on: convert to PDF, export PDF, generate PDF, 轉PDF, 导出PDF."
agent_created: true
---

📄 任務：將跑團用 MD 檔案轉換為 PDF

你是這個任務的 AI。你已經完成了整套 TRPG 規則的撰寫。現在請將跑團時實際會用到的 .md 檔案轉換為 PDF 版本，供玩家和 GM 列印或在平板上閱讀。

轉換範圍（只轉換跑團用檔案）：

  1. 玩家規則書（.md）→ 同名 .pdf
  2. GM 規則書（.md）→ 同名 .pdf
  3. 所有劇本（scenarios/ 目錄下的 .md 檔案，如有）→ 同名 .pdf
  4. 所有圖鑑（catalogs/ 目錄下的 .md 檔案，如有）→ 同名 .pdf
  5. 任何其他規則獨有、跑團時會實際使用的 .md 檔案 → 同名 .pdf

不需要轉換的檔案：

  ❌ 需求規格書（*需求規格書.md）
  ❌ 生成過程筆記.md
  ❌ 設計草稿、臨時筆記、任何過渡檔案
  ❌ briefing_package 內的任何檔案

轉換要求：

  - 每一份 .md 檔案轉換為一份同名 PDF，存放在同一目錄中
  - 保留原始 .md 的排版結構：標題層級、列表、粗體、斜體、分隔線、引用區塊
  - 中文字型正常顯示，不出現亂碼或方塊
  - PDF 可列印、可在平板/手機上閱讀
  - 若有圖片或 SVG 地圖嵌入在 .md 中，需確保在 PDF 中可見

⚠️ 不要修改原有的 .md 檔案。
⚠️ 轉換完成後，原本的 .md 檔案保留不動——PDF 是額外的產出。