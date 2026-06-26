# vision-ocr

vision-ocr 是一个面向 OpenClaw 的文档识别技能，支持图片和 PDF 的 OCR 提取、多模态整合，以及 Markdown 结果输出。

它适合处理截图、扫描件、表格、技术文档、票据和常见 PDF 文档。识别完成后默认保留在本地临时目录；如需发送到飞书，请显式开启。

当前版本：1.1.2

## 1.1.2 修订说明

- 安全强化：远程附件下载引入 SSRF 防护，禁止 localhost/私有网段 URL，新增 15s 超时与 50MB 限制。
- 安全强化：PDF helper 调用改用可配置 `PYTHON_PATH` 且上限 `maxBuffer` 20MB。
- 更新运行时读取策略：`VISION_RESOLVE_OPENCLAW_SESSION` 仍需显式开启，避免默认泄露会话信息。

## 1.1.1 修订说明

- 多模态链路新增大图自动预处理，超大图片会先缩放再发送，降低服务端处理失败概率。
- 发送图片前统一清理 base64 中的换行符，并按真实图片 MIME 类型构造 data URL，提升多模态兼容性。
- PDF 处理改为调用固定 `pdf-helper.py`，不再运行时动态生成 Python 脚本。
- 远程附件下载默认关闭，需显式开启 `--allow-remote-input` 或 `VISION_ALLOW_REMOTE_INPUT=true`。
- CLI 会话接收者恢复默认关闭，需显式开启 `--resolve-openclaw-session` 或 `VISION_RESOLVE_OPENCLAW_SESSION=true`。
- 文档与打包内容同步更新，发布包现包含固定 helper 文件并反映最新隐私/安全默认值。

## 核心能力

- 图片识别：支持常见图片格式，默认按文档识别流程处理。
- PDF 识别：支持逐页处理，适合长文档和多页材料。
- Markdown 输出：尽量保留标题、列表、表格和代码块结构。
- 多模态整合：OCR 有效时，结合原图输出更完整的最终 Markdown。
- 手写优化：检测到手写文档、手写便条或手写批注相关指令时，会自动启用手写优先识别策略。
- 飞书发送：默认关闭，可显式开启发送到当前会话或其他对象。

## 安装要求

必需环境：

- Node.js 18+
- Python 3.8+
- PyMuPDF

安装 PyMuPDF：

```bash
pip install pymupdf
```

如需发送到飞书，建议同时安装 `feishu-send-files` 技能。

## 快速开始

1. 安装技能并进入目录。
2. 准备 OCR 和多模态配置。
3. 运行命令或直接在 OpenClaw 中调用。

从环境变量写入本技能本地配置：

```bash
cd ~/.openclaw/workspace/skills/vision-ocr
node index.js --update-config
```

图片识别示例：

```bash
node index.js --image /path/to/image.jpg --confirm=true
```

PDF 识别示例：

```bash
node index.js --image /path/to/file.pdf --pdf-option=ocr_full --confirm=true
```

关闭飞书发送：

```bash
node index.js --image /path/to/image.jpg --confirm=true --no-send-to-feishu
```

仅返回 OCR 原始结果：

```bash
node index.js --image /path/to/image.jpg --confirm=true --ocr-only
node index.js --image /path/to/file.pdf --pdf-option=ocr_full --confirm=true --ocr-only
```

## 配置

支持以下配置来源，优先级从高到低：

1. 环境变量
2. 技能目录配置 `./config.json`

推荐配置示例：

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

未显式配置 `autoSendToFeishu` 时，技能默认保留本地结果文件。只有显式设置 `autoSendToFeishu: true`、传入 `--send-to-feishu`，或在上层集成中明确开启发送时，才会尝试发送到飞书。

机器人模式下，如果 OpenClaw 提供当前会话上下文并且你显式开启发送，识别结果会优先发送到当前群聊或当前私聊。若要发送给其他对象，可直接在对话里明确指定，例如：`发给 open_id:ou_xxx` 或 `发给 chat:oc_xxx`。

CLI 模式下，只有显式开启 `--resolve-openclaw-session` 或设置 `VISION_RESOLVE_OPENCLAW_SESSION=true` 时，技能才会尝试从 `OPENCLAW_CHAT_ID`、`OPENCLAW_SENDER_ID`、`OPENCLAW_OPEN_ID` 等环境变量，以及 `~/.openclaw/runtime.json` 中恢复当前会话信息。机器人模式默认只信任 `context.session` 或消息中显式指定的接收者。

OpenClaw 集成时，如需发送到当前会话，必须以机器人模式调用导出的 `run(context)` 并显式开启发送，不能只走命令行：

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

如果 OpenClaw 只执行 `node index.js --image ...` 这类命令行调用，技能仍可完成识别，但不会拿到 `context.session`，因此无法自动发送到当前飞书会话。

`node index.js --update-config` 只会读当前 shell 中的 `VISION_*` 环境变量，并写入技能目录下的 `config.json`。它不会读取或改写任何 OpenClaw 全局配置。

常用环境变量：

```bash
export VISION_IMAGEOCR_TOKEN="你的 Token"
export VISION_IMAGEOCR_ENDPOINT="你的端点"
export VISION_BASE_URL="你的多模态 API 地址"
export VISION_MULTIMODAL_TOKEN="你的多模态 Token"
export VISION_MODEL="你的模型名称"
export VISION_AUTO_SEND_TO_FEISHU="true"
export VISION_ALLOW_REMOTE_INPUT="false"
export VISION_RESOLVE_OPENCLAW_SESSION="false"
```

