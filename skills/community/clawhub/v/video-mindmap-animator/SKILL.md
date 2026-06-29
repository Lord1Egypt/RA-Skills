---
name: "video-mindmap-animator"
description: "视频号深度科普视频全案：思维导图动画 + 长句旁白 + BGM + 多时长压缩。适用图文转视频、科普内容视频化。"
---

# video-mindmap-animator

> 视频号深度科普视频全案 — 从图文/笔记到多时长成片的端到端制作技能

## 何时使用

- 老板有现成**公众号图文/笔记/长文**，想做成视频号深度科普视频
- 想避免"真人出镜 / 数字人 / T2V 崩坏"，偏好**结构化思维导图动画**
- 内容调性：去 AI 味、口语化、我们站位、长句叙述
- 老板反馈多次：AI 味、半句话、英文符号 TTS 怪异、文案与画面不同步

## 核心定位

**不是**引流短视频钩子型（30 秒带量），**而是**科普深度视频（3-5 分钟立人设）。

| 维度 | 引流短视频 | 科普深度视频（本技能）|
|---|---|---|
| 时长 | 30s | 3-5 分钟（可压 1.5-2x → 1:55-3:20）|
| 画面 | 强冲击人物 | 思维导图动画，无人物 |
| 旁白 | 可选静音字幕 | 必有长句旁白 |
| 目的 | 流量转化 | IP 沉淀 + 知识传递 |

## 端到端 9 步流程

### Step 1：内容评估与方向判断
- 老板给图文/笔记 → 评估长度（建议 2000-5000 字）
- 拆分核心算式（一句话能写下的命题）
- 5-7 个场景分段（钩子/归因/细节/反差/反馈/总结）
- 决策：是否值得做视频（看受众是否视频号主流量）

### Step 2：文字分镜（script.md）
```
S1 钩子       0:00-0:15   帧 0-450
S2 归因       0:15-0:45   帧 450-1350
S3 员工阻力   0:45-1:30   帧 1350-2700
S4 四个机制   1:30-2:30   帧 2700-4500
S5 反差       2:30-3:15   帧 4500-5850
S6 反馈回路   3:15-3:45   帧 5850-6750
S7 总结       3:45-4:00   帧 6750-7200
```
- 每个场景列**画面元素清单**（圆节点、副标、底部金句等）
- 文字与画面**一一对应**

### Step 3：渲染视频帧（思维导图动画）

**工具**：Python PIL + ffmpeg
- 画幅 1080×1920（9:16 视频号）
- 30 fps
- 字体 msyh.ttc / msyhbd.ttc
- 配色：#1e3a5f 深蓝 / #d4af37 金 / #faf8f4 米 / #c0392b 红警示

**核心代码模式**：
```python
def render_scene(frame_idx, total_in_scene):
    t = frame_idx / total_in_scene  # 0-1
    img = Image.new("RGB", (W, H), COL_BG)  # 基础浅米画布
    # 每个元素：make_layer() + 绘制 + apply_layer_alpha() + paste
    return img
```

**关键函数**：
- `ease_out_cubic(t) = 1 - (1-t)**3`（节点浮现）
- `ease_in_out_cubic(t)`（文字淡入）
- `apply_layer_alpha(layer, factor)`：**用 split/merge 正确处理 alpha**（不是 putalpha！）

**踩坑（必看）**：
- ❌ `layer.putalpha(N)` 把整图层 alpha 设为 N → 黑色覆盖整画布
- ✅ 修复：`r,g,b,a = layer.split(); a = a.point(lambda p: int(p * f)); Image.merge(...)`

**ffmpeg 合成**：
```bash
ffmpeg -framerate 30 -i frames/frame_%04d.png \
  -c:v libx264 -pix_fmt yuv420p -crf 18 -preset slow \
  output.mp4
```

### Step 4：旁白稿（去 AI 味 5 原则）

