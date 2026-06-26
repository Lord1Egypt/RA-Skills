<div align="center">

# 🦞 虾BB

### 按住 Globe 键，说话，文字出现。

**专为 Vibe Coding 设计的免费开源 macOS 语音转文字**

*Free & open-source macOS voice-to-text, built for Vibe Coding.*

[![Swift](https://img.shields.io/badge/Swift-6.2-orange?logo=swift&logoColor=white)](https://swift.org)
[![macOS](https://img.shields.io/badge/macOS-14%2B-black?logo=apple&logoColor=white)](https://www.apple.com/macos/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Binary Size](https://img.shields.io/badge/体积-280KB-blue)]()
[![Gemini](https://img.shields.io/badge/Powered%20by-Gemini%20API-4285F4?logo=google&logoColor=white)](https://ai.google.dev/)

<br>

<img src="xiabb-demo.gif" width="720" alt="虾BB 演示">

<br>

*中英文混着说，它都能搞定。*

</div>

---

## 为什么做虾BB？

如果你跟我一样每天 Vibe Coding 十个小时，你就知道一款免费、准确、开源的语音转文字有多重要。

Vibe Coding 注定你说话时会夹大量英文单词 —— "帮我把这个 component 的 onClick handler 改成 async 的" —— 标点符号和断句对 AI 理解你的需求至关重要，而许多大模型要么语言能力单一，要么在封装起来的产品里需要收费。

市面上很多语音工具想做 AI 助手、会议纪要、多人协作。**虾BB 不做这些。** 它只做一件事：你说话，文字出现在光标位置。纯粹、快速、免费。

> **虾BB = 瞎BB** —— 最好的想法，说出来的时候都像在瞎说。🦞

希望你能喜欢。欢迎提交 Pull Request 或 Issues，一起共创属于 AI 时代 Vibe Coder 的完美语音转文字工具。

---

## 竞品对比

| | **虾BB (Gemini)** | SuperWhisper | Typeless | Wispr Flow | MacWhisper |
|---|---|---|---|---|---|
| **价格** | **免费** | $8.49/月 或 $249 买断 | 免费 4000 词/周，$12/月 | $15/月 | $29 买断 |
| **免费额度** | **250 次/天** | 无 | 4000 词/周 (~27 分钟) | 无 | 有限 |
| **中英混搭** | **很好** | 一般 | 一般 | 好 | 一般 |
| **标点符号** | **完美** | 一般 | 好（AI润色） | 好 | 没有 |
| **实时预览** | **有（边说边看）** | 无 | 无 | 有 | 无 |
| **识别引擎** | **LLM（理解语义）** | Whisper ASR | 云端 ASR | 云端 ASR + LLM | Whisper ASR |
| **体积** | **280KB** | ~100MB | ~50MB | ~50MB | ~50MB |
| **内存占用** | **~38MB** | ~500MB+ | **~1GB** | ~200MB | ~4GB |
| **开源** | **是** | 否 | 否 | 否 | 否 |
| **隐私** | 音频发 Google | 本地 | 云端 | 云端（含截屏） | 本地 |
| **单次最长** | **9.5 小时** | 依赖模型 | 未知 | 未知 | 容易出错 |

**核心差异**：虾BB 用的不是传统 ASR（语音识别），而是 **Google Gemini LLM（大语言模型）**。Whisper 只做声音→文字的机械转换，不理解你在说什么。Gemini 是先听懂，再输出 —— 标点完美、错别字少、中英切换自然。更重要的是，Gemini 免费额度每天 250 次，比所有竞品都慷慨。

---

## 功能

<table>
<tr>
<td width="50%">

**🌐 Globe 键一键录音**
按住录音，松开转写+自动粘贴。一个键搞定一切。

**🔴 实时流式预览**
边说边看文字出现在 HUD 上。Gemini Live API 实时流式传输 —— 这是竞品很少有的体验。

**🌏 真正的中英混输**
"帮我 schedule a meeting" → 完美识别。Vibe Coding 必备。

</td>
<td width="50%">

**📋 自动粘贴**
文字直接出现在光标位置，任何 app 都能用。

**⚡ 280KB 极致轻量**
纯 Swift 原生。没有 Electron，没有 Python，没有 Node。

**🎙 超长录音支持**
单次最长 9.5 小时。MacWhisper 长音频经常出错，虾BB 不会。

**🆓 完全免费**
Google Gemini 免费额度，每天 250 次，对个人用户完全够。

</td>
</tr>
</table>

### 🧠 Smart Modes 智能模式

录音时按快捷键，AI 自动处理你的语音：

| 快捷键 | 模式 | 效果 |
|--------|------|------|
| `Globe + `` | 翻译 | 说中文出英文，说英文出中文，自动识别 |
| `Globe + 1` | 提示词 | 口述想法，自动生成专业 AI 提示词 |
| `Globe + 2` | 邮件 | 口述内容，自动生成格式规范的邮件 |
| `Globe + Esc` | 取消 | 丢弃录音 |

再按同一键可切换回普通听写模式。

**彩蛋：** 龙虾麦克风 HUD 悬浮窗 + 声波动画 + 识别成功弹出 🦞BB!

---

## 安装

**方式一：直接下载（推荐）**

去 [Releases](https://github.com/dyz2102/xiabb/releases) 下载 `XiaBB-v1.0.0-macOS-arm64.zip`，解压，拖到 Applications，双击打开。

已通过 Apple 公证（Notarized），不会弹 Gatekeeper 警告。

**方式二：从源码编译**

```bash
git clone https://github.com/dyz2102/xiabb.git
cd xiabb && bash install.sh
```

<details>
<summary><b>手动编译</b></summary>

```bash
xcode-select --install  # 需要 Xcode 命令行工具
cd xiabb/native && bash build.sh
open /Applications/XiaBB.app
```

要求 macOS 14+，Apple Silicon。

</details>

---

## 设置（3 步）

| 步骤 | 操作 |
|------|------|
| **1. 获取 API Key** | 免费申请：[aistudio.google.com/apikey](https://aistudio.google.com/apikey) → 保存到 `.api-key` 文件或设置环境变量 `GEMINI_API_KEY` |
| **2. 辅助功能权限** | 系统设置 → 隐私与安全性 → 辅助功能 → 添加 **Terminal.app** |
| **3. 麦克风权限** | 首次录音时系统会弹窗，点允许 |

---

## 使用方法

| 操作 | 效果 |
|------|------|
| **按住 🌐 Globe 键** | 开始录音，HUD 显示实时预览 |
| **松开 🌐 Globe 键** | 转写完成 → 复制 → 粘贴到光标位置 |
| **Globe + `** | 🔄 翻译模式（自动识别中↔英） |
| **Globe + 1** | ⚡ 生成 AI 提示词 |
| **Globe + 2** | 📧 生成邮件 |
| **Globe + Esc** | 取消录音 |
| **点击 HUD** | 复制上次结果 |
| **拖动 HUD** | 移动到任意位置 |

说话就行，不用管标点。中英文随便混着说。

---

## 技术架构

```
按住 🌐 ─── AVAudioEngine (16kHz) ──┬──> Gemini Live WebSocket
                                     │   (流式预览 → HUD 实时显示)
                                     │
松开 🌐 ─── WAV 编码 ──────────────>└──> Gemini REST API
                                          (最终准确转写)
                                               │
                                      📋 剪贴板 + ⌘V 粘贴
```

双引擎架构：说话时用 Live API 做实时预览（低延迟），松手后用 REST API 做最终转写（高准确率）。

<details>
<summary><b>配置选项</b></summary>

`.config.json`：

| 键 | 默认值 | 说明 |
|-----|---------|------|
| `lang` | `"zh"` | 界面语言（`"en"` 或 `"zh"`） |
| `min_duration` | `2.0` | 最短录音秒数（更短的会被忽略） |
| `hud_x`/`hud_y` | 屏幕居中 | HUD 位置（或直接拖动） |
| `theme` | `"lobster"` | 皮肤主题 |

环境变量：`GEMINI_API_KEY`，`XIABB_MODEL`（默认 `gemini-2.5-flash`）

</details>

<details>
<summary><b>常见问题</b></summary>

**Globe 键没反应？** → 在系统设置 → 辅助功能里添加 Terminal.app 权限。

**日志显示 "Too short"？** → 按住 Globe 键久一点，或在配置里降低 `min_duration`。

**出现繁体字？** → 自动转换简体。如果还有问题请开 Issue。

**查看日志？** → `tail -f ~/Library/Logs/XiaBB.log`

**卸载？** → `bash uninstall.sh`

</details>

---

## English

XiaBB (虾BB) is a free, open-source macOS voice-to-text tool powered by Google Gemini, built for Vibe Coding.

Hold the Globe key to speak, release to transcribe. Works seamlessly with mixed Chinese and English. Pure Swift, 280KB binary, zero dependencies.

- **Download:** [Releases](https://github.com/dyz2102/xiabb/releases)
- **API Key:** Free from [Google AI Studio](https://aistudio.google.com/apikey)
- **Requires:** macOS 14+, Apple Silicon

---

<div align="center">

**用 🦞 做的 by [dyz2102](https://github.com/dyz2102)**

MIT License · [xiabb.lol](https://xiabb.lol)

</div>
