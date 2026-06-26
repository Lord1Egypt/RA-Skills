---
name: image-generator
description: Generate images via BigModel APIs and send them as chat images (e.g. Feishu). Invoke when user asks to create a single picture with specific style/size.
metadata: { "openclaw": { "emoji": "🖼️", "requires": { "env": ["ZHIPU_API_KEY"] }, "primaryEnv": "ZHIPU_API_KEY" } }
---

# CogView-3-Flash Skill

基于智谱/BigModel 的 `cogview-3-flash` 文生图接口，提供**快速单张图片生成**能力。

## Features

- 使用 `https://open.bigmodel.cn/api/paas/v4/images/generations` 接口
- 支持通过环境变量 `ZHIPU_API_KEY` 配置鉴权 Token
- 支持 `cogview-3-flash` 与 `glm-image` 两类模型
- 作为 OpenClaw Skill 使用：当用户在对话中请求生成图片时，由 Agent 调用本技能，自动执行 `scripts/generate.py`，根据提示词和尺寸生成图片并返回本地文件路径
- 简单参数：提示词、尺寸、水印开关

## Setup

1. 从对应平台控制台获取 API Key/Token
2. 在终端中设置环境变量：

```bash
export ZHIPU_API_KEY="你的 API Key"
```

或在工具配置中以同名变量注入。

## Models & Sizes

在脚本中通过 `--model` 选择模型：

- `cogview`：对应 `cogview-3-flash`（默认）
- `glm`：对应 `glm-image`

各模型推荐尺寸与限制：

- `glm-image` 推荐枚举值：`1280x1280`(默认), `1568x1056`, `1056x1568`, `1472x1088`, `1088x1472`, `1728x960`, `960x1728`  
  自定义尺寸: 长宽推荐在 `1024px-2048px` 范围内, 最大像素数不超过 `2^22`，长宽需为 `32` 的整数倍。
- 其它模型（如 `cogview-3-flash`）推荐枚举值：`1024x1024`(默认), `768x1344`, `864x1152`, `1344x768`, `1152x864`, `1440x720`, `720x1440`  
  自定义尺寸: 长宽需在 `512px-2048px` 范围内, 最大像素数不超过 `2^21`，长宽需为 `16` 的整数倍。

## Usage

### 命令行生成图片

```bash
python scripts/generate.py \
  "两只可爱的小猫咪，坐在阳光明媚的窗台上，背景是蓝天白云。" \
  --model cogview \
  --size 1024x1024 \
  --no-watermark \
  --output cats.png
```

### 参数说明

- `prompt`：必填，中文或英文提示词
- `--model`：模型选择，`cogview`(默认)/`glm`
- `--size`：图片尺寸，不传则使用所选模型默认尺寸
- `--watermark`：开启水印（默认开启）
- `--no-watermark`：关闭水印
- `--output` / `-o`：指定输出文件名，默认自动生成

## API 行为说明

- 接口返回 JSON，格式类似：

```json
{
  "created": 1773146620,
  "data": [
    { "url": "https://.../image.png" }
  ],
  "id": "20260310204340ad2bd838dcb64c7f",
  "request_id": "20260310204340ad2bd838dcb64c7f"
}
```

- 本 Skill 会自动解析 `data[0].url`，下载图片并保存到本地。

## 在 Feishu 中的使用（给 Agent 的操作指引）

当用户在 Feishu 对话中请求你生成图片时，请按下面步骤操作：

1. 使用系统运行工具，在 `{baseDir}` 目录下执行命令，根据用户的提示词和期望尺寸构造参数，例如：

   - `python {baseDir}/scripts/generate.py "<用户提示词>" --model cogview --size "<宽x高>" --no-watermark --output "/root/.openclaw/workspace/images/cogview-{时间戳}.png"`

2. 从脚本标准输出中找到形如 `✅ 图片已保存: /path/to/image.png` 的一行，并解析出其中的本地图片路径。
3. 使用 Feishu 的发送图片能力，将该图片文件直接作为图片消息发送到当前会话，而不是只把本地路径文本返回给用户。
4. 在文字回复中简单说明图片信息（模型、尺寸、提示词等），同时附上生成的图片。

## 示例

```bash
# 使用 cogview-3-flash，默认尺寸
python scripts/generate.py "一幅赛博朋克城市夜景，霓虹灯与雨夜" -o cyberpunk.png

# 使用 glm-image，自定义尺寸 + 关闭水印
python scripts/generate.py \
  "可爱风格的猫咪插画" \
  --model glm \
  --size 1280x1280 \
  --no-watermark
```
