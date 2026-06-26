---
name: volc-vision
description: 使用火山引擎 ARK API 做图片理解、图片描述、视觉问答与图像分析。适用于用户发来图片并询问“这是什么”“图里有什么”“帮我看下这张图”“描述一下图片内容”“识别图片中的信息”等场景，也适用于需要对本地图片、图片 URL 或 base64 图片做理解和问答时。
metadata: { "openclaw": { "emoji": "🖼️", "requires": { "bins": ["node"], "env": ["ARK_API_KEY"] }, "primaryEnv": "ARK_API_KEY" } }
---

# volc-vision

火山引擎 ARK API 图像理解服务。

## 适用场景

- 用户发送图片并询问关于图片的问题
- 需要理解、分析、描述图片时
- 用户说“看看这张图”“描述一下”“这图是什么”“图里有什么”“帮我分析图片内容”
- 需要对本地图片路径、图片 URL 或 base64 图片做视觉问答

## 输入参数

| 参数 | 必填 | 说明 |
|------|------|------|
| image | 是 | 图片路径、URL 或 base64 |
| prompt | 否 | 要问的问题，默认 `描述这张图片` |

## 使用方式

```bash
# 命令行调用
node skills/volc-vision/index.js <图片路径> "<问题>"

# 示例
node skills/volc-vision/index.js /path/to/image.jpg "描述这张图片"
node skills/volc-vision/index.js https://example.com/image.jpg "这图里有什么"
```

## 模型优先级（按强弱排序）

Vision 系列优先，其他模型按能力依次降序：

1. `doubao-seed-1-6-vision-250815` 🌟 首选
2. `doubao-1-5-vision-pro-32k-250115` 🌟
3. `doubao-seed-2-0-pro-260215`
4. `doubao-seed-1-8-251228`
5. `doubao-seed-2-0-lite-260215`
6. `doubao-seed-2-0-mini-260215`

**自动切换**：如果不指定模型，会按列表顺序依次尝试可用模型，直到成功。

## 环境变量

```bash
# 必需：ARK API Key
export ARK_API_KEY="your_api_key"

# 可选：指定模型
export VISION_MODEL="doubao-seed-1-6-vision-250815"
```

## 指定模型

```bash
ARK_API_KEY=your_api_key VISION_MODEL=doubao-seed-1-6-vision-250815 node skills/volc-vision/index.js <图片> "<问题>"
```

## 返回

- 图片描述
- 视觉问答结果
- 图像分析文本结果

## 调用示例

```text
用户：看看这张图
-> agent 调用: node skills/volc-vision/index.js /root/.openclaw/media/inbound/xxx.jpg "描述这张图片"
-> 返回描述结果
```

## 注意事项

- 使用前必须设置 `ARK_API_KEY`
- 如果用户只是要生成图片而不是理解图片，不要误用本技能
- 若已有明确视觉问题，优先把问题放进 `prompt`，不要只做泛泛描述