**5 大原则**（老板多次反馈沉淀）：
1. **长句叙述** 40-60 字/句，**不是**短句堆砌
2. **口语连接词**："讲到这" / "你看" / "回头看" / "我们"
3. **数字汉字化**："七成三" 而非 "73%"
4. **人名汉化**："科特" 而非 "Kotter"
5. **符号零容忍**：删除引号/破折号/百分号/小数

**节奏锚定**：
- 默认 4.3 字/秒（rate=-15%）
- 4 分钟 ≈ 1000 字 + 自然停顿
- 2 分钟 ≈ 500-600 字

**v3 长句 vs v2 短句对比**：
```
v2 (AI 味)              v3 (长句叙述)
管理者盲区，七成。        管理者盲区七成，这个数字看着大，里面其实有四个具体
决定胜败的两成。          的机制在起作用，每一个都会让我们在自我察觉这件事上
四个机制叠在一起。        失效。第一个机制是约哈里之窗的盲区，自己不知别人知。
                         比如我们自己的口头禅、习惯动作，全世界都看得见，
                         自我们自己看不见。
```

### Step 5：配音生成（Edge TTS）

**关键认知**：
- ❌ `edge_tts.Communicate` **不支持 SSML**
- 传 `<speak><voice><prosody><break>` 整段当纯文本 → **TTS 念出标签**
- 注释 `<!-- 注释 -->` 也被朗读

**正确用法**：
```python
communicate = edge_tts.Communicate(
    TEXT,                       # 纯文本，无标签
    voice="zh-CN-YunxiNeural",  # 成熟男声
    rate="-15%",                # 自然略慢
    pitch="+0Hz",
)
await communicate.save("out.mp3")
```

**中文男声备选**：
- `zh-CN-YunxiNeural`（成熟，推荐）
- `zh-CN-YunyangNeural`（新闻）
- `zh-CN-YunjianNeural`（浑厚）

### Step 6：BGM 生成（mmx music）

```powershell
mmx music generate \
  --prompt "soft contemplative piano, 60 bpm, minimal, hopeful undertone, cinematic, no vocals" \
  --instrumental \
  --out bgm.mp3
```

**踩坑**：
- mmx music-2.6 **默认 4 分钟**，不能指定时长
- 需要更短 → ffmpeg `-t` 裁剪（不要 atempo 加速）
- 需循环 → ffmpeg `-stream_loop -1`

### Step 7：音视频混合

```bash
ffmpeg -y \
  -i video.mp4 \
  -i voiceover.mp3 \
  -stream_loop -1 -i bgm.mp3 \
  -filter_complex "[2:a]volume=0.18,afade=t=in:st=0:d=1.0,afade=t=out:st=N-1:d=1.0[b];[1:a][b]amix=inputs=2:duration=longest[a]" \
  -map 0:v -map "[a]" \
  -c:v copy -c:a aac -b:a 128k \
  -shortest \
  output.mp4
```

**踩坑**：
- `-c:v copy` 与 filter 冲突 → 用 `-c:v libx264 -preset fast` 重编码
- 输出 0 字节 → 加 `-movflags +faststart`
- moov atom not found → 同样 `-movflags +faststart`

### Step 8：多时长压缩

| 目标 | 视频 | 旁白 | BGM |
|---|---|---|---|
| 4:00 完整 | setpts 1.0x | 1.0x（自然）| 1.0x |
| 2:24 中等 | setpts 0.6x | 重生精简稿 1.0x | `-t 144` 裁剪 |
| 1:55 紧凑 | setpts 0.8x | wave 1.25x | wave 1.25x |
| 2:00 极速 | setpts 0.5x | atempo 2.0x ❌ 诡异 | 裁 2:00 |

**音频加速**（最关键）：
- ❌ atempo 2.0+ 失真诡异（老板亲口反馈）
- ❌ wave 重采样 1.65x → 老板嫌薄
- ✅ wave 重采样 1.25x 略微加速（1/1.25 = 80% 时长）
- ✅ 或 atempo 1.0x（不加速）配精简字数

