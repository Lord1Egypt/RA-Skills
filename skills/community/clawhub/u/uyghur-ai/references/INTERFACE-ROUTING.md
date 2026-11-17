# 接口路由

所有路径都基于 `/api/v1/uyghur-ai`。

| 用户意图 | 方法与路径 | 说明 |
|---|---|---|
| 中文与维吾尔语严格互译 | `POST /translation` | JSON，语言代码为 `zh` 与 `ug` |
| DOCX 翻译 | `POST /word/translation` | multipart，提取文字后翻译 |
| PDF 翻译 | `POST /pdf/translation` | multipart，支持文字版、扫描 PDF 和混合型 PDF |
| 图片 OCR 翻译 | `POST /image/translation` | multipart，返回 OCR 原文和译文 |
| 维吾尔语问答、解释、改写或创作 | `POST /chat/completions` | OpenAI 风格消息数组 |

- 用户要求“翻译”且不需要解释时使用 `/translation`。
- 用户上传 `.docx` 或 `.pdf` 时使用对应文档接口；扫描 PDF 仍使用 `/pdf/translation`。
- 用户明确提供 JPG、JPEG、PNG 或 WebP 图片并要求识别/翻译时，使用 `/image/translation`。
- 用户要求问答、润色、总结、续写或创作时使用 `/chat/completions`。
- 维吾尔文通常使用阿拉伯字母；不要仅凭拉丁字母片段假定为维吾尔文。
- 不接受远程图片 URL，也不要把图片转换成 JSON 字段；图片只通过 multipart 的 `file` 上传。
