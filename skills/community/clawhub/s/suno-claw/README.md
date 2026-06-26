# 🎵 suno-claw

**Suno AI 创意工作流 — 让 AI 替你做音乐**

一个基于 [Suno AI](https://suno.ai)（[kie.ai API](https://docs.kie.ai/)）的多代理创意工作流 skill。模拟艺术创作的发散与收敛过程，通过双轨迭代逐步产出高质量歌曲。

[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://clawhub.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## ✨ 特性

- 🧠 **多代理架构** — 主代理 + 歌词/音乐性双轨子代理，并行迭代
- 🎯 **Relevance 衰减** — 三轮发散（1.0 → 0.7 → 0.5），从精准到远距联想
- 🧊 **记忆系统** — history.json 热数据 + patterns.log 长期偏好存档
- 🎤 **渐进生成** — 每首用户确认后再生成，有效节约 API 额度
- 🌐 **中文优化** — 歌词 ≥400 字，每段 Verse/Chorus ≥4 行
- 🚫 **零容忍规则** — 歌词和风格标签中禁止出现歌手名/参考曲名

---

## 🔧 工作原理

```
用户输入 →  信息收集 + IS_INSTRUMENTAL 判断
                │
                ├── IS_INSTRUMENTAL = false ─────────────────┐
                │                                            │
                ▼                                            ▼
        ┌───────────────┐                    ┌───────────────────┐
        │  Agent A      │                    │  Agent B          │
        │  作词人        │                    │  乐评人            │
        │  × 3轮 Relevance│                   │  × 3轮 Relevance  │
        │  1.0→0.7→0.5 │                    │  1.0→0.7→0.5  │
        └───────┬───────┘                    └────────┬──────────┘
                │                                     │
                └─────────────────┬───────────────────┘
                                  ▼
                    ┌─────────────────────────┐
                    │  封包代理 (Packager)     │
                    │  → Suno Prompt × 3     │
                    └────────────┬────────────┘
                                 ▼
                    ┌─────────────────────────┐
                    │  kie.ai API 生成        │
                    │  PENDING→SUCCESS 轮询   │
                    │  → 音频 URL + 歌词      │
                    └────────────┬────────────┘
                                 │
                          用户确认? ──→ 👍 → 存档 + 结束
                                         😐 → 下一条 Prompt
```

---

## 📁 目录结构

```
suno-claw/
├── SKILL.md                  # OpenClaw skill 入口
├── ARCHITECTURE.md           # 系统架构详解
├── workflow.md               # 工作流详细说明
├── memory-system.md          # 记忆系统设计
├── prompts/
│   ├── agent-a.md            # Agent A（作词人）完整 Prompt
│   ├── agent-b.md            # Agent B（乐评人）完整 Prompt
│   ├── collector.md          # 信息收集代理
│   ├── executor-main.md      # 主代理调度逻辑
│   ├── packager.md           # Suno Prompt 封包代理
│   └── generator.md          # kie.ai API 调用指南
├── scripts/
│   ├── suno_generate.py      # 生成脚本（提交 + 轮询）
│   ├── poll_task.py          # 独立轮询脚本
│   └── check_task.py         # 单次状态查询
└── memory/
    ├── history.json          # 交互历史（热数据）
    └── patterns.log          # 偏好模式（长期记忆）
```

---

## 🚀 快速开始

### 1. 安装依赖

```bash
# 安装 OpenClaw（如果你还没有）
npm install -g openclaw

# 安装 skill
clawhub install suno-claw
```

### 2. 配置 API Key

在 OpenClaw 配置中添加环境变量：

```
KIEAI_API_KEY=your_api_key_here
```

API Key 在 [kie.ai](https://kie.ai/api-key) 获取。

### 3. 开始创作

对 OpenClaw 说：

```
制作一首西海岸 chill rap 风格的歌
生成一段放松的钢琴纯音乐
```

---

## 📖 核心概念

### Relevance 衰减

| 轮次 | Relevance | 说明 |
|:----:|:---------:|------|
| 第1轮 | 1.0 | 严格围绕原始创意，精准提炼 |
| 第2轮 | 0.7 | 适度延伸，引入关联元素，参考历史偏好 |
| 第3轮 | 0.5 | 高度发散，探索远距联想 |

### IS_INSTRUMENTAL

| 类型 | 唤醒的子代理 |
|------|------------|
| `false`（有歌词）| Agent A（歌词）+ Agent B（音乐性）并行 |
| `true`（纯音乐）| 仅 Agent B（音乐性） |

### 记忆系统

- **history.json** — 完整交互快照，超过 50 条时合并最旧 10 条到 patterns.log
- **patterns.log** — 成功标签模式压缩存档，下一轮 Round 2/3 自动注入

---

## 📝 示例

输入：
```
制作一首 Kill This Love 风格的歌曲
```

输出（示例）：
```
🎵 歌名：火焰的觉醒
🔗 试听：https://suno.com/song/xxx
📝 歌词：
[Verse 1]
...
[Chorus]
...
🎸 风格：EDM, K-pop, Energetic, Female Vocal, Synth Lead
```

---

## ⚙️ 环境变量

| 变量 | 必填 | 说明 |
|------|:----:|------|
| `KIEAI_API_KEY` | ✅ | kie.ai API 密钥 |

---

## 📄 License

MIT © [jasonzhang-zzx](https://github.com/jasonzhang-zzx)


