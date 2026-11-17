# Seedancer v10.0.3 — AI Film Director Operating System

<p align="center">
  <a href="README.md"><b>English</b></a> · <a href="docs/README-cn.md">中文</a>
</p>

<div align="center">

**From Script to Screen — End-to-End AI Film Production Pipeline**

[![Version](https://img.shields.io/badge/version-10.0.3-blue.svg)](https://github.com/taosiuman/seedancer/releases)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE)

[![Seedance](https://img.shields.io/badge/Seedance-2.5-purple.svg)](https://seedance.ai)

**[Quick Start](#quick-start)** · **[Core Modules](#core-modules)** · **[Examples](#examples)** · **[Changelog](CHANGELOG.md)**

</div>

---

## 🎬 Overview

**Seedancer** is not a prompt generator. It is a **director-grade AI film production operating system** — a complete workflow engine that transforms scripts into production-ready video prompts through **12 quality gates**, **10 core modules**, and **48 reference documents**.

### ✨ What's New in v10.0.3

**硬门可机算**——合并 [PR #1](https://github.com/taosiuman/seedancer/pull/1)：台词容量、分组时长、镜头密度 Smin 从模型心算改为可执行计算器，并补上 CI（详见 `CHANGELOG.md`）。

| 变化 | 说明 |
|------|------|
| 🧮 **硬门计算器** | `scripts/seedancer_calc.py`：`smin` / `dialogue` / `check-group` / `models`，退出码 0/1/2 |
| 🛠 **SKILL.sh** | 解析时长与画幅；超 15s 预警；`--help`；计算子命令委托给计算器 |
| ✅ **CI** | push / PR 跑一致性检查、攻击测试、单元测试、SKILL.sh 冒烟 |
| 📝 **入口修正** | 运镜三要素口径统一、景别↔焦段改为参考、补第六判定「换模式」、时间片不留空档、阶段数 6→8 |

### 📜 历史：What's New in v9.0.0

**结构重构版（MAJOR）**——不改创作语义，改的是"规范怎么被机器守住"：

| 变化 | 说明 |
|------|------|
| 📋 **参考文档加载表** | 门控 → 必须加载的文件，取代旧索引；48 篇全部接线（v8 有 15 篇从未被入口引用） |
| 🔍 **一致性检查器** | `scripts/check_consistency.py`：版本 / 元数据 / 死链 / 索引 / 接线 / 重复 / 硬门按节 / **关键小节内容行** / **规范枚举顺序** / **文件内指针层级**，**现版 19 项断言**（实测；含 `A2`/`A3`/`A4`）。逐步状态输出到 stderr（`[RUN ]`），中断可见断点 |
| ⚖️ **合规修复** | LICENSE 归因从 4 个来源补全到 8 个（此前 SKILL.md 声称"完整归因见 LICENSE"并不成立） |
| 🧹 **入口去重** | SKILL.md 瘦身：v8 记录 **56,037 字节** → v9.0.0 发布时 **43,243 字节** → 当前 **43,678 字节**（实测 2026-10-06，含 D7 的 5→2 重写，比 D7 前 **+78 字节**）；删的是与 references 重复的内容，硬门逐字保留 |
| 🎯 **版本单一权威** | `_meta.json` 为唯一来源，其余 **9 处**版本戳由检查器 `V1` 断言守护（此前 6 处漂移） |

v8.0.0 的五大导演系统仍在，详述见各 reference（见《参考文档加载表》）。

---

##  Core Modules

### Pre-Production Pipeline (P0–P2)

| Phase | Output |
|-------|--------|
| **P0** Project Intake | Project baseline card |
| **P0A** 10-Point Script Analysis | World bible + character bios + emotion curve |
| **P1** Creative Baseline | Camera/color/sound bible |
| **P2a** Character Assets | 9:16 confirmation + 16:9 concept board |
| **P2b** Key Props | 3:4 prop master template |

### Five Hard Gates (v6.0.0)

Rigorous constraints ensuring prompt executability:

- **Dialogue Capacity Check** — Speaking rate × punctuation pauses × reaction beats
- **Group Hard Gate** — Model duration cap + continuity equation + scene-end stability
- **Shot Density Gates (×4)** — Smin / Bmin / new feedback / Gmax thresholds
- **Camera Design System** — Narrative function table + 3-element camera axis
- **Output Format Gate** — Natural paragraph style + pronoun ban + media translation table

### Five Director Systems (v7.0.0)

####  Scene Prototype Router

Auto-classifies scenes into 9 archetypes with independent camera focus and spatial dynamics:

- **Action**: Chase → Confrontation → Impact
- **General**: Journey → Atmosphere → Revelation  
- **Dialogue**: Standoff → Interrogation → Negotiation

#### 📷 Camera-Emotion Sync

The camera is the emotional avatar of the focal character:

| Emotion | Camera Type | Effect |
|---------|-------------|--------|
| Anger / Tension | Handheld, unstable | Visible breathing drift |
| Calm / Control | Handheld, smooth | Minimal rhythmic micro-movement |
| Sadness / Vulnerability | Handheld, slow low-angle | Slowed breathing, slight descent |
| Shock / Revelation | Locked + slow push/pull | Strict stillness → 0.5s delay → imperceptible move |
| Action | 60fps 180° shutter | Fluid motion, motion blur within shutter angle |
| Final Shot | Overhead freeze-frame | Strict top-down, 0.3–0.5s freeze |

#### 🎬 Performance Micro-Beat Catalog

**Doctrine**: Abstract emotion = bad prompt. Specific muscle/breath/eye = good prompt.

| Emotion | Micro-Beats |
|---------|-------------|
| Anger | Masseter pulsing, carotid pulse, nostril flare, pupil constriction |
| Anxiety | Laryngeal swallow, short pre-line breath, lip moistening |
| Sadness | Outer eye corner droop, moisture band with catch light, no tears |
| Shock | 0.3–0.5s body freeze, pupil dilation, delayed sharp nasal inhale |

Every line: pre-beat (swallow/inhale) + mid emphasis + post-beat (0.5s gaze hold).

#### 💡 Lighting Rules

**Practicals-only doctrine** — only light sources physically present in the scene:

- Camera always on the character's shadow side
- 60:30:10 color ratio — primary / secondary / accent
- Atmospheric haze throughout; no god rays
- Scene-specific clauses: night / underground / day-ext / night-ext / warm interior

#### 📋 JSON API Output Mode

Structured bilingual JSON for automation:

```json
[
  {"lang": "en", "prompt": "Style & Mood: ...\nNarrative: ...\nDynamic: ...\nStatic: ...\nAudio: ..."},
  {"lang": "zh", "prompt": "风格与氛围：...\n叙事：...\n动态：...\n静态：...\n音频：..."}
]
```

Chinese prompt hard cap: 1800 chars. Full anti-junk vocabulary included.

### Supported Models

| Model | Type | Max Duration | Best For |
|-------|------|-------------|----------|
| Seedance 2.5 | Video | 30s | Complex action + long dialogue |
| Seedance 2.0 | Video | 15s | Cost-effective general use |
| Kling 3.0 | Video | 15s | Action + physics interaction |
| Veo 3 | Video | 8s | Short atmosphere shots |
| GPT Image 2 | Image | — | Photorealistic quality |
| Seedream 5.0 Pro | Image | — | Layer separation + commercial |

### 12-Gate Quality Routing

```
Gate 0  Pre-production detect
Gate 0A Pre-production phase
Gate 1  Intake
Gate 2  Source verification
Gate 3  Mode selection
Gate 4  Capability check
Gate 5  Reference mapping
Gate 6  Safety gate
Gate 7  Prompt construction
Gate 7A Dialogue capacity check
Gate 7B Group + density gates
Gate 8  Quality inspection
```

---

## 🚀 Quick Start

### Install

```bash
# Load SKILL.md in your OpenClaw agent
# See https://github.com/taosiuman/seedancer for details
```

### Full Production Flow

```
User: Read my script and run the full pipeline from script analysis to storyboard.

System:
1. P0  Project intake → baseline card
2. P0A 10-point script analysis → world + characters + emotion curve
3. P1  Creative baseline → camera/color/sound bible
4. P2a Character assets → 9:16 + 16:9 boards
5. P2b Key props → 3:4 master template
6. Production pipeline → 12 gates → storyboard generation
```

### Single Shot (Skip Pre-Production)

```
User: Shoot a cyberpunk rain-night street, 15s, 16:9.

System: Skip P0-P2 → Gate 1 → Scene router (Atmosphere)
        → Camera-Emotion Sync (Melancholy → Handheld slow low-angle)
        → Bilingual prompt output
```

### JSON API Automation

```bash
# Local usage example (requires agent runtime)
# Note: ClawHub API is deprecated. Use local agent invocation instead.
```

**Usage**:
- Load SKILL.md in your OpenClaw agent
- Describe your request in conversation
- Or script agent API calls (not ClawHub public API)

---

## 📁 Reference Documents (48)

```
references/
├── scene-prototypes.md          # Scene prototype router (v7)
├── camera-emotion-sync.md       # Camera-emotion sync (v7)
── performance-micro-beats.md   # Performance micro-beat catalog (v7)
├── json-api-mode.md             # JSON API output mode (v7)
├── lighting-rules.md            # Lighting rules engine (v7)
├── dialogue-capacity.md         # Dialogue capacity check
├── grouping-density.md          # Group hard gate + shot density
├── camera-design.md             # Camera design system
├── output-format.md             # Output format gate
├── story-analysis.md            # P0A 10-point script analysis
├── emotion-curve.md             # Emotion curve visualization
├── creative-baseline.md         # Creative baseline
── character-assets.md          # Character assets
├── prop-assets.md               # Key props
├── cinedance-video-prompt.md    # CINEDANCE 16-block
├── lira-image-prompt.md         # LIRA 4-D
├── acting-performance.md        # ACTING performance system
├── geo-spatial-layout.md        # GEO spatial lock
├── style-prefix.md              # Style prefix
├── ai-director.md               # AI director methodology
├── failure-codes.md             # Failure diagnostics (6 types + 5 gate codes = 38 codes)
└── ...
```

---

## 📜 Changelog Highlights

| Version | Date | Highlights |
|---------|------|-----------|
| **v10.0.3** | 2026-10-18 | 排除 Python 字节码，修复 ClawHub 安全扫描拒绝 |
| **v10.0.2** | 2026-10-18 | 硬门计算器 + SKILL.sh 实用化 + CI（合并 PR #1） |
| **v10.0.1** | 2026-10-06 | 大扫除（删死代码 + 合并重复 + 清理陈旧标记） |
| **v9.0.2** | 2026-10-06 | 元数据一致性修复（frontmatter 表述 + skill-card 漂移 + 检查器 v3） |
| **v9.0.1** | 2026-10-06 | 安全与数据边界整改（真人素材同意/留存门 + 消除规避措辞） |

完整版本历史见 [CHANGELOG.md](CHANGELOG.md)。

---

##  Acknowledgments

- **shotlist-builder** — Scene prototype router + Camera-emotion sync + Performance micro-beats
- **seedance-director** — JSON API output mode
- **hellgrind** — ACTING / CINEDANCE / LIRA
- **ifeihong/aigc-film-studio** — CINEDANCE / LIRA / ACTING / GEO / Style Prefix
- **chaoge-assets-trial** — P0-P2 pre-production pipeline
- **Elio_AIGC** — Five hard gate systems
- **Emily2040/seedance-2.0** — Model mechanics + anti-junk vocabulary

Full attribution: [LICENSE](LICENSE)

---

## 🔗 Links

**GitHub** · [taosiuman/seedancer](https://github.com/taosiuman/seedancer)  
**Issues** · [Report a bug](https://github.com/taosiuman/seedancer/issues)

---

<div align="center">

**🎬 Seedancer v10.0.3 — Where Scripts Become Frames**

*Made with ❤️ for AI filmmakers*

</div>
