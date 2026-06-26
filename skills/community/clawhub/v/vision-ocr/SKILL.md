---
name: vision-ocr
description: 用于识别图片和 PDF 文档，调用你已配置的 OCR 与多模态服务输出 Markdown 结果，并可按需发送到飞书。适合截图、扫描件、表格、票据和技术文档。
---

# vision-ocr

vision-ocr 是一个用于 OpenClaw 的文档识别技能，支持图片和 PDF 输入，输出结构化 Markdown 结果，并在机器人会话中优先发送到当前飞书会话。

## 适用场景

- 文档截图
- 扫描件
- 表格和票据
- 技术文档
- 多页 PDF
- 手写便条和手写批注

## 核心能力

- 文档识别：图片默认按文档流程处理。
- PDF 处理：支持逐页识别与基础信息查看。
- Markdown 输出：尽量保留原始文档结构，复杂表格允许混合 HTML 表格。
- 多模态整合：OCR 有效时结合原图输出最终 Markdown。
- 手写优化：手写文档、手写便条和手写批注会自动启用手写优先识别策略。
- 飞书发送：默认关闭；显式开启后可发送到当前会话或指定对象，无会话上下文时保留本地结果。

## 触发方式

```text
识别图片 /path/to/image.jpg
识别 PDF /path/to/file.pdf --pdf-option=ocr_full
OCR 这个截图
```

## 🚀 飞书集成场景：自动识别 + 按需发送

**目标：** 在飞书/集成场景下实现「发送图片/PDF → 自动识别 → 按需发送结果到当前会话」

### 正确操作（⚠️ 必须遵守）

| 场景 | 调用方式 | 能否自动发送 |
|------|---------|-------------|
| ✅ **飞书集成** | 直接在主会话调用 `vision-ocr.run(context)` 并显式开启发送 | ✅ 可以 |
| ❌ 子会话 | 通过子会话调用 `vision-ocr.run(context)` | ❌ 无法发送 |
| ❌ 命令行 | `node index.js --image ...` | ❌ 无法发送 |

### 为什么子会话不行？

```
主会话（飞书集成）
    ↓
子会话（隔离环境）
    ↓
vision-ocr 尝试获取会话上下文
    ↓
❌ 当前上下文未传入 session.chatId / session.openId
    ↓
❌ 无法确定发送目标，跳过自动发送
```

**解决方案：** 直接在主会话中调用 `vision-ocr.run(context)`，确保能获取到 `chatId` 和 `openId` 或 `senderId`。

### 代码示例

```javascript
// ✅ 正确：在主会话中直接调用
const visionOcr = require('/home/node/.openclaw/workspace/skills/vision-ocr');

await visionOcr.run({
  session: {
    chatId: 'chat_xxx',
    openId: 'ou_xxx',
    isGroup: false
  },
  message: {
    text: '识别图片 /path/to/image.jpg'
  },
  replyText: async (msg) => {
    // 显式开启发送后，可发送到当前飞书会话
    console.log(msg);
  }
});

// ❌ 错误：通过子会话调用会丢失当前会话上下文
```

### 关键检查清单

在使用 vision-ocr 实现自动发送前，确认：

- [ ] **在主会话中直接调用**（不是子会话）
- [ ] **通过 `run(context)` 传递会话上下文**（不是命令行）
- [ ] **context 中包含 `session.chatId` 和 `session.openId` / `session.senderId`**

---

## 基本配置

推荐在技能目录 `config.json` 或当前进程环境变量中提供以下内容：

```json
{
  "ocr": {
    "imageocr": {
      "token": "你的 ImageOCR Token",
      "endpoint": "你的 ImageOCR 端点"
    },
    "multimodal": {
      "baseUrl": "你的多模态 API 地址",
      "token": "你的多模态 Token",
      "model": "你的模型名称"
    }
  },
  "autoSendToFeishu": false
}
```

如果技能运行在 OpenClaw 会话中，并且你显式开启了飞书发送，同时运行时提供了当前群聊或私聊上下文，则发送飞书文件时会优先发到当前会话。若要发送给其他对象，可直接在对话中明确指定，例如：发给 open_id:ou_xxx 或 发给 chat:oc_xxx。

CLI 模式下，只有显式开启 `--resolve-openclaw-session` 或设置 `VISION_RESOLVE_OPENCLAW_SESSION=true` 时，技能才会尝试从 `OPENCLAW_CHAT_ID`、`OPENCLAW_SENDER_ID`、`OPENCLAW_OPEN_ID` 等环境变量，以及 `~/.openclaw/runtime.json` 中恢复当前会话信息。机器人模式默认只信任 `context.session` 或消息中显式指定的接收者。

`node index.js --update-config` 只会把当前 shell 中的 `VISION_*` 环境变量写入技能目录 `config.json`，不会读取或改写 OpenClaw 全局配置。

如果 OpenClaw 需要发送到当前会话，必须调用导出的机器人入口 `run(context)` 并显式开启发送，而不是只执行命令行。例如：

```js
const visionOcr = require('/home/node/.openclaw/workspace/skills/vision-ocr');

await visionOcr.run({
  session: {
    chatId: 'chat_xxx',
    openId: 'ou_xxx',
    isGroup: false
  },
  message: {
    text: '识别图片 /path/to/image.jpg'
  },
  replyText: async (msg) => {
    console.log(msg);
  }
});
```

如果仅执行 `node index.js --image ...`，识别会成功，但不会有当前会话信息，因此不会自动发送到当前飞书会话。

## 常用命令

```bash
node index.js --image /path/to/image.jpg --confirm=true
node index.js --image /path/to/file.pdf --pdf-option=ocr_full --confirm=true
node index.js --image /path/to/image.jpg --confirm=true --no-send-to-feishu
node index.js --image /path/to/image.jpg --confirm=true --send-to-feishu --resolve-openclaw-session
```

## 行为说明

- 图片默认先执行 OCR。
- OCR 有效时，会将 OCR Markdown 和原图一起交给大模型生成最终 Markdown。
- OCR 无效时，会自动切换为图片描述模式。
- 显式开启飞书发送时，优先发送到当前会话；没有会话上下文时不会自动发送。
- 只有显式开启远程输入时，技能才会下载远程附件 URL 或 token 模板资源。
- 关闭飞书发送后，结果文件会保留在临时目录，便于手动处理。

## 依赖

- Node.js 18+
- Python 3.8+
- PyMuPDF
- feishu-send-files 技能

## 隐私提示

- 默认不会发送识别结果到飞书；只有显式开启后才会发送。
- 处理敏感文档时，建议使用 --no-send-to-feishu。
- 仓库和发布包中不应包含真实凭据或本地配置文件。

## 版本

当前版本：1.1.2

## 修订说明

- 1.1.2：安全增强，远程附件下载 SSRF 过滤（禁止 localhost/私有段），新增下载超时与最大大小；PDF helper 调用加 `maxBuffer` 与 `PYTHON_PATH` 支持。
- 1.1.1：新增多模态大图自动预处理与 base64 清理，固定 PDF helper 文件，远程附件下载与 CLI OpenClaw 会话恢复改为显式开启，并同步更新文档与打包内容。
