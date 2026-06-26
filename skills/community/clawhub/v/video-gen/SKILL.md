---
name: video-gen
description: AI视频生成与编辑，使用火山引擎 Doubao Seedance 模型。支持文生视频、图生视频、有声视频。当用户要求生成视频、制作视频、文生视频、图生视频时使用此 skill。
---

# AI 视频生成

通过火山引擎 Doubao Seedance API 生成视频。

## 环境变量

脚本通过以下环境变量获取 API 配置：

- `VIDEO_GEN_API_KEY` — 火山引擎 API Key
- `VIDEO_GEN_BASE_URL` — API 基础地址（默认：https://ark.cn-beijing.volces.com/api/v3）

## 支持的生成模式

| 模式 | 说明 | 参数 |
|------|------|------|
| `text_to_video` | 文生视频 | prompt |
| `image_to_video` | 图+文生视频（URL）| prompt + --first-frame URL |
| `image_to_video_base64` | 图生视频（Base64）| prompt + --first-frame 路径/base64 |
| `audio_video_first_frame` | 有声视频-首帧 | prompt + --first-frame + --audio |
| `audio_video_first_last_frame` | 有声视频-首尾帧 | prompt + --first-frame + --last-frame + --audio |
| `seedance_lite_reference` | Seedance-Lite 参考图 | prompt + --reference-image |

## 可用模型

- `doubao-seedance-1.5` — 完整版（默认）
- `seedance-lite` — 轻量版

## 使用方法

### 文生视频

```bash
export VIDEO_GEN_API_KEY="your-api-key"

python3 scripts/generate_video.py "一只可爱的小猫在草地上奔跑，阳光明媚，慢动作" \
  --mode text_to_video \
  --output cat_running.mp4
```

### 图生视频

```bash
python3 scripts/generate_video.py "让图片中的人物转头微笑" \
  --mode image_to_video \
  --first-frame "https://example.com/image.jpg" \
  --output person_smile.mp4
```

### 图生视频（Base64）

```bash
python3 scripts/generate_video.py "让图片动起来" \
  --mode image_to_video_base64 \
  --first-frame ./input_image.png \
  --output animated.mp4
```

### 有声视频（首帧）

```bash
python3 scripts/generate_video.py "人物开口说话，声音洪亮" \
  --mode audio_video_first_frame \
  --first-frame ./portrait.jpg \
  --audio \
  --output talking.mp4
```

### 有声视频（首尾帧）

```bash
python3 scripts/generate_video.py "人物从左转头到右" \
  --mode audio_video_first_last_frame \
  --first-frame ./left.jpg \
  --last-frame ./right.jpg \
  --audio \
  --output turn_head.mp4
```

### Seedance-Lite 参考图

```bash
python3 scripts/generate_video.py "参考图片风格生成视频" \
  --mode seedance_lite_reference \
  --reference-image ./style_ref.jpg \
  --output styled_video.mp4
```

## 工作流程

1. **理解需求**：分析用户的视频需求，确定生成模式
2. **选择模式**：文生视频、图生视频、有声视频等
3. **优化提示词**：将用户描述扩展为详细的视频描述
4. **执行脚本**：调用 `scripts/generate_video.py` 生成视频
5. **等待完成**：视频生成通常需要几分钟
6. **上传视频**：上传到飞书获取 file_key
7. **发送视频**：使用 `message` 工具发送视频

## 飞书视频上传

```python
import requests

# 获取 token（使用飞书 app_id 和 app_secret）
resp = requests.post(
    "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
    json={"app_id": "YOUR_APP_ID", "app_secret": "YOUR_APP_SECRET"}
)
token = resp.json()["tenant_access_token"]

# 上传视频
with open("video.mp4", "rb") as f:
    resp = requests.post(
        "https://open.feishu.cn/open-apis/im/v1/files",
        headers={"Authorization": f"Bearer {token}"},
        files={"file": ("video.mp4", f, "video/mp4")},
        data={"file_type": "mp4"}
    )
file_key = resp.json()["data"]["file_key"]

# 发送视频
# 使用 message 工具: {"file_key": "<file_key>"}
```

## 提示词技巧

- **描述动作**：清晰描述主体运动、镜头运动
- **时间感**：快/慢动作、延时、瞬间
- **氛围感**：光线、天气、情绪
- **镜头语言**：推/拉/摇/移、特写/远景

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| --mode | 生成模式 | text_to_video |
| --model | 模型名称 | doubao-seedance-1.5 |
| --first-frame | 首帧图片 | - |
| --last-frame | 尾帧图片 | - |
| --reference-image | 参考图片 | - |
| --audio | 启用音频 | False |
| --output | 输出路径 | 自动生成 |
| --no-wait | 不等待完成 | False |