**wave 重采样代码**（保 pitch）：
```python
new_framerate = int(framerate * speed)  # 24000 * 1.25 = 30000
audio = audio._spawn(raw, overrides={"frame_rate": new_framerate})
audio = audio.set_frame_rate(framerate)  # 改回
```

或 ffmpeg：
```bash
ffmpeg -i in.mp3 -af "asetrate=28800,aresample=24000" out.mp3
```

### Step 9：9 步审 + 交付

1. 分辨率 1080×1920 ✅
2. 时长匹配版本 ✅
3. 字幕对齐画面元素 ✅
4. 音频同步（不漂移）✅
5. 首帧合规（无敏感内容）✅
6. BGM 不盖过旁白（音量 ≤ 20%）✅
7. 旁白音调自然（**不要 atempo 2.0+**）✅
8. 数字/人名无英文 ✅
9. 视频号尺寸 2.35:1 封面（如需公众号同步）✅

## 关键踩坑清单（必记）

| # | 坑 | 修复 |
|---|---|---|
| 1 | edge_tts.Communicate 不支持 SSML | 用纯文本 + rate/pitch/voice 参数 |
| 2 | SSML 注释被朗读 | 删除所有 XML 注释 |
| 3 | atempo 2.0+ 音调诡异 | 不超过 1.5x，或用 wave 重采样 |
| 4 | wave 重采样 1.65x 变薄 | 不超过 1.30x |
| 5 | ffmpeg 链式 atempo 行为异常 | 改用单段 atempo 或 wave 重采样 |
| 6 | pydub speedup 缺 ffprobe | 用 imageio_ffmpeg 路径 + env var |
| 7 | PIL putalpha 整图层 | split/merge 单独处理 alpha |
| 8 | ffmpeg 写 mp4 moov atom not found | 加 `-movflags +faststart` |
| 9 | ffmpeg concat 列表 BOM 干扰 | UTF-8 无 BOM（PS 用 .NET UTF8Encoding $False）|
| 10 | PS 5.1 GBK 输出 emoji 报错 | 输出用 ASCII 或 sys.stdout 编码 |
| 11 | mmx music 默认 4 分钟 | ffmpeg `-t` 裁剪 |
| 12 | ffmpeg `-c:v copy` 与 filter 冲突 | 改 `-c:v libx264 -preset fast` |
| 13 | imageio_ffmpeg 路径含特殊字符 | 用 raw string `r"..."` |

## 工具链固定路径

```
Python: C:\Users\ZWB2016\AppData\Local\Programs\Python\Python312\python.exe
ffmpeg: C:\Users\ZWB2016\AppData\Local\Programs\Python\Python312\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe
字体: C:\Windows\Fonts\msyh.ttc / msyhbd.ttc
项目目录: output/videos/<project_name>/<episode>/
  ├── <episode>_script.md          文字分镜
  ├── <episode>_voiceover.md       旁白稿
  ├── render_<episode>.py          视频帧渲染脚本
  ├── voiceover_<episode>.py       TTS 生成脚本
  ├── make_<episode>.py            完整混合脚本
  ├── voiceover_<ver>.mp3         各种旁白
  ├── bgm_<ver>.mp3               BGM
  ├── <episode>_video_<dur>.mp4   视频流（无音）
  └── <episode>_v<N>_<dur>_with_voice.mp4  最终成片
```

## 老板风格观察（深度沉淀）

老板对"AI 味"极度敏感（多次反馈），核心判断标准：

| 老板厌恶 | 老板认可 |
|---|---|
| 短句堆砌（"X 是 Y" / "X 与 Y"）| 长句叙述（主谓宾齐全）|
| 格言警句式结尾 | 朴素陈述 + 自然过渡 |
| "综上所述" / "值得注意的是" | "讲到这" / "回头看" |
| 数字英文（73% / Kotter）| 数字汉字（七成三 / 科特）|
| 旁白与画面不同步 | 旁白与画面元素一一对应 |
| 符号（引号 / 破折号 / 百分号）| 全部删掉或换说法 |
| atempo 加速 | 自然语速 + 精简字数 |

