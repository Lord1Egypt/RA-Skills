# PDF 提取与多后端 triage

中文简历 PDF 上下文：

- 单一后端容易把页边跟踪串、竖排装饰字、隐藏文本层一起抽出。
- `pdfplumber` / `pdfminer.six` / `fitz`（PyMuPDF）对同一份 PDF 表现差异明显。
- 先做"多后端提取 → 清洗 → 打分 → 选最优文本"，比人工盯原始噪声稳定得多。

## 依赖

任一即可，越多越好：

```bash
# 推荐三套都装上，脚本会自动选最优
python3 -m pip install --user pymupdf pdfplumber pdfminer.six
```

> macOS 备选：`textutil -convert txt -stdout xxx.pdf` 只对文字型 PDF 有效，图片型 PDF 会报 encoding 错误，仍需 OCR。

## 推荐命令

单份 PDF：

```bash
python3 scripts/resume_pdf_extract.py /path/to/resume.pdf --output-dir /tmp/resume_extract_one
```

批量 PDF / 一个目录：

```bash
python3 scripts/resume_pdf_extract.py /path/to/resume_dir --output-dir /tmp/resume_extract_batch
```

脚本会：

1. 分别尝试可用后端（`fitz` / `pdfplumber` / `pdfminer.six`）。
2. 对每个结果做 Unicode 归一化、空白折叠、跟踪串 / 碎片行清洗。
3. 计算 `score / chars / lines / keyword_hits / quality`。
4. 选择分数最高的文本作为正式筛选输入。
5. 输出：
   - `summary.json`
   - 每份 PDF 对应的最佳 `.txt`
   - stdout Markdown 表格（可直接粘回会话）

## 文本质量分层

| 等级 | 判定 |
| --- | --- |
| `high` | `chars >= 2600` 且 `lines >= 55` 且 `score >= 65` |
| `medium` | `chars >= 1600` 且 `lines >= 35` 且 `score >= 35` |
| `low` | 低于上述阈值，标记"待补核" |

## 常见陷阱

- **下载到 JSON 不是 PDF**：批量下载后检查文件大小，若所有文件都是几百 bytes 大概率是错误响应体。
- **`.doc` 旧格式**：macOS 上没有 antiword/catdoc 时难以提取，建议要求候选人发 PDF 或 `.docx`。
- **加密 / 图片型 PDF**：所有文本后端都会返回空或乱码，需要 OCR；当前脚本会把这种情况标记为 `low` 并提示原因。
- **简历模板花哨**：极简模板、双列 / 三列模板、带装饰侧边栏的模板，往往要换后端才能正确还原阅读顺序。

## 与简历筛选流程的衔接

- 提取完成后**不要**把 backend/score/chars/lines 表写进正式筛选报告，只放进内部工作材料。
- 文本质量 `low` 的候选人单独列"待补核"名单，**不阻塞**其他候选人交付。
- 提取产物建议落到独立临时目录，避免与历史附件混淆。
