# 文档翻译

- DOCX：`POST /api/v1/uyghur-ai/word/translation`
- PDF：`POST /api/v1/uyghur-ai/pdf/translation`

multipart/form-data 字段：

| 字段 | 约束 |
|---|---|
| `file` | 必填；DOCX 或 PDF；最大 5 MB |
| `from` | 必填，`zh` 或 `ug` |
| `to` | 必填，`zh` 或 `ug` |
| `mode` | 可选，`all_text`（默认）或 `uyghur_only` |

`all_text` 翻译提取出的全部文字；`uyghur_only` 只保留并处理维吾尔文相关文本。接口返回
提取文本的翻译结果，不生成保留原排版的新文件。

PDF 支持文字版、扫描 PDF 和混合型 PDF：逐页优先使用文字层，缺少有效文字层的页面再执行
OCR，最后按页码顺序合并并翻译。最多 50 页，其中需要 OCR 的页面最多 10 页；超过上限返回
HTTP 422 `document_ocr_page_limit_exceeded`，应请用户拆分文件。损坏、加密或无法解析的文件返回
`document_extraction_failed`，没有可翻译文字返回 `empty_ocr_content`。完全空白页不会渲染或计入 OCR 页数。

纯文字 PDF 只调用一次翻译，返回普通翻译响应结构：包含 `data.srcText` 与 `data.tgtText`，
不包含 `pages`，usage 也只计算翻译调用。

扫描或混合型 PDF 才执行 OCR 与翻译两阶段。此时响应包含 `source=pdf_ocr` 和 `data.pages`，
OCR 与翻译两次调用的输入、输出 token 合并到一次 usage 和一次账单中。PDF 翻译必须携带非空
`Idempotency-Key`；每次新上传都使用唯一值，同一文件重试才复用原值。成功幂等重放只返回
`replayed=true`、`content_retained=false` 的摘要，不会保留 OCR 原文、译文或页内容。
