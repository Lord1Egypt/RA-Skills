---
name: video-creator
description: 产品介绍视频自动生成技能。当用户需要生成产品介绍视频、宣传视频、演示视频时、复刻声音时触发。支持：(1) 声音合成——若用户明确指定"我的"声音，则复刻声音并用于下次合成；否则自动使用edge-tts合成语音（支持男声/女声选择）；(2) 基于用户提供的图片素材生成静态幻灯片视频（无需大模型生成视频）；(3) 自动生成对应语言的SRT字幕（软字幕/硬字幕/无字幕可选）并与音频同步。（4）复刻声音。（5）口播引导视频：当脚本首段以"口播："开头时，使用真人照片+TTS音频 并生成真人口播片段。适用场景：用户说"帮我生成产品视频"、"制作一个XX的介绍视频"、"用我的声音或男声或女声生成视频"、"把这些图片做成视频"、"生成一段口播视频"时，务必使用此技能。
---

# 产品介绍视频自动生成

将文案、图片素材自动合成为带字幕和配音的产品介绍视频，不依赖大模型生成视频，以控制成本。

## API Key

用户需要提供平台 API Key，用于鉴权。配置示例：
```json
{
  "api_key": "YOUR_API_KEY_HERE",
  "voice_id": "YOUR_VOICE_ID_HERE"
}
```
> ⚠️ **未配置 API Key 时**，不得执行检索，必须先提示用户：
> "config.json 中的 api_key 尚未配置。请前往 https://open.delilegal.com/personal/keys 创建 API Key，并填入技能目录下的 config.json 文件中。"

## 快速开始

1. 阅读 `references/dependencies.md` 了解环境依赖
2. 运行 `scripts/generate_video.py` 执行完整流程

---

## 输入规范

用户需要提供：

| 输入 | 说明 | 是否必须 |
|------|------|----------|
| 文案脚本 | 每段对应一张图片的旁白文本；首段可加"口播："前缀触发真人口播模式 | 必须 |
| 图片素材 | JPG/PNG，建议16:9或9:16比例 | 口播模式下仅非口播段需要 |
| 真人照片 | JPG/PNG，主持人正面照，用于口播视频 | 口播模式必须 |
| 口播质量 | high（高质量720P）或 standard（标准质量480P），统一使用 wan2.7-i2v 模型 | 可选（默认standard） |
| 口播提示词 | wan2.7 高质量模式下的 prompt，用于控制生成画面质感 | 可选（默认带美颜+高清提示词） |
| 声音偏好 | "我的"复刻声音 或 edge-tts（男声/女声） | 可选（默认edge-tts女声） |
| 配图风格 | `--image-style` 参数。例如："动漫"、"卡通"、"自然风景"、"赛博朋克"等 | 可选（默认专业严肃风格） |
| 字幕类型 | soft（软字幕）/ hard（硬字幕）/ none（无字幕） | 可选（默认soft） |
| 目标语言 | zh-CN / en-US / ja-JP 等 | 可选（默认自动检测） |
| 输出分辨率 | 默认1920×1080 | 可选 |

用户只提供了生成视频，但不包含文案脚本，需提示用户提供更多信息，脚本格式示例：
```   
生成视频，竖屏，男声，硬字幕：
口播：大家好，我是得理科技的我的。今天很高兴为大家介绍我们的新产品。
第1段：欢迎使用我们的产品，这是全球领先的解决方案。
第2段：我们的技术创新已获得超过200项专利认证。
第3段：现在就加入我们，开启智能化新时代。
```
## 参数收集

当用户请求生成视频但参数不明确时，系统**必须按以下优先级主动询问**，收集确认后再执行生成。

### 1. 声音选择

