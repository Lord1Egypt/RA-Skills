# 解卦 | Hexagram Interpreter

**以代码演绎象数，用推演替代断言**  
**展开可能性，而非给出结论。**

---

## 📢 这是什么？

**「解卦·象推演」** 是一个基于中国传统易学（梅花易数 + 六爻纳甲）的符号推演系统。它不是一个"算命工具"，而是一个**启发式思考助手**——帮你从卦象符号中展开多种可能性，让你自己判断。

> 不做吉凶断言，不替你做决定。只展开"可能""或许""含有…之象"。

---

## 🎯 谁可以用？在哪些平台可以用？

**任何支持 OpenClaw Skill 格式的 AI Agent 都可以使用本技能。**

包括但不限于：

| 平台/工具 | 是否兼容 | 说明 |
|-----------|---------|------|
| **WorkBuddy**（腾讯小龙虾） | ✅ | 直接安装使用 |
| **OpenClaw** | ✅ | 标准兼容 |
| **Hermes Agent** | ✅ | 支持 OpenClaw 格式 |
| **QClaw** | ✅ | 支持 OpenClaw 格式 |
| **ArcLaw** | ✅ | 支持 OpenClaw 格式 |
| **微信**（接入 AI Agent 的工具） | ✅ | 若使用的 AI 支持 OpenClaw Skill 则可安装 |
| **小红书**（AI 助手类工具） | ✅ | 同上 |
| **X / Twitter**（AI Bot 工具） | ✅ | 同上 |
| **TikTok**（AI 创作助手） | ✅ | 同上 |
| **其他 OpenClaw 兼容 Agent** | ✅ | 只要支持 OpenClaw Skill 格式均可 |

简而言之：**如果你用的 AI 助手支持安装 Skill/技能，并且兼容 OpenClaw 标准，就能用这个。**

---

## ⚡ 30 秒快速安装

### 方式一：通过 ClawHub（推荐，最简单）

1. 打开你的 AI Agent 工具的 Skill/技能 管理页面
2. 搜索 **"sitiantai-xiangtuie"** 或 **"解卦"**
3. 点击安装
4. 或者直接访问链接：https://clawhub.ai/skills/sitiantai-xiangtuie
5. 点击 **Install** 按钮

### 方式二：CLI 命令（技术用户）

```bash
# 使用 OpenClaw CLI 安装
openclaw skills install sitiantai-xiangtuie

# 或使用 ClawHub CLI
clawhub skill install sitiantai-xiangtuie
```

---

## 🗣️ 怎么用？直接跟 AI 说这些话

安装后，在对话中直接说以下**触发词**，AI 就能自动启动解卦推演：

**中文触发词：**
> 解卦、算一卦、问卦、卜问、分析这事、推演一下、象推演、四象合参

**英文/其他语言触发词：**
> divination, iching, hexagram reading, symbolic deduction, lecture d'hexagramme, adivinación, lectura de hexagramas

### 完整对话示例

> **你：** 算一卦，帮我看一下最近的事业发展
>
> **AI（推演师）：**
> 📅 时间确认：2026年5月17日 12:44（当前时间）
> 🔍 事项确认：事业发展
> 👁 外应：无
>
> [开始推演…]
> 📋 **卦象总览**
> 本卦：风天小畜（巽上乾下）
> 变爻：第3爻
> ...
>
> 💡 **启发提问：**
> - 在工作中有没有遇到需要耐心积累的瓶颈？
> - 当前最大的阻力来自外部环境还是内部团队？

---

## ⚠️ 重要：起卦方式说明

本 Skill 支持两种起卦方式，但**进阶功能有差异**，请按你的实际情况选择：

### 🔵 方式一：日期起卦（推荐，支持进阶）

由 AI 根据当前日期自动计算卦象，无需你提供任何卦象信息。

```text
你只需说：算一卦，看看我和这个合作项目的发展
```

**支持进阶功能 ✅**：
- ✅ 可使用大六壬（时空脉络分析）
- ✅ 可使用奇门遁甲（空间方位分析）

基础推演完成后，AI 会主动询问是否启动进阶推演：
> 📊 基础推演已生成。需要更多角度吗？
>   → 想了解发展脉络？ [触发大六壬]
>   → 想了解空间方位？ [触发奇门遁甲]
>   → 已经够了

### 🟢 方式二：人工起卦（不支持进阶）

如果你已经通过其他方式得到了卦象（如掷铜钱、数字起卦、外应取卦等），可以手动输入：

```text
我掷铜钱得到了风天小畜卦，第3爻动，帮我推演一下最近的财运
```

或

```text
用数字3和8起卦，看看这次出行怎么样
```

**不支持进阶功能 ❌**：
- ❌ 无法使用大六壬
- ❌ 无法使用奇门遁甲
- 仅进行基础推演（梅花 + 六爻 + 类象展开）

> 💡 **为什么？** 六壬和奇门需要精确的日期/时间/空间数据才能计算，人工起卦时缺乏这些基础信息，无法进行准确计算。

---

## 🖥️ 专业用户配置说明

### API 集成

本系统的核心算法（旺衰精算、象展开权重、四象合参融合）通过 API 提供服务，不在此仓库中公开源码。

详见 [API.md](./API.md) 了解完整的接口文档和使用方式。

### 本地数据使用

类象知识库（`data/xiang/` 下的 28 个 JSON 文件）以 CC BY-NC-SA 4.0 许可证公开，可直接用于研究和非商业项目。使用方法：

