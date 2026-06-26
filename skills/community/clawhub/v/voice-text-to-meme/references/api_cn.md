> 若运行环境对 /mnt 只读，请不要把输出目录设到 /mnt。默认会写到当前目录下的 meme_outputs；必要时可用 --output ./meme.jpg 或设置 MEME_OUTPUT_DIR=./meme_outputs。

# 图片模型接入说明（中文）

## 默认模型
- 图片模型：`doubao-seedream-4-5-251128`
- 默认基地址：`https://models.audiozen.cn/v1`

## 默认调用方式
脚本按你提供的 OpenAI SDK 兼容方式调用：

```python
from openai import OpenAI

client = OpenAI(
    api_key="你的 token",
    base_url="https://models.audiozen.cn/v1"
)

images_response = client.images.generate(
    model="doubao-seedream-4-5-251128",
    prompt="...",
    size="2K",
    output_format="jpeg",
    response_format="url",
)
```

需要环境变量：
- `MEME_MODEL_API_KEY`
- `MEME_MODEL_BASE_URL`（可选，默认 `https://models.audiozen.cn/v1`）
- `MEME_MODEL_NAME`（可选，默认 `doubao-seedream-4-5-251128`）
- `MEME_MODEL_OUTPUT_FORMAT`（可选，默认 `jpeg`）
- `MEME_MODEL_RESPONSE_FORMAT`（可选，默认 `url`）

## 重要限制
该模型当前按你的接入方式，默认只按 **JPEG/JPG** 输出处理。

因此脚本已做这些调整：
- 默认输出格式固定按 `jpeg`
- 保存文件默认使用 `.jpg`
- 即使用户误写成 `jepg`，脚本也会自动纠正为 `jpeg`

## 表情包成品策略
“表情包格式”在这里指 **内容与排版风格像聊天表情包**，不要求特殊容器格式。

也就是说：
- 最终文件格式是 `.jpg`
- 但提示词、文案和构图会强制往“聊天表情包 / 梗图 / 贴纸感”靠

## 两种输出模式
### 1. direct-text
模型直接生成带字的 JPEG 表情包。

适合：
- 文案较短
- 想直接发送
- 不想自己后处理字幕

### 2. template
模型生成无字 JPEG 图，并输出字幕模板 JSON。

适合：
- 需要客户端统一叠字
- 文案较长
- 想自己控制字体和排版

## 推荐提示词结构
脚本会自动构造包含以下信息的图片提示词：
- 主要情绪
- 人物表情与动作
- 单主体 / 干净背景
- 聊天表情包或 meme 风格
- 是否带字
- 字幕长度与排版约束

## 兼容性说明
如果你后续接口字段发生变化，优先修改：
- `scripts/generate_meme.py` 中的 `_call_image_api`
- `scripts/generate_meme.py` 中的 `_extract_image_bytes`
