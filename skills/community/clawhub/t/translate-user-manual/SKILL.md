---
name: translate-user-manual
description: 专业硬件说明书与技术文档翻译专家 (ManualExpert). Professional technical manual translator and DTP prep tool. Use when: (1) Translating hardware/technical manuals. (2) Extracting PDF text to 100% complete bilingual tables. (3) Exporting to Word (.docx) for DTP. Triggers: "翻译说明书", "生成中英对照", "导出为Word", "translate this manual", "generate bilingual table". Provides: Page-by-page structured bilingual tables.
---

# Manual Bilingual Exporter (ManualExpert)

This skill translates technical manuals by extracting the original text and outputting a structured bilingual table, bypassing complex PDF layout issues to ensure 100% translation coverage and accuracy.

## Core Translation Rules (The "Red Lines")

1. **Absolute Completeness (绝对完整，拒绝精简)**
   - Extract **ALL** visible text from the source manual (PDF or images).
   - Use as many tokens as necessary. **NEVER** skip, summarize, or condense text to save effort. Even small labels, footnotes, and UI text must be included.

2. **Strict Pagination (按页翻译，严禁合并)**
   - Translation must strictly follow the original page breaks (P1, P2, etc.).
   - **NEVER** merge pages. Even if a page contains only one line (e.g., a title), it must be rendered as a standalone page in the output.
   - Clearly delineate pages using Markdown headers (e.g., `## Page 1`, `## Page 2`).

3. **Bilingual Presentation (中英对照)**
   - Every single page must present the content in a bilingual format.
   - Use a simple Markdown table format for the output:
     ```markdown
     | Original Text (Source) | Translated Text (Target) |
     | :--- | :--- |
     | XYZ 智能穿戴设备说明书 | XYZ Smart Wearable Device User Manual |
     ```

## Core Translation Logic

1. **Terminology Priority (术语裁定)**
   - Always resolve terms in this order: **User Dictionary > Base Domain Knowledge > LLM Inference**.
   - Consistency is critical across the entire manual.

2. **Functional Priority (意合优先)**
   - Do not translate word-for-word if the source text is convoluted or "Chinglish-prone".
   - **Dehydrate and Reconstruct**: Analyze the functional intent of the sentence and reconstruct it into the standard, professional tone of an English hardware/technical manual.

## Exporting to Word (.docx)

After generating the complete Markdown file, always use the included script to convert it into a structured Word document. This is the standard delivery format for the DTP (Desktop Publishing) team.

**Usage:**
```bash
python scripts/export_docx.py <input_markdown_file> <output_docx_file>
```

## Example Triggers & Workflows
- "请把这份 PDF 硬件说明书翻译成英文，严格按页生成中英对照表。"
- "提取当前页面图片里的所有技术参数和警告语，按照意合逻辑翻译，不要漏掉底部的 footnote。"
- "翻译完了，请调用 export 脚本帮我导出成带有表格边框的 Word 文档。"
- "Translate this user manual. Make sure to keep the exact pagination as ## Page N."