---
name: qclaw-speaker
description: |
  四引擎本地轻量CPU TTS语音播报系统。让 QClaw/OpenClaw 像豆包一样自然开口说话。
  引擎：Edge TTS（在线微软神经）→ sherpa-onnx Piper（离线13MB ONNX）→ Windows SAPI（离线原生）。
  支持 11 款中文音色、自动语音播报、引擎智能降级、一键安装。
  Use when: 用户说"语音播报"/"说话"/"开口"/"读出来"/"念给我听"/"tts",
  要求文字转语音, 需要自动语音回复, 无障碍/驾车/做饭场景。
---

# 🎙️ QClaw Speaker — 让 AI 自然开口说话

**四引擎本地轻量 CPU TTS 语音播报系统**。无需 GPU，无需云 API，13MB 模型即可在 CPU 上实时合成中文语音，流畅度媲美云服务。

> 如果说 `video-subtitle-extractor` 是给大模型装上了"视频字幕眼睛"，
> 那么 `qclaw-speaker` 就是给它装上了"嘴巴"，像豆包一样自然开口！

---

## 🚀 Quick Start

```bash
# 一键安装（2引擎 + 默认音色）
python scripts/install.py

# 说话！
python scripts/speak.py "你好，我是QClaw，很高兴为你服务！"
python scripts/speak.py "大家好" --voice yunxi      # 男声
python scripts/speak.py "离线播报" --engine sherpa   # 本地离线
python scripts/speak.py "系统原生" --engine win       # Windows自带

# 切换默认音色
python scripts/speak.py --set-voice xiao_ya

# 开启自动播报
python scripts/speak.py --auto-speak on
```

---

## 📊 2025-2026 本地轻量 CPU 中文 TTS 模型全景对比

### 技能内置引擎对比

| 排名 | 引擎 | 大小 | RAM | 中文 | CPU速度 | 流式 | 离线 | 说明 |
|:----:|------|-----:|----:|:----:|--------|:----:|:----:|------|
| 🥇 | **Edge TTS** | 0 | ~50MB | ⭐⭐⭐⭐⭐ | <1s | ✅ | ❌ | 微软神经TTS，免费在线 |
| 🥈 | **Sherpa+Piper** | 13MB | ~200MB | ⭐⭐⭐⭐ | RTF 0.05 | ✅ | ✅ | ONNX推理，CPU极快 |
| 🥉 | **Windows SAPI** | 0 | ~50MB | ⭐⭐⭐ | <0.1s | ❌ | ✅ | 系统原生，零配置 |

### 其他值得关注的候选（可扩展）

| 模型 | 大小 | RAM | 中文 | CPU速度 | 流式 | 优势 |
|------|-----:|----:|:----:|--------|:----:|------|
| **Kokoro v1.0** | 85MB | ~500MB | ⭐⭐⭐⭐ | RTF 0.04 | ✅ | 多语言，极快，ONNX |
| **Piper C++ 原生** | 30MB | ~300MB | ⭐⭐⭐⭐ | RTF 0.03 | ✅ | 纯C++，最快，独立 |
| **Matcha-TTS** | 72MB | ~500MB | ⭐⭐⭐⭐⭐ | RTF 0.05 | ✅ | 中文轻量最优质量 |
| **ChatTTS 2.0** | 600MB | ~2GB | ⭐⭐⭐⭐⭐ | RTF 0.5 | ❌ | 最自然人声(非实时) |
| **MeloTTS** | 160MB | ~1GB | ⭐⭐⭐⭐ | 快 | ❌ | MIT开源，微软出品 |
| **ZipVoice(int8)** | 104MB | ~600MB | ⭐⭐⭐⭐⭐ | RTF 0.08 | ✅ | 中英混合极好 |
| **espeak-ng** | 6MB | ~100MB | ⭐⭐ | 闪电 | ✅ | 超轻量，全语言 |

### 决策指南

```
需要离线？ ─YES→ 选择 Sherpa+Piper (13MB) 或 Windows SAPI (0MB)
需要实时流式？ ─YES→ Edge TTS / Sherpa / Kokoro
最小RAM？ ─→ Windows SAPI (50MB) / Sherpa (200MB)
最佳中文？ ─→ Edge TTS (在线) / Matcha-TTS (离线72MB)
最快速度？ ─→ Piper C++ 原生 (RTF 0.03) / Kokoro (RTF 0.04)
```

---

## 🎤 四引擎详解

| 特性 | ☁️ Edge TTS | 🏠 Sherpa+Piper | 💻 Win SAPI |
|------|-------------|----------------|-------------|
| 网络 | 需要 | **无需** ✅ | **无需** ✅ |
| 模型下载 | 零 | 13MB | 零 |
| RAM占用 | ~50MB | ~200MB | ~50MB |
| 首字延迟 | ~0.5s | **<0.1s** | **<0.05s** |
| 中文音色 | 6款 | 3款 | 1款 |
| 流式输出 | ✅ | ✅ | ❌ |
| 隐私 | 数据上云 | 本地处理 | 本地处理 |
| 安装 | `pip edge-tts` | `pip sherpa-onnx` | 系统自带 |

### 自动降级逻辑
```
请求播报
  ├── 1. Edge TTS (品质最优)
  ├── 2. Sherpa-onnx (本地离线)  ← 网络不佳时
  └── 3. Windows SAPI (终极兜底)  ← 都不行时
```

---

## 🎨 内置音色库（11款）

### Edge TTS — 6款在线微软神经语音

| 音色 | 风格 | 推荐场景 |
|------|------|---------|
| `xiaoxiao` ⭐ | 晓晓，标准女声 | **默认通用** |
| `yunxi` | 云希，活泼男声 | 讲解/教程 |
| `xiaoyi` | 晓依，温柔女声 | 情感内容 |
| `xiaochen` | 晓辰，自然男声 | 新闻播报 |
| `yunyang` | 云扬，沉稳男声 | 正式场合 |
| `xiaohan` | 晓涵，少女声 | 轻快内容 |

### Sherpa-onnx Piper — 3款本地离线

| 音色 | 大小 | 风格 | RTF |
|------|-----:|------|-----|
| `xiao_ya` ⭐ | 13MB | 小雅，温暖女声 | 0.05 |
| `chaowen` | 13MB | 超稳，沉稳男声 | 0.05 |
| `huayan` | 64MB | 花颜，柔和女声 | 0.10 |

### Windows SAPI — 1款系统原生

| 音色 | 大小 | 风格 |
|------|-----:|------|
| `huihui` | 0 | 慧慧，系统中文语音 |

---

## 🏗️ 技术架构

```
┌─────────────────────────────────────────────────────────┐
│                     QClaw / OpenClaw                     │
│                                                          │
│  ┌──────────┐     ┌──────────────┐     ┌─────────────┐ │
│  │ LLM 输出  │ →   │  speak.py    │ →   │  音频输出    │ │
│  │ (文本)    │     │  引擎调度器    │     │  (WAV/MP3)  │ │
│  └──────────┘     └──────┬───────┘     └─────────────┘ │
│                          │                               │
│            ┌─────────────┼─────────────┐                │
│            ▼             ▼             ▼                │
│     ┌──────────┐  ┌──────────┐  ┌──────────┐          │
│     │ Edge TTS │  │ Sherpa   │  │ Win SAPI │          │
│     │ (在线)    │  │ (ONNX)   │  │ (原生)    │          │
│     │ 0MB      │  │ 13MB     │  │ 0MB      │          │
│     └──────────┘  └────┬─────┘  └──────────┘          │
│                        │                                │
│                 ┌──────▼──────┐                        │
│                 │  Piper VITS │                        │
│                 │  (int8量化)  │  纯CPU, <0.1s延迟     │
│                 └─────────────┘                        │
└─────────────────────────────────────────────────────────┘
```

### 技术栈

| 层 | 技术 | 版本 | 说明 |
|----|------|------|------|
| 在线引擎 | edge-tts | latest | 微软神经网络，免费 |
| 离线引擎 | sherpa-onnx | 1.13.2 | C++ ONNX Runtime |
| 模型 | Piper VITS (int8) | - | 13MB, 中文, CPU |
| 本地引擎 | pyttsx3 (SAPI) | latest | Win原生语音 |
| 音频 | soundfile | latest | WAV 读写 |
| ORT修复 | onnxruntime | 1.26+ | 自动覆盖sherpa内置旧版DLL |

---

## 🧠 Auto-Speak 自动语音播报

开启后，每次 AI 回复自动朗读：

```
用户: 开启语音播报
→ config.json: auto_speak = true
→ 后续每次回复自动调用 TTS
→ 语音消息发送至当前聊天
```

关闭：
```
用户: 关闭语音播报 / 安静 / 别说了
→ config.json: auto_speak = false
```

一个答案只会开一次口，工具调用/系统消息不会触发朗读。

---

## 📦 安装

```bash
# 全自动安装（edge-tts + pyttsx3 + sherpa-onnx）
python scripts/install.py

# 仅安装在线引擎
python scripts/install.py --edge-only

# 仅安装离线引擎
python scripts/install.py --win-only

# 下载 sherpa-onnx 模型
python scripts/install.py --sherpa xiao_ya

# 检查安装状态
python scripts/install.py --check
```

---

## 🔧 CLI 参考

```bash
python scripts/speak.py "文本" [选项]

选项:
  --voice, -v    NAME      音色名称
  --engine, -e    ENGINE   引擎: auto / edge / sherpa / win
  --speed, -s     FLOAT    语速 (0.5-2.0, 默认 1.0)
  --output, -o    PATH     输出音频文件
  --list-voices            列出全部音色
  --set-voice     NAME     设置默认音色
  --set-speed     FLOAT    设置默认语速
  --auto-speak    on|off   开启/关闭自动语音播报
  --config                 显示当前配置
  --config-path            显示配置文件路径
```

---

## 📊 实测性能（Win 11, i7, 16GB）

| 引擎 | 模型 | 首句 | RTF | RAM |
|------|------|------|-----|-----|
| edge | xiaoxiao | 0.5s | — | 50MB |
| sherpa | xiao_ya (int8) | 0.08s | 0.05 | 200MB |
| win | huihui | 0.03s | — | 50MB |

---

## 🔧 Troubleshooting

| 问题 | 解决 |
|------|------|
| `No module named 'edge_tts'` | `pip install edge-tts` |
| `No module named 'pyttsx3'` | `pip install pyttsx3` |
| `sherpa-onnx ORT version mismatch` | 已自动修复：skills/scripts 自动覆盖旧版 ORT DLL |
| 模型未找到 | `python scripts/install.py --sherpa xiao_ya` |
| Edge TTS 超时 | 网络问题，自动降级到 sherpa/win |
| 中文 SAPI 不可用 | 安装 Windows 中文语言包 |

---

## 🆚 与现有 TTS 技能对比

| 维度 | 本技能 | qwen-tts | edge-tts | sherpa-onnx-tts |
|------|--------|----------|----------|-----------------|
| 引擎数 | **4个** | 1个 | 1个 | 1个 |
| 模型大小 | 13MB | 1.7GB | 0 | 需自行下载 |
| 中文支持 | ✅ | ✅ | ✅ | ❌(英文为主) |
| 智能降级 | ✅ | ❌ | ❌ | ❌ |
| 自动播报 | ✅ | ❌ | ❌ | ❌ |
| 离线可用 | ✅ | ✅ | ❌ | ✅ |

---

## 📝 Changelog

### v1.1.0 — 四引擎 + Sherpa打通
- **New**: Windows SAPI (pyttsx3) 本地引擎，零配置离线
- **Fix**: sherpa-onnx ORT DLL 自动覆盖（系统 1.26→覆盖sherpa内置1.17）
- **Fix**: Piper 模型 lexicon 路径显式传入
- **Change**: 引擎自动降级 edge → sherpa → win
- **New**: 6款 Edge TTS 音色（+yunyang/xiaohan）
- **New**: ORT auto-fix (_ensure_ort_fix)
- **Docs**: 2025-2026 本地轻量 CPU 中文 TTS 模型全景对比

### v1.0.0 — Initial Release
- Edge TTS + sherpa-onnx 双引擎
- 3款 Piper 中文音色 (xiao_ya/chaowen/huayan)
- 3款 Edge 中文音色 (xiaoxiao/yunxi/xiaoyi)
- Auto-speak 自动语音播报模式
- 流式 TTS 支持
- 一键安装脚本