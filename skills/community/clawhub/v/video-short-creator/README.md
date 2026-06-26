# Video Short Creator

> 两阶段 AI 旁白短视频创作工具，每个关键步骤都有人工审核检查点。

将现有视频片段和脚本转化为带有 AI 旁白和字幕的短视频，适合科技论文解读、产品介绍等社交媒体内容。

## ✨ 特性

- **两阶段审核工作流**：先生成审核材料 → 人工确认 → 再执行剪辑
- **AI 语音合成**：使用 Microsoft edge-tts（免费，无需 API Key）
- **电影风格字幕**：小号字体、底部对齐、不遮挡画面主体
- **智能转场**：xfade 淡入淡出 + 黑场过渡自动交替
- **完全离线**：除 TTS 外所有处理在本地完成，无需云端服务

## 📋 前置要求

| 工具 | 用途 | 安装方式 |
|------|------|----------|
| **FFmpeg** | 视频处理 | `winget install FFmpeg` 或 [官网下载](https://ffmpeg.org/download.html) |
| **Python 3.8+** | 脚本执行 | 使用 WorkBuddy 内置运行时 |
| **edge-tts** | 微软 TTS | `pip install edge-tts`（无需 API Key） |
| **SimHei 字体** | 中文字幕渲染 | Windows 通常已预装 (`C:\Windows\Fonts\simhei.ttf`) |

## 🚀 使用方式

### Phase 1：素材准备与审核

1. **提供素材**：视频片段路径 + 旁白脚本（或提供参考资料由 AI 生成）
2. **AI 分析素材**：自动扫描片段元数据，生成片段清单
3. **生成配音**：edge-tts 生成每个分段的旁白音频
4. **导出审核表**：包含所有字幕条目（序号、时间轴、文本内容）

> ⚠️ **关键：Phase 1 完成后必须等待用户确认，不得自动进入 Phase 2。**

### Phase 2：视频剪辑（审核通过后）

1. **应用修改**：如有用户修改，更新字幕条目
2. **裁剪缩放**：按指定起止时间提取片段，缩放到目标分辨率
3. **烧录字幕**：SRT 字幕文件 + FFmpeg subtitles 滤镜
4. **转场拼接**：xfade 转场连接各分段
5. **音视频合并**：最终输出完整视频

## 📁 文件结构

```
video-short-creator/
├── SKILL.md                      # Skill 主文档（AI Agent 执行指南）
├── README.md                     # 本文件
├── scripts/
│   ├── step1_generate_review.py  # Phase 1: 生成配音 + 导出审核表
│   └── step2_edit_video.py       # Phase 2: 审核后执行视频剪辑
└── references/
    ├── config-example.py         # 配置模板（含可用中文语音列表）
    └── ffmpeg-pitfalls.md        # Windows FFmpeg 踩坑记录
```

## ⚙️ 配置

所有配置通过 SCRIPT 数据结构传递，关键参数：

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `VOICE` | `zh-CN-YunxiNeural` | TTS 语音（中文年轻男声） |
| `TARGET_W/H` | 1920×1080 | 输出分辨率 |
| `XFADE_DUR` | 0.8s | 转场时长 |
| `SUBTITLE_FONT_SIZE` | 14 | 字幕字号 |
| `SUBTITLE_MARGIN_V` | 50 | 字幕底部边距(px) |

### 可用中文语音（edge-tts）

| 语音 ID | 描述 |
|---------|------|
| `zh-CN-YunxiNeural` | 年轻男声（推荐，自然活泼） |
| `zh-CN-YunjianNeural` | 成熟男声（新闻播报风格） |
| `zh-CN-XiaoxiaoNeural` | 年轻女声（温柔亲切） |
| `zh-CN-XiaoyiNeural` | 知性女声（专业解说） |

## 🎬 输出规格

- **分辨率**：1920×1080（横屏），30 FPS
- **视频编码**：H.264 CRF 20
- **音频编码**：AAC 128kbps
- **字幕风格**：SimHei 字体、14号、白色、细描边、底部对齐

## ⚠️ 已知注意事项（Windows）

- **不要用 `drawtext` 滤镜** — Windows 下特殊字符转义不可靠，始终使用 `.srt` + `subtitles` 滤镜
- **SRT 路径需要转义**：`\` → `/`，`:` → `\:`
- **edge-tts `SentenceBoundary`** 给出干净的文本分割；`WordBoundary` 可能包含 `n` 等杂散字符
- **xfade 标签**必须用 `tmp0`, `tmp1` 格式（不能用 `v01`, `v02`）

详细踩坑记录见 `references/ffmpeg-pitfalls.md`。

## 📝 License

MIT-0