**老板话术风格**：
- 极简、不啰嗦
- 反馈精准（如"音调诡异"、"半句话感觉"）
- 倾向快速迭代（v1→v2→v3→v3.1→v3.2→v4.0→v5.0）
- 不喜欢"等一下让我重做"——希望直接出方案

## 完整脚本模板（直接复用）

**1. 视频帧渲染（render_xxx.py）**：
```python
W, H = 1080, 1920
FPS = 30
DURATION = 240
TOTAL_FRAMES = FPS * DURATION

COL_BG = (250, 248, 244)
COL_NAVY = (30, 58, 95)
COL_GOLD = (212, 175, 55)
COL_RED = (192, 57, 43)
COL_GRAY = (44, 62, 80)

FONT_PATH = r"C:\Windows\Fonts\msyh.ttc"
FONT_BOLD = r"C:\Windows\Fonts\mshybd.ttc"

def ease_out_cubic(t): return 1 - (1 - t) ** 3
def ease_in_out_cubic(t):
    if t < 0.5: return 4 * t * t * t
    return 1 - (-2 * t + 2) ** 3 / 2

def apply_layer_alpha(layer, factor):
    r, g, b, a = layer.split()
    a = a.point(lambda p: int(p * factor))
    return Image.merge("RGBA", (r, g, b, a))

def make_layer(): return Image.new("RGBA", (W, H), (0, 0, 0, 0))

# SCENE_MAP 调度
# render_s1 ~ render_s7 各场景函数
# main() 按帧号分发渲染
```

**2. TTS 生成（voiceover_xxx.py）**：
```python
import asyncio, edge_tts

TEXT = """<纯文本，无 SSML>
"""

async def main():
    communicate = edge_tts.Communicate(
        TEXT,
        voice="zh-CN-YunxiNeural",
        rate="-15%",
        pitch="+0Hz",
    )
    await communicate.save("voiceover.mp3")
```

**3. 多版本混合（make_xxx.py）**：
```python
import subprocess

FFMPEG = r"C:\Users\...\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"

def mix(video, voiceover, bgm, output, duration):
    cmd = [
        FFMPEG, "-y",
        "-i", video,
        "-i", voiceover,
        "-stream_loop", "-1", "-i", bgm,
        "-filter_complex", f"[2:a]volume=0.18,afade=t=in:st=0:d=1.0,afade=t=out:st={duration-1}:d=1.0[b];[1:a][b]amix=inputs=2:duration=longest[a]",
        "-map", "0:v", "-map", "[a]",
        "-c:v", "libx264", "-preset", "fast", "-crf", "20",
        "-c:a", "aac", "-b:a", "128k",
        "-movflags", "+faststart",
        "-shortest",
        output,
    ]
    subprocess.run(cmd, check=True)
```

## 适用场景扩展

- **公众号图文 → 视频号深度视频**（本次主用）
- **长文章/笔记 → 思维导图讲解视频**
- **5 条系列科普**（E1-E5，本次规划但未全做）
- **跨平台分发**：视频号 + B 站 + 抖音 + 知乎 + 小红书（同一视频素材）

## 不适用场景

- 需要真人 IP（强镜头感、表情）的视频
- 30 秒钩子型引流短视频
- 复杂电影级特效动画
- 实时直播

## 沉淀引用

- 原始会话：2026-06-13 09:22 - 20:25
- 项目目录：`output/videos/ceo_obstacle_v1/E1/`
- 全部产出：v1 静默 / v2 短句 / v3.1 长句+加速 / v3.2 自然 / v4.0 2:24 / v5.0 1:55
- 核心交付：v5.0_1min55_with_voice.mp4（推荐）
