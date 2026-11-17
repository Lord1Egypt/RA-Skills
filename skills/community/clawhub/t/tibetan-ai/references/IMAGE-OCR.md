# 图片 OCR 翻译

由阿里云百炼 Qwen3.8-Max 先识别图片中的藏文或中文，再对识别原文执行翻译。

接口：`POST /api/v1/tibetan-ai/image/translation`

请求必须是 `multipart/form-data`：

| 字段 | 约束 |
|---|---|
| `file` | 必填；JPEG（`.jpg`/`.jpeg`）、PNG 或 WebP；最大 10 MB；单次一张；不接受远程 URL |
| `from` | 必填，`zh` 或 `bo` |
| `to` | 必填，`zh` 或 `bo`，不能与 `from` 相同 |

图片必须能真实解码且扩展名、MIME 与签名一致，总像素不超过 16,000,000。SVG、GIF、TIFF、
HEIC、伪造扩展名和多图请求会被拒绝。

首次成功响应中，`srcText`（`data.srcText`）是 OCR 原文，`tgtText`（`data.tgtText`）是译文，
`pages`（`data.pages`）为页码与
识别文字（单图页码为 1）；`usage` 汇总 OCR 与翻译两阶段的输入、输出 token，并只结算一次。

`Idempotency-Key` 是必填的非空请求头；每次新图片使用唯一值，网络重试同一逻辑请求时复用原值。为保护隐私，成功
幂等重放只返回 `replayed=true`、`content_retained=false` 的计费摘要，不会保留 OCR 原文、
译文或页内容；图片与 PDF 是内容隐私例外，幂等记录不持久化任何 OCR/翻译/页面轮次内容，
因此调用方应在首次响应时保存用户需要的结果。

只在用户明确提供并同意处理时上传文件。绝不把图片字节、Base64 或 Data URL 放入 JSON、
日志或对话正文，也不要转存为公网 URL。

稳定错误码：

- `image_validation_failed`：格式、大小、签名、尺寸或像素不合法；修正文件后用新幂等键提交。
- `invalid_idempotency_key`：缺少或传入空白 `Idempotency-Key`；生成新键后再提交。
- `image_ocr_failed`：OCR 响应结构无法解析；有限退避并复用原幂等键。
- `empty_ocr_content`：没有识别到可翻译文字；请换清晰图片，不盲目重试。
- `upstream_unavailable`：上游超时或不可用；有限退避并复用原幂等键。
- `insufficient_balance`：余额不足；充值后再继续。
- `document_ocr_page_limit_exceeded`：仅适用于 PDF OCR 页超过上限，应拆分 PDF。