```python
import json
import os

xiang_dir = "data/xiang"
for category in os.listdir(xiang_dir):
    for filename in os.listdir(f"{xiang_dir}/{category}"):
        with open(f"{xiang_dir}/{category}/{filename}") as f:
            data = json.load(f)
            print(f"{data['symbol']}: {data['core_properties']}")
```

### 项目结构

```
sitiantai-xiangtuie/
├── API.md                   # API 接口文档
├── data/xiang/              # 28 个类象知识库 JSON
├── skill/
│   └── SKILL.MD             # AI Skill 编排文件
├── config.json              # 技能元数据
├── SKILL.md                 # 根目录 Skill 文件
├── CHANGELOG.md             # 更新日志
├── LICENSE                  # MIT-0（框架与文档）
└── LICENSE-DATA             # CC BY-NC-SA 4.0（数据）
```

---

## 📜 许可证

| 部分 | 许可证 | 说明 |
|------|--------|------|
| `SKILL.md` / `API.md` / `README.md` / `config.json`（框架与文档） | **MIT-0** | 无需署名，极致开源，引流 |
| `data/xiang/`（类象知识库） | **CC BY-NC-SA 4.0** | 署名-非商业-相同方式共享 |
| 核心算法（旺衰精算/象展开权重/四象合参融合） | **不开源** | 仅通过 API 提供服务 |

---

## 📚 了解更多

- **GitHub 仓库**: https://github.com/henrryjoke/sitiantai-xiangtuie
- **ClawHub 页面**: https://clawhub.ai/skills/sitiantai-xiangtuie
- **更新日志**: [CHANGELOG.md](CHANGELOG.md)

---

**观天之道，执天之行**

---

## English Version

### What is this?

**Hexagram Interpreter (Xiang Tuiye)** is a symbolic deduction system based on traditional Chinese metaphysics (Plum Blossom Numerology + Six Lines). Instead of making fortune-telling verdicts, it unfolds multiple possibilities to inspire your own judgment.

### Where can I use it?

Any AI Agent that supports the **OpenClaw Skill format**, including:

| Platform | Compatible |
|----------|-----------|
| WorkBuddy | ✅ |
| OpenClaw | ✅ |
| Hermes Agent | ✅ |
| QClaw | ✅ |
| ArcLaw | ✅ |
| WeChat AI tools | ✅ (if OpenClaw compatible) |
| Xiaohongshu AI tools | ✅ |
| X / Twitter AI Bots | ✅ |
| TikTok AI tools | ✅ |
| Other OpenClaw agents | ✅ |

### Quick Install

```bash
# Via ClawHub CLI
openclaw skills install sitiantai-xiangtuie

# Or visit: https://clawhub.ai/skills/sitiantai-xiangtuie
```

### How to Use

Say these trigger words in your conversation:

> divination, iching, hexagram reading, symbolic deduction, I Ching, lecture d'hexagramme, adivinación, lectura de hexagramas

### Important: Two Casting Methods

1. **Date-based casting (recommended)** — Just tell AI your query, it auto-computes the hexagram from current date. **Supports advanced features** (Da Liu Ren, Qi Men Dun Jia).

2. **Manual casting** — If you already have a hexagram (coin toss, numbers, external signs), describe it to AI. **No advanced features** (Liu Ren / Qi Men not supported due to missing temporal data).

### License

| Part | License | Note |
|------|---------|------|
| Framework & Docs (`SKILL.md`, `API.md`, etc.) | **MIT-0** | Open source, no attribution required |
| Data (`data/xiang/`) | **CC BY-NC-SA 4.0** | Attribution-NonCommercial-ShareAlike |
| Core algorithms | **Proprietary** | API only, not open source |

---

## 💬 反馈 / Feedback

你的反馈对改进系统至关重要！

### 为什么需要你的反馈？

**"读象"功能的准确性依赖于对各类卦象、符号、情境的理解。** 你提供的每一个类象信息，都会帮助我们：
1. 识别当前算法的盲点
2. 扩充类象数据库
3. 改进解读逻辑的准确性

**你的反馈将直接提升系统的解读质量，让所有用户受益！**

### 如何提供反馈？

点击以下链接，选择合适的模板提交反馈：

| 反馈类型 | 链接 | 说明 |
|---------|------|------|
| **🐛 Bug 报告** | [提交 Bug](https://github.com/henrryjoke/sitiantai-xiangtuie/issues/new?template=bug_report.md) | 报告错误或异常行为 |
| **✨ 功能请求** | [建议功能](https://github.com/henrryjoke/sitiantai-xiangtuie/issues/new?template=feature_request.md) | 建议新功能或改进 |
| **💬 使用反馈** | [提供反馈](https://github.com/henrryjoke/sitiantai-xiangtuie/issues/new?template=feedback.md) | 提供使用体验、类象信息等 |

### 🌟 重点：提供类象信息

如果你发现"读象"功能的解读不够准确，**请提供以下信息**（在任意 Issue 模板中均有引导）：

```
输入的卦象/符号：
系统返回的解读结果：
你期望的准确解读：
该类象的其他相关信息（背景/上下文/类似案例）：
```

**为什么这很重要？**
- 每个类象信息都会直接用于训练和改进算法
- 你的反馈将帮助系统更好地理解类似场景
- 这是提升"读象"准确性的最直接方式

---