| 场景 | 询问内容 | 选项 |
|------|----------|------|
| 用户未提及声音 | "视频配音使用什么声音？" | ① 我的复刻声音；② edge-tts 默认女声；③ edge-tts 男声 |
| 用户提到"默认""自动" | 同上 | 同上 |
| 用户指定"我的" | 无需询问，直接使用 | — |
| 用户指定"男声"或"女声" | 无需询问，直接使用对应性别edge-tts | — |

### 2. 字幕选择（***关键参数，必须确认***）

| 场景 | 询问内容 | 选项 |
|------|----------|------|
| 用户未提及字幕 | **必须主动询问**："需要生成字幕吗？如果需要，要软字幕还是硬字幕？" | ① 软字幕：播放器内可开关；② 硬字幕：烧录进画面，始终显示；③ 无字幕 |
| 用户只说"要字幕" | 追问软/硬选择 | 同上 |
| 用户说"不要字幕" | 无需询问，使用 none | — |
| 用户明确指定 soft/hard | 无需询问，直接使用 | — |

### 3. 图片素材

| 场景 | 处理 |
|------|------|
| 用户未提供图片或没找到任何产品图片 | 基于段落文案自动使用 `wan2.7-image` 模型生成统一风格的图片。若无 `DASHSCOPE_API_KEY`，会自动降级使用 Python Pillow 生成包含专业法律风格（深蓝底+金字）的配图 |
| 图片数 ≠ 文案段落数且提供了图片 | 报错提示不匹配详情，要求用户调整 |

### 参数 → CLI 映射表

收集到的参数通过以下命令行参数传递给 `generate_video.py`：

| 用户选择 | 命令行参数 | 示例 |
|----------|-----------|------|
| 我的声音 | `--voice myvoice` | `--voice myvoice` |
| 自动复刻（公网音频） | `--clone-audio-url` | `--clone-audio-url https://yourAudioFileUrl` |
| 自动复刻（本地音频） | `--clone-audio-file` | `--clone-audio-file /path/to/voice.wav` |
| 生成配图风格 | `--image-style` | `--image-style 动漫` |
| edge-tts 女声 | `--voice edge_tts --edge-tts-gender female`（默认） | — |
| edge-tts 男声 | `--voice edge_tts --edge-tts-gender male` | `--edge-tts-gender male` |
| 真人口播照片 | `--portrait` | `--portrait /path/to/host.jpg` |
| 软字幕 | `--subtitle soft`（默认） | — |
| 硬字幕 | `--subtitle hard` | `--subtitle hard` |
| 无字幕 | `--subtitle none` | `--subtitle none` |

### 询问模板

当多个参数都不明确时，一次性询问（避免多次来回）：

> 在生成视频前，需要确认以下参数：
> 1. **声音**：使用"我的"复刻声音，还是 edge-tts 默认女声 / 男声？
> 2. **字幕**：需要生成字幕吗？软字幕（可开关）还是硬字幕（烧录进画面）？
> 3. **图片**：请提供图片素材，数量应与文案段落数一致（口播模式下首段无需图片）。
> 4. **口播**：若脚本第一段以"口播："开头，请提供主持人真人照片（JPG/PNG），否则任务无法继续。
---

## 工作流程

```
用户输入（文案 + 图片）
        │
        ▼
  ① 参数收集确认（声音 / 字幕 / 图片 / 口播照片）
        │
        ▼
  ② 解析文案脚本（按段落切分）
        │
        ├── 首段含"口播："前缀 → 验证 --portrait 照片存在，否则立即退出
        │
        ├── 检查图片素材，若未提供或没找到，则使用 wan2.7-image 依据每段内容自动生成统一风格的对应图片
        │
        ▼
  ③ 声音合成（TTS）
      ├── 指定 --voice myvoice → 需提供 --clone-audio-url/file 复刻声音后合成
      └── edge-tts      → 根据 --edge-tts-gender 选择男/女声（免费）
        │
        ▼
  ④ 获取每段音频时长，生成时间轴
        │
        ├── --subtitle soft/hard ↓
        │
  ⑤a  生成SRT字幕文件（与音频时间对齐）
        │
        ▼
  ⑥  生成视频片段
        ├── 首段（口播模式）
        │     ├── 音频 ≤ 15s → 上传照片+音频 → 调用 wan2.7-i2v 模型 → 轮询 → 下载口播视频
        │     └── 音频 > 15s 或 API 失败 → 降级：真人照片+音频 → ffmpeg 图片视频
        └── 其余段落 → 普通图片视频（ffmpeg）
        │
        ├── soft →  ⑦a 软字幕嵌入（mov_text轨道）
        └── hard →  ⑦b 硬字幕烧录（libass → drawtext → Python fallback）
        │
        ▼
  ⑦  输出MP4（含字幕版本）
  
        ├── --subtitle none → 直接跳过 ⑤⑥
        │
  ⑤b  静态图片视频合成（ffmpeg，无字幕）
        │
        ▼
  ⑥b  输出MP4（无字幕版本）
```

---

## 口播视频生成模块

当脚本**首段文案**以以下任意前缀开头时，自动进入口播模式：

- `口播：`（全角冒号）
- `口播:`（半角冒号）
- `【口播】`
- `[口播]`

### 生成流程