## 使用方式

OpenClaw 对话示例：

```text
识别图片 /path/to/image.jpg
识别 PDF /path/to/file.pdf --pdf-option=ocr_full
OCR 这个截图
识别图片 /path/to/image.jpg 只要OCR结果
直接发送一张图片附件，不额外写路径
在显式开启远程输入后发送一个可直接下载的远程图片 URL
```

常用参数：

| 参数 | 说明 |
| ---- | ---- |
| `--image` | 输入图片或 PDF 路径 |
| `--pdf-option` | PDF 处理方式 |
| `--prompt` | 自定义补充指令 |
| `--prompt-type` | 预设模板类型 |
| `--confirm` | 跳过交互确认 |
| `--progress` | 显示处理进度 |
| `--ocr-only` | 仅返回 OCR 原始结果，不做多模态整合 |
| `--send-to-feishu` | 显式开启发送到飞书 |
| `--no-send-to-feishu` | 显式关闭发送到飞书 |
| `--allow-remote-input` | 显式允许下载远程附件 URL 或 token 模板资源 |
| `--resolve-openclaw-session` | 显式允许从 `OPENCLAW_*` 或 `runtime.json` 恢复接收者 |
| `--to` | 显式指定接收者，例如 `open_id:ou_xxx` |

PDF 处理选项：

| 选项 | 说明 |
| ---- | ---- |
| `ocr_full` | 逐页识别全部内容 |
| `ocr_table` | 逐页提取表格内容 |
| `ocr_plain` | 逐页提取纯文字 |
| `save_images` | 将 PDF 保存为图片 |
| `info` | 查看 PDF 基本信息 |

## 结果与隐私

- 默认不会发送识别结果到飞书；只有显式开启后才会发送。
- 机器人模式下，如果上下文里带有附件本地路径，技能可以直接识别，不必强制把路径写进消息文本。
- 只有显式开启远程输入后，如果上下文里提供了可直接下载的远程附件 URL，或提供了 `file token + download URL 模板/前缀`，技能才会先下载到本地临时目录再识别。
- 当前已显式适配的本地字段包括：`path`、`filePath`、`file_path`、`localPath`、`local_path`、`tempFilePath`、`temp_file_path`、`downloadPath`、`savedPath`。
- 当前已显式适配的远程字段包括：`url`、`downloadUrl`、`download_url`、`previewUrl`、`fileUrl`、`imageUrl`、`resourceUrl`，以及 `file_token` / `fileToken` / `file_key` / `image_key` 配合 `attachmentDownloadUrlTemplate`、`downloadUrlTemplate`、`attachmentDownloadUrlPrefix` 等模板或前缀字段。
- 当前会优先扫描这些常见容器：`context.message`、`context.message.attachments`、`context.message.files`、`context.message.images`、`context.attachments`、`context.files`、`context.images`、`context.event.message`、`context.payload.message`、`context.extra.attachments`，以及 JSON 字符串形式的 `message.content`。
- 显式指定 `--ocr-only` 或在对话中说明“只要 OCR 结果”时，会直接返回 OCR 原始结果，便于排查识别质量。
- 对 PDF 启用 `--ocr-only` 时，会按页返回每页 OCR 原文，不再做多模态整合。
- 默认会先判断图片更像文档、代码截图、界面截图，还是自然照片/动物照片/人物照片，再自动决定走 OCR+多模态，还是直接多模态描述。
- 机器人回复会附带简短判定说明，便于查看是按文档链路、照片链路还是回退链路完成处理。
- 如果上游只给裸 `file token`，但没有下载模板、前缀或可用 URL，技能仍然无法自行下载该附件，需要 OpenClaw 集成层补充可下载地址或先落地到本地路径。
- 在 OpenClaw 机器人会话中，若显式开启发送，会优先发送到当前会话；没有当前会话上下文时不会自动发送。
- 如处理敏感文档，继续保持默认本地输出，或显式使用 `--no-send-to-feishu`。
- 发送关闭或发送失败时，结果会保留在临时目录 `/tmp/vision-ocr-<PID>/result.md`。
- 仓库和发布包中不应包含真实 `config.json`、Token 或 API Key。
- 技能会读取输入文件、技能目录 `config.json`、显式 `VISION_*` 环境变量；只有显式开启 OpenClaw 会话恢复后，才会在 CLI 发送场景下读取 `OPENCLAW_*` 环境变量或 `~/.openclaw/runtime.json` 以恢复接收者。
- 技能默认只会向你配置的 OCR、多模态服务发起网络请求；开启飞书发送时才会调用 `feishu-send-files`。

## 常见问题

### 未找到 imageocr 配置

请检查以下任一位置是否已配置：

1. `./config.json`
2. 环境变量 `VISION_IMAGEOCR_TOKEN` 与 `VISION_IMAGEOCR_ENDPOINT`

### 未自动发送到飞书

如果未显式开启飞书发送，或当前运行环境没有提供会话上下文，技能会保留结果文件而不自动发送。OpenClaw 集成时，如需发送到当前会话，请改为调用导出的 `run(context)` 并开启发送，或在对话中显式指定接收者，或手动发送生成的 Markdown 文件。

### PDF 转图片失败

通常是未安装 PyMuPDF：

```bash
pip install pymupdf
```

### 需要查看详细日志

```bash
DEBUG=1 node index.js --image /path/to/file.jpg --confirm=true
```

## 发布页

Clawhub 页面：<https://clawhub.ai/zhangxusong637/vision-ocr>
