# vision - 图片全能识别

## 简介
本技能能够在 **聊天、文档、以及本地文件夹** 中对图片进行 **文字、物体、场景** 三类识别。文字识别支持中英文，若检测到英文会自动翻译为中文后写回。识别结果直接写回原始文档/聊天，或在本地生成同名 `.txt`。

## 使用方式
- **聊天/文档**：在 Feishu 消息或文档中发送图片，系统会自动调用本技能并把识别结果写回。
- **本地文件夹**：运行 `openclaw skill vision /path/to/image.jpg`，结果会生成 `image.txt`。
- **命令行**：`openclaw vision recognize /path/to/img.png`

## 参数
| 参数 | 必须 | 说明 |
|------|------|------|
| \`image\` | ✅ | 图片文件本地路径或 URL |
| \`source\` | ❌ | \`feishu-msg\` / \`feishu-doc\` / \`local\`（默认自动判断） |

## 配置
见 `config.json`，可自行修改模型路径、翻译 API Key 等。

## 注意
- 本技能完全本地运行，除翻译外不依赖外部云服务。  
- 推荐在 macOS M 系列上使用 `brew install tesseract`，并将 `tesseract` 可执行文件加入 \`$PATH\`。