1. 验证 `--portrait` 照片路径存在，否则立即报错退出
2. 合成该段 TTS 音频，检查时长
3. 若音频时长 ≤ 15s 且 `DASHSCOPE_API_KEY` 可用：
   - 上传照片到阿里百炼系统临时文件存储，获取临时 URL (oss://)
   - 上传 TTS 音频，获取临时 URL (oss://)
   - 根据 `--portrait-quality` 调用模型：
     - `standard` (默认)：resolution=480P
     - `high`：resolution=720P
   - 提交任务后，每 5 秒轮询一次任务状态，最长等待 300s
   - 任务成功后下载视频并用作第一段
4. 若音频时长 > 15s 或生成失败：降级为 ffmpeg 图片视频（使用真人照片）

### API 规格（通过自有平台 SkillController 代理）

```
POST https://platform.delilegal.com/api/v1/skill/video/create
Headers: Authorization: Bearer {PLATFORM_API_KEY}
         Content-Type: application/json
Body: {
  "photoUrl": "https://...",     // 真人照片 OSS URL
  "audioUrl": "https://...",     // 驱动音频 OSS URL
  "quality": "standard",         // standard(480P) 或 high(720P)
  "duration": 5,                 // 2-15 整数
  "prompt": "..."                // high 质量时的 prompt
}
Response: { "success": true, "body": { "taskId": "..." } }

Task query: GET https://platform.delilegal.com/api/v1/skill/video/task/{taskId}
Success:    { "success": true, "body": { "taskStatus": "SUCCEEDED", "videoUrl": "..." } }
```

### 文件上传（三步上传到 OSS）

```
步骤一: POST https://platform.delilegal.com/api/v1/skill/video/prepareUpload
        获取 OSS 上传地址和临时 URL

步骤二: PUT {ossUploadUrl}（直接上传文件内容到 OSS）

步骤三: POST https://platform.delilegal.com/api/v1/skill/video/saveFile
        确认保存，获取最终文件访问 URL
```

---

## 声音合成模块

### 策略选择逻辑

```python
def select_tts_strategy(voice_arg: Optional[str]) -> str:
    """返回 'myvoice' 或 'edge_tts'"""
    if voice_arg and "myvoice" in voice_arg.lower():
        return "myvoice"
    return "edge_tts"
```

### voice_config.json 格式

保存平台 API Key，用于鉴权，
voice_id 用于保存我的声音（myvoice）
```json
{
  "api_key": "YOUR_PLATFORM_API_KEY_HERE"
  "voice_id": "YOUR_VOICE_ID_HERE"
}
```



### 我的声音复刻（自有平台 SkillController）

将符合声音复刻要求的音频上传到公网可访问地址（例如 OSS）后，调用自有平台接口：

```bash
curl -X POST "https://platform.delilegal.com/api/v1/skill/voice/enroll" \
      -H "Authorization: Bearer $PLATFORM_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{
            "audioUrl": "https://yourAudioFileUrl",
            "prefix": "myvoice",
            "language": "zh",
            "targetModel": "cosyvoice-v3.5-plus"
      }'
```

建议直接使用脚本：

```bash
/usr/local/bin/python3 scripts/enroll_my_voice.py \
      --audio-url "https://yourAudioFileUrl" \
      --prefix "myvoice" \
      --language zh
```

如果只有本地音频文件：

```bash
/usr/local/bin/python3 scripts/enroll_my_voice.py \
      --audio-file "/path/to/voice.wav" \
      --prefix "myvoice"
```

voice_id 仅在当次有效，不会写入配置文件。在 generate_video.py 中通过 `--clone-audio-url` 或 `--clone-audio-file` 参数自动复刻并使用。
      --audio-file "/path/to/voice.wav" \
      --prefix "myvoice" \
      --language zh
```

### edge-tts 声音映射

| 语言 | 女声（默认） | 男声 |
|------|-------------|------|
| zh-CN | zh-CN-XiaoxiaoNeural | zh-CN-YunxiNeural |
| zh-TW | zh-TW-HsiaoYuNeural | zh-TW-YunJheNeural |
| en-US | en-US-JennyNeural | en-US-GuyNeural |
| en-GB | en-GB-SoniaNeural | en-GB-RyanNeural |
| ja-JP | ja-JP-NanamiNeural | ja-JP-KeitaNeural |
| ko-KR | ko-KR-SunHiNeural | ko-KR-InJoonNeural |
| fr-FR | fr-FR-DeniseNeural | fr-FR-HenriNeural |
| de-DE | de-DE-KatjaNeural | de-DE-ConradNeural |

---

## 字幕生成规范

- 格式：SRT（SubRip Text）
- 编码：UTF-8
- 每条字幕时长：与对应音频段完全对齐
- 每行字符数：中文≤20字，英文≤42字，超出自动换行
- 时间戳精度：毫秒级

SRT示例：
```
1
00:00:00,000 --> 00:00:04,230
欢迎使用我们的产品，
这是全球领先的解决方案。

2
00:00:04,500 --> 00:00:08,100
我们的技术创新已获得
超过200项专利认证。
```

---

## 视频合成规范

- 工具：**ffmpeg**（不使用大模型，成本为零）
- 每张图片持续时长 = 对应音频时长（含0.3秒过渡缓冲）
- 图片缩放策略：`scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080`
- 音频：AAC 128kbps
- 视频：H.264，CRF 23
- 字幕：`--subtitle soft`（软字幕，独立轨道，用户可关闭）/ `--subtitle hard`（硬字幕，烧录进视频）/ `--subtitle none`（无字幕）

---

## 执行步骤

### Step 1：环境检查

```bash
# 建议使用系统 Python（托管 Python 可能存在 Pillow 签名冲突）
/usr/local/bin/python3 scripts/check_env.py
```

检查 ffmpeg、edge-tts、pillow、pydub 等依赖是否就绪。

### Step 2：复刻我的声音（可选）

voice_id 不在配置文件中存储。如需使用复刻声音，在 `generate_video.py` 中通过 `--clone-audio-url` 或 `--clone-audio-file` 参数自动复刻。

也可单独执行复刻脚本获取 voice_id：

```bash
/usr/local/bin/python3 scripts/enroll_my_voice.py \
      --audio-url "https://your-public-audio-url"
```

voice_id 仅在当次有效，不会写入配置文件。

### Step 3：准备输入

将图片素材放入 `input/images/`，文案写入 `input/script.txt`（每行一段）。

**如果不想提供图片素材**，WorkBuddy 会自动根据文案生成场景描述，写入 `input/scene_descriptions.txt`（每行一条），然后在运行脚本时通过 `--scene-descriptions input/scene_descriptions.txt` 传入即可。

### Step 4：运行生成

```bash
/usr/local/bin/python3 scripts/generate_video.py \
  --script input/script.txt \
  --images input/images/ \
  --voice myvoice \
      --clone-audio-file "/path/to/voice.wav" \
  --edge-tts-gender female \
  --lang zh-CN \
  --subtitle soft \
  --output output/product_video.mp4

# 无素材模式（使用 WorkBuddy 生成的场景描述替代图片）
/usr/local/bin/python3 scripts/generate_video.py \
  --script input/script.txt \
  --scene-descriptions input/scene_descriptions.txt \
  --voice edge_tts \
  --edge-tts-gender female \
  --lang zh-CN \
  --subtitle soft \
  --output output/product_video.mp4

# 口播模式示例（首段文案以"口播："开头）：
/usr/local/bin/python3 scripts/generate_video.py \
  --script input/script.txt \
  --images input/images/ \
  --portrait input/host.jpg \
  --voice myvoice \
  --subtitle soft \
  --output output/product_video.mp4
```

参数说明：
-- `--voice`：`myvoice` 或 `edge_tts`（默认 edge_tts）
-- `--clone-audio-url`：使用 `--voice myvoice` 时，通过公网音频URL自动复刻声音
-- `--clone-audio-file`：使用 `--voice myvoice` 时，通过本地音频文件自动复刻声音
-- `--clone-prefix`：声音复刻时的前缀，默认 `myvoice`
- `--clone-language`：声音复刻时语言提示，默认 `zh`
- `--edge-tts-gender`：`female`（女声，默认）或 `male`（男声），仅在 `--voice edge_tts` 时生效
- `--scene-descriptions`：场景描述文件路径（由 WorkBuddy 生成），每行一条，与文案段落一一对应；用于文生图 prompt
- `--subtitle`：`soft`（软字幕，默认）/ `hard`（硬字幕烧录）/ `none`（无字幕）
- `--resolution`：`1920x1080`（默认）或 `1280x720` / `1080x1920`

### Step 5：查看输出

```
output/
├── product_video.mp4       # 最终视频（含软字幕）
├── product_video.srt       # 独立字幕文件
└── audio/
    ├── segment_001.mp3
    ├── segment_002.mp3
    └── ...
```

---

## 错误处理

| 错误情况 | 处理方式 |
|----------|----------|
| voice_config.json 不存在 | 使用 edge-tts（无需 API Key 即可运行） |
| 指定 --voice myvoice 但未提供复刻音频 | 降级使用 edge-tts，提示用户提供 --clone-audio-url/file |
| 声音API调用失败 | 降级使用 edge-tts，记录警告 |
| 图片数量 ≠ 文案段落数且已提供部分图片 | 报错提示，显示不匹配详情 |
| 未提供图片且未提供 --scene-descriptions | 使用原始文案作为文生图 prompt |
| 未提供图片/场景描述且未配置 API Key | 自动降级使用 Pillow 生成包含专业法律风格（深蓝底金字）的本地配图 |
| ffmpeg 未安装 | 报错并给出安装指引 |
| 图片格式不支持 | 自动转换为PNG后继续 |
| 口播模式未提供 --portrait | 立即报错退出，提示用户提供真人照片 |
| 口播视频生成超时/失败 | 自动降级为真人照片图片视频，记录警告 |
| 口播音频时长 > 15s | 自动降级为图片视频，无需用户干预 |
| 余额不足 | 提示用户去 https://open.delilegal.com/personal/keys 充值 |

---

## 参考文档

- 依赖安装：`references/dependencies.md`
- 阿里百炼 TTS 文档：https://help.aliyun.com/zh/model-studio/text-to-speech

---

## 主执行脚本入口

核心逻辑在 `scripts/generate_video.py`，详见脚本内注释。
