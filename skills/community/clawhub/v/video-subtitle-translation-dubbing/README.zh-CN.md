# 视频字幕翻译与自动配音技能 (Video Translation & Dubbing Skill)

[English](./README.md) | [简体中文]

[![Python Version](https://img.shields.io/badge/python-3.11%20%7C%203.12-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Apache_2.0-green.svg)](LICENSE)
[![Framework](https://img.shields.io/badge/framework-OpenClaw-orange.svg)](https://github.com/OpenClaw)

一个高质量的 **OpenClaw 技能（Skill）**：支持在多种语言（如英文、中文、日文、西班牙文、法文、德文、韩文等）之间进行视频字幕自动翻译与配音，并可选择基于目标语言语音合成（TTS，支持自动语种映射）以及音轨时间对齐技术，生成具有**双音轨、双字幕轨**的高品质配音视频。

---

## 🌟 核心特性

- 🛠 **双模式灵活处理**：
  - **`subtitle_only`**（仅字幕模式）：仅翻译字幕。输出视频保留原始音轨（默认），内嵌源语言和翻译后的目标语言双字幕轨，并输出独立 `.srt`/`.vtt` 目标语言字幕文件。
  - **`subtitle_and_dubbing`**（字幕+配音模式，默认）：翻译字幕并配音。利用 TTS 生成目标语言配音，自动根据原字幕时间轴进行**音频伸缩与对齐**，无损合成包含源语言/目标语言双音轨、源语言/目标语言双字幕轨的视频，目标语言音轨及字幕轨默认开启。
- ⚖ **三维自适应调度器 (Adaptive Scheduler)**：
  - 内置了**批量 (Batch Size)**、**文本量 (Payload Size)**、**并发度 (Concurrency)** 三维自适应调节策略。
  - 能够自适应应对大模型 API 的 Rate Limit（频率限制）及 Context Window 限制，并在遇到 429 报错或 Context 溢出时自动降级重试与重新切片，极大降低调用成本和失败概率。
- 🔌 **可插拔后端适配器 (Pluggable Providers)**：
  - **翻译后端**：支持 `llm`（大语言模型，内置 MiniMax / DeepSeek / OpenAI 等兼容协议并支持自动处理 `<think>` 思考过程）与 `web`（网络翻译 API）。
  - **TTS 后端**：支持 `llm` 与 `web`（网络 TTS）。
- ⚡ **无损封装与高质量对齐**：使用 `ffmpeg` 对多音轨、多字幕轨进行无损封装（MKV容器），不降低原始视频的画质。

---

## 🧱 项目结构

```
src/translation_dubbing_skill/
├── models/          # 数据模型 (ProcessingMode, SubtitleEntry 等)
├── subtitle/        # 字幕解析器与序列化器 (支持 SRT / VTT)
├── providers/       # 可插拔后端实现
│   ├── translation/ # 翻译提供方 (LLM 接口, Web 接口)
│   └── tts/         # 语音合成提供方 (LLM 接口, Web 接口)
├── scheduler/       # 三维自适应调度器 (批量、文本量、并发自适应)
├── align/           # 音频对齐与时间拉伸器
├── mux/             # 音视频合成多路复用 (ffmpeg 封装)
├── progress/        # 进度反馈与状态监听
├── errors/          # 统一的错误层次结构
└── entry/           # 技能入口与 Manifest 配置解析
```

---

## 🚀 快速开始

### 1. 环境准备
- **Python 3.11+**
- **FFmpeg**：需要在系统的 `PATH` 环境变量中可用。
  - **macOS**: `brew install ffmpeg`
  - **Ubuntu**: `sudo apt install ffmpeg`

### 2. 安装依赖
克隆项目后，在根目录下执行：
```bash
pip install -e .
# 如果需要运行测试或进行开发：
pip install -e ".[dev]"
```

### 3. 配置凭证
复制环境变量模板文件并填写你的 API Keys：
```bash
cp .env.example .env
```
根据 `.env` 中的说明，配置你的大模型或翻译/TTS 提供商凭证。

---

## ⚙ 清单文件配置 (manifest.yaml)

作为一个标准的 OpenClaw 技能，本技能通过 `manifest.yaml` 来声明其输入、输出与运行配置。以下是核心配置字段：

| 参数名 | 类型 | 是否必填 | 默认值 | 描述 |
| :--- | :--- | :--- | :--- | :--- |
| `video_path` | `path` | 是 | - | 输入的原始视频路径 |
| `subtitle_path` | `path` | 否 | - | 外挂字幕（.srt/.vtt）。缺省时自动提取视频内嵌字幕 |
| `source_language` | `string`| 是 | `en` | 原始视频/字幕语言（如 `en`, `zh-CN`, `ja` 等） |
| `target_language` | `string`| 是 | `zh-CN` | 目标翻译/TTS语言（如 `zh-CN`, `en`, `ja` 等） |
| `processing_mode` | `enum` | 是 | `subtitle_and_dubbing` | 运行模式：`subtitle_only` 或 `subtitle_and_dubbing` |
| `translation_provider` | `enum` | 是 | - | 翻译提供方：`llm` 或 `web` |
| `translation_endpoint` | `string`| 是 | - | 翻译服务的 API 端点地址 |
| `translation_credential`| `secret`| 是 | - | 翻译服务的 API Key / Token |
| `tts_provider` | `enum` | 条件必填 | - | 配音模式下必填：`llm` 或 `web` |
| `tts_endpoint` | `string`| 条件必填 | - | 配音模式下必填：TTS 服务的 API 端点地址 |
| `tts_credential` | `secret`| 条件必填 | - | 配音模式下必填：TTS 服务的 API Key |

> 完整的配置架构和更高级的调度器参数（例如 `translation_rate_limit` 和 `tts_rate_limit` 自适应参数微调）请参考 [manifest.yaml](manifest.yaml)。

---

## 🧪 运行测试

本项目配备了完整的单元测试与属性测试（使用 Hypothesis）：

```bash
# 运行全部测试
pytest

# 运行除集成测试外的快速单元测试
pytest -m "not integration"
```

---

## 📄 开源协议

本项目采用 [Apache-2.0 License](LICENSE) 协议开源。
