# video-metadata-analyzer

视频元数据智能分析系统 — 扔一个视频文件进来，自动抽帧分析画面、转写音频内容，最后合成一份完整的 B 站投稿元数据——标题、简介、标签、分区、封面建议、创作声明，全给你准备好。

Video Metadata Intelligence System — drop in a video file and get back a complete Bilibili publishing package: title, intro, tags, category, cover suggestion, and content declaration, all generated automatically from visual and audio analysis.

> ⚠️ **隐私提示：** API 模式（`audio-llm`、`cloud`、`vision-llm`、`api` 合成）会将提取的视频帧、音频、转写文本和生成的元数据发送到你配置的外部 LLM 端点。视频可能包含人脸、声音、屏幕文字、文档或其他敏感信息。使用 API 模式前，请确认你对端点和服务商的数据处理策略充分了解。处理机密或受监管内容时，请使用 `agent-direct` 或 `local` 模式。
>
> **Privacy Notice:** API modes transmit extracted video frames, audio, transcripts, and derived metadata to your configured external LLM endpoints. Videos may contain faces, voices, on-screen text, documents, or other sensitive data. Verify endpoint trust and provider retention policy before use. Use `agent-direct` or `local` modes for confidential or regulated content.

[![ClawHub](https://img.shields.io/badge/ClawHub-video--metadata--analyzer-blue)](https://clawhub.ai/CyberKurry/video-metadata-analyzer) [![GitHub](https://img.shields.io/badge/GitHub-CyberKurry%2Fvideo--metadata--analyzer-black)](https://github.com/CyberKurry/video-metadata-analyzer) [![SkillHub](https://img.shields.io/badge/SkillHub-video--metadata--analyzer-orange)](https://skillhub.cn/skills/video-metadata-analyzer) [![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**Version:** 1.2.0 | **Owner:** [CyberKurry](https://github.com/CyberKurry)

---

## ✨ 这是什么 / What Is This

Video Analyzer 从视频文件中自动提取关键帧和音频，用 AI 分别做视觉分析和语音转写，然后把两路结果合并，生成一份完整的、可直接用于 B 站投稿的结构化元数据。

Video Analyzer automatically extracts key frames and audio from a video file, runs AI-powered visual analysis and speech transcription in parallel, then merges both results into a complete, ready-to-use Bilibili publishing metadata package.

```
视频文件 / Video file
  │
  ├─→ 🖼️ 抽帧 + 视觉分析 ──→ 画面里有什么？文字是什么？哪帧适合做封面？
  │                        What's in the frame? Any text? Good cover candidate?
  │
  ├─→ 🔊 提取音频 + 转写 ──→ 说了什么？关键信息点有哪些？什么语气？
  │                        What was said? Key points? Tone?
  │
  └─→ ✍️ 合成元数据 ──→ 标题、简介、标签、分区、封面建议、创作声明
                        Title, intro, tags, category, cover suggestion, declaration
```

视觉和音频**并行处理**，合成阶段等两者都跑完才启动。

Visual and audio run **in parallel**. Synthesis starts only after both finish.

## 🚀 快速开始 / Quick Start

```bash
bash scripts/run.sh \
  --video 你的视频.mp4 --output /tmp/output \
  --transcribe audio-llm \
  --audio-llm-key YOUR_KEY --audio-llm-base https://api.example.com/v1 --audio-llm-model mimo-v2.5 \
  --vision-llm-key YOUR_KEY --vision-llm-base https://api.example.com/v1 --vision-llm-model mimo-v2.5 \
  --max-frames 15 \
  --synthesize-method api \
  --analyze-llm-key YOUR_KEY --analyze-llm-base https://api.example.com/v1 --analyze-llm-model gpt-5.5
```

一条命令，输出三个文件：

One command, three output files:

| 文件 / File | 内容 / Content |
|------|------|
| `observations_visual.json` | 每帧画面的结构化分析（对象、文字、动作、风格、是否适合做封面） |
| `observations_audio.json` | 语音转写全文 + 说话人 + 关键信息点 + 语气 |
| `metadata.json` | 可直接用于投稿的元数据（标题、简介、标签、分区、封面建议、创作声明） |

三个 LLM（视觉 / 音频 / 合成）可以各用各的 key，也可以用同一个。

The three LLMs (vision / audio / synthesis) can use different keys and models, or share the same one.

## 📊 实际效果 / Example Output

**输入：** 一段在市集拍的老北京天桥杂技表演视频（196 秒）
**Input:** A street acrobatics performance video shot at a market (196 seconds)

**输出的标题 / Generated title:**
> 徒手托球真的不碎？老北京天桥绝活让我捏把汗

**输出的简介 / Generated intro:**
> 去逛市集，偶遇了一场老北京天桥风味的传统杂技表演，看得我手心直冒汗！视频里这位表演的师傅展示了一项极其危险的绝活：徒手托着一个球，主持人反复强调千万别碰到，因为一碰就可能碎掉伤人...

**输出的标签 / Generated tags:** 古彩戏法、硬气功、老北京天桥、徒手托球、传统杂技、民间绝活、市集表演、非遗传承

**输出的封面建议 / Cover suggestion:**
> 🥇 第 1 帧 — 红色灯笼和中式雕花门窗氛围感十足，主持人与表演者同框，画面色彩对比鲜明
> 🥈 第 10 帧 — 表演特写镜头

合成 prompt 把 LLM 定位为"资深 B 站内容运营"——标题和简介是给人看的，不是给机器看的。严禁 "深入浅出""全面解析""带你了解" 这类 AI 味空话。

The synthesis prompt positions the LLM as a "senior Bilibili content strategist" — titles and intros are written for humans, not machines. Cliché phrases like "comprehensive guide" or "let me walk you through" are explicitly banned.

## 🛣️ 两种模式 / Two Modes

**外部 LLM API（推荐）：** 给 API key，脚本全自动调 LLM 分析。视觉、音频、合成三个阶段的 key 和 model 可以分别配。

**External LLM API (recommended):** Provide an API key and the scripts call the LLM automatically. Vision, audio, and synthesis stages can each use different keys and models.

**Agent 直读（无需外部 API）：** 不给 API key，脚本只抽帧和提取音频。Agent 用自己的模型直接看帧、听音频、生成 metadata。

**Agent-direct (no external API):** Skip the API key — the script only extracts frames and audio. The Agent reads them directly using its own model to generate metadata.

两条线可以混搭——视觉走 API、音频走 Agent 直读，随你组合。缺参数自动降级到 agent-direct，不会崩。

You can mix and match — vision via API, audio via agent-direct, or any combination. Missing parameters auto-degrade to agent-direct mode; nothing crashes.

## 🎞️ 智能抽帧 / Smart Frame Extraction

不需要手动设间隔，系统自动算：

No manual interval needed — the system calculates it automatically:

| 视频时长 / Duration | 策略 / Strategy | API 调用 / API Calls |
|---------|------|---------|
| ≤ 4 分钟 / min | 单段，自适应间隔，15 帧 / single segment, adaptive interval, 15 frames | 1 次 / call |
| 30 分钟 / min | 8 段，每段 15 帧，**段间并行（最多 4 路）** / segments, parallel (max 4) | 8 次 / calls |
| 2 小时 / hr | 30 段，最多 4 路并发 / segments, max 4 concurrent | 30 次 / calls |

大帧自动压缩：超过 200KB 的帧自动缩放到 1280px 宽（JPEG quality 85），避免 API payload 过大导致 502。

Large frames are auto-compressed: anything over 200KB gets scaled to 1280px wide (JPEG quality 85) to avoid oversized API payloads causing 502 errors.

## 🔊 四种音频转写 / Four Transcription Modes

| 方式 / Mode | 说明 / Description | 需要什么 / Requirements |
|------|------|---------|
| **audio-llm** 🌐 | 多模态 LLM 直接听音频，输出结构化 JSON / Multimodal LLM listens directly, outputs structured JSON | API key + 支持音频的模型 |
| **cloud** 🌐 | 云端 Whisper API，输出纯文本转写 / Cloud Whisper API, plain text output | `--whisper-api-key` + `--whisper-api-base` |
| **local** | 本地 Whisper，免费，数据不出本机 / Local Whisper, free, data stays on your machine | `pip install openai-whisper` |
| **agent-direct** | 只提取音频文件，让 Agent 自己读，数据不出本机 / Extract audio only, Agent reads it, data stays local | ffmpeg |

🌐 = 数据会发送到外部端点。见顶部隐私提示。/ Data sent to external endpoint. See Privacy Notice at top.

音频处理全自动：WAV 自动压缩成 MP3 → 文件太大自动分片（带 2 秒重叠去重）→ 转写 → 合并。

Audio processing is fully automatic: WAV auto-compressed to MP3 → oversized files auto-chunked (2s overlap for deduplication) → transcribed → merged.

## ✍️ 合成 Prompt / Synthesis Prompt

**标题设计 / Title design:**
- ✅ `"用 AI Agent 自动审查代码缺陷，我把自家项目翻了个底朝天"`
- ✅ `"ESP32 心率监测器：20 块钱的方案也能跑"`
- ❌ `"AI Agent 技术分享"` — 空泛，没信息量 / vague, no substance

**简介 / Intro:** 帮观众判断"这个视频跟我有关吗"。自然语言分段，包含搜索关键词。不是摘要，是预告。

Helps viewers decide "is this video relevant to me?" Written in natural language, with search keywords. It's a teaser, not a summary.

**封面建议 / Cover suggestion:** 基于实际帧内容，说清楚为什么这帧好（信息密度？文字清晰？视觉冲击力？），附备选帧。

Based on actual frame content — explains why a frame works (high info density? clear text? visual impact?) with alternatives.

**创作声明 / Declaration:** 对齐 B 站网页端六选一单选：`内容无需标注` / `含AI生成内容` / `含虚构演绎内容` / `内容含营销信息` / `个人观点，仅供参考` / `内容为转载`

Matches the Bilibili web UI six-option single choice.

**作者声明 / Author marks:** 非必选多选勾选，6 项可选，如 `作者声明:视频内含有危险行为,请勿轻易模仿`

Optional multi-select checkboxes, e.g. `Author statement: contains dangerous behavior, do not imitate`.

**水印与自制声明 / Watermark & copyright:** `watermark` 默认 true（B站原创水印），`copyright_claim` 默认 false（不勾自制，仅用户明确要求时设 true）

`watermark` defaults to true (Bilibili original watermark). `copyright_claim` defaults to false (not checked unless user explicitly requests it).

**超时保护 / Timeout protection:** `run.sh` 自带 `VA_TIMEOUT` 环境变量（默认 3600s），自动 `exec timeout` 包裹防挂死

`run.sh` includes `VA_TIMEOUT` env var (default 3600s), auto-wrapped with `exec timeout` to prevent hangs.

三种合成方式 / Three synthesis methods:
- `api` 🌐 — 调 LLM 生成（推荐），失败自动退到启发式规则 / Call LLM (recommended), auto-fallback to heuristics on failure
- `agent` — 输出 prompt 文件，Agent 用自己的模型生成 / Output prompt file, Agent generates with its own model
- `manual` — 输出 Markdown 供人工审阅 / Output Markdown for manual review

## 🛡️ 三层容错 / Three-Layer Fault Tolerance

**第 1 层：网络重试 / Layer 1 — Network retry:** API 返回 5xx 或断连 → 自动重试 3 次，指数退避。API returns 5xx or disconnect → auto-retry 3 times with exponential backoff.

**第 2 层：解析重试 / Layer 2 — Parse retry:** 模型输出不是合法 JSON？把错误信息喂回去让它重新出。最多 3 轮。Model output isn't valid JSON? Feed the error back for a retry. Up to 3 rounds.

**第 3 层：优雅降级 / Layer 3 — Graceful degradation:** 视觉：占位观测；音频：保留原始文本；合成：启发式规则。参数缺失自动退到 agent-direct。Vision: placeholder observations. Audio: raw text preserved. Synthesis: heuristic rules. Missing params auto-degrade to agent-direct.

## 📦 输出格式 / Output Format

### metadata.json

```json
{
  "title": "80字以内，像 UP 主写的标题",
  "intro": "2000字以内，给观众看的视频介绍",
  "tags": ["标签1", "标签2"],
  "category": "B站一级分区（2026-05 type2 平铺，共30个）",
  "cover_suggestion": {
    "primary": "推荐帧文件名",
    "reason": "为什么这帧适合做封面",
    "secondary": "备选帧文件名"
  },
  "declaration": "内容无需标注",
  "copyright_claim": false,
  "watermark": true,
  "author_marks": []
}
```

### observations_visual.json

每帧一个对象：`frame`（文件名）、`objects`（关键实体）、`desc`（~100字六要素描述）、`texts`（画面文字）、`actions`（动作事件）、`style`（风格标签）、`cover_candidate`（是否适合做封面）

One object per frame: `frame` (filename), `objects` (key entities), `desc` (~100 chars, 5W1H description), `texts` (on-screen text), `actions` (action events), `style` (style tags), `cover_candidate` (suitable for cover).

### observations_audio.json

`transcript`（完整转写）、`speakers`（说话人）、`key_points`（3-8 个关键信息点）、`tone`（语气风格）

`transcript` (full transcription), `speakers` (speaker identification), `key_points` (3–8 key info points), `tone` (tone/style).

## 📁 文件结构 / File Structure

```
video-metadata-analyzer/
├── SKILL.md                # Agent 技能描述 / Agent skill descriptor
├── README.md               # 你正在读的这个 / This file
├── TOPOLOGY.md             # 架构拓扑（开发者参考）/ Architecture topology
├── references/
│   └── REFERENCE.md        # 完整参数表、JSON schema、独立使用示例
└── scripts/
    ├── common.py            # 公共工具 / Shared utilities (HTTP retry, media duration, JSON parse)
    ├── run.sh               # 一键编排 / Orchestrator (parallel visual+audio, then synthesis)
    ├── visual.py            # 抽帧 + 视觉观测 / Frame extraction + visual observation
    ├── transcribe.py        # 音频转写 / Audio transcription (4 modes)
    └── analyze.py           # 合成投稿元数据 / Synthesize publishing metadata (3 methods)
```

## 📦 依赖 / Dependencies

| 依赖 / Dependency | 必需 / Required | 用途 / Purpose |
|------|------|------|
| **ffmpeg / ffprobe** | ✅ | 抽帧、音频提取、压缩 / Frame extraction, audio extraction, compression |
| **Python 3.8+** | ✅ | 纯 Python，API 模式不需要额外 pip 包 / Pure Python, no extra pip packages for API mode |
| **Pillow** | 推荐 / Recommended | 帧图片压缩，没装自动退到 ffmpeg / Frame compression, auto-fallback to ffmpeg |
| **openai-whisper** | 可选 / Optional | 仅 `--transcribe local` 时需要 / Only for `--transcribe local` |
| **外部 LLM API** | 可选 / Optional | OpenAI 兼容的 chat completions 端点 / OpenAI-compatible chat completions endpoint |

## 📄 许可证 / License

MIT License — 可自由使用、修改、分发，需保留版权声明和 LICENSE 文件。详见 [LICENSE](LICENSE)。

MIT License — free to use, modify, and distribute with copyright notice retained. See [LICENSE](LICENSE) for details.

## 🔗 链接 / Links

- **ClawHub**: https://clawhub.ai/CyberKurry/video-metadata-analyzer
- **SkillHub**: https://skillhub.cn/skills/video-metadata-analyzer
- **GitHub**: https://github.com/CyberKurry/video-metadata-analyzer
- **Owner**: [CyberKurry](https://github.com/CyberKurry)
