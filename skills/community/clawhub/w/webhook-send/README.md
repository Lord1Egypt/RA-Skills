# Webhook 发送消息

向指定 webhook 地址 **POST** 发送**文本**或 **Markdown** 消息。URL 从环境变量 `WEBHOOK_SEND_URL` 读取。

---

## 限制

- **频率**：≤ 20 条/分钟  
- **长度**：单条 ≤ 5000 字符  
- **请求**：`POST`，`Content-Type: application/json`

---

## 1. 文本（text）

| 参数 | 必填 | 说明 |
|------|------|------|
| `msgtype` | 是 | 固定 `text` |
| `text.content` | 是 | 消息内容 |

**示例**

```json
{
  "msgtype": "text",
  "text": { "content": "每日数据报告：\n请相关同事注意" }
}
```

---

## 2. Markdown（markdown）

| 参数 | 必填 | 说明 |
|------|------|------|
| `msgtype` | 是 | 固定 `markdown` |
| `markdown.text` | 是 | Markdown 内容 |

**支持的语法**：标题(#～######)、引用(>)、**加粗**、*斜体*、~~删除线~~、`<font color='#FF0000'>颜色</font>`、链接、有序/无序列表、图片。换行：`\n\n` 或 `双空格+\n`。

**示例**

```json
{
  "msgtype": "markdown",
  "markdown": {
    "text": "## 监控报警\n\n报警内容：网关入口\n\n> 备注：严重程度中等"
  }
}
```

更多请求体示例见 [reference.md](reference.md)。
