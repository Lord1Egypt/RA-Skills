# Webhook 消息体参考

请求：`POST` 到 webhook URL，请求头 `Content-Type: application/json`。

---

## 文本（text）

`msgtype` = `text`，`text.content` 必填。

```json
{
  "msgtype": "text",
  "text": {
    "content": "每日数据监控报告：\n请相关同事注意"
  }
}
```

---

## Markdown（markdown）

`msgtype` = `markdown`，`markdown.text` 必填。支持标题、引用、加粗、颜色、斜体、删除线、链接、列表、图片；换行 `\n\n` 或 `双空格+\n`。

```json
{
  "msgtype": "markdown",
  "markdown": {
    "text": "## 监控报警\n\n报警内容：网关入口\n\n> 备注：严重程度中等"
  }
}
```

---

## curl 示例

```bash
# 替换 WEBHOOK_URL 为实际地址
curl -X POST "$WEBHOOK_SEND_URL" \
  -H "Content-Type: application/json" \
  -d '{"msgtype":"text","text":{"content":"Hello"}}'
```
