<p align="center">
  <h1 align="center">Soul Guardian | 心灵守望者</h1>
  <p align="center">
    A persistent AI counselor for Claude Code — it remembers you, speaks your language, and keeps everything local.
    <br />
    一位住在终端里的心理咨询师，越聊越懂你。
  </p>
  <p align="center">
    <a href="#installation">Install</a> · <a href="#quick-start">Quick Start</a> · <a href="#features">Features</a> · <a href="#privacy">Privacy</a> · <a href="#license">License</a>
  </p>
</p>

---

> **Important / 重要声明**
>
> Soul Guardian is an AI-assisted psychological support tool. It is **not** a substitute for professional mental health services. If you are in crisis, please contact a qualified professional or call an emergency hotline immediately.
>
> 心灵守望者是一个 AI 辅助心理支持工具，**不能替代**专业心理咨询师或精神科医生。如果你正处于危机中，请立即联系专业人士或拨打心理援助热线。
>
> - 全国 24 小时心理援助热线：**400-161-9995**
> - 生命热线：**400-821-1215**
> - 紧急情况：**120** 或 **110**

---

## Why Soul Guardian? / 为什么需要心灵守望者？

**Every AI therapy tool today has amnesia.** You pour your heart out, close the window, and next time you're a stranger again.

**现在的 AI 心理工具都有"失忆症"。** 你倾诉了半天，关掉窗口，下次你就是个陌生人。

Soul Guardian is different. It builds a **persistent psychological profile** that grows with every conversation — your emotional patterns, family dynamics, belief systems, strengths, and goals. It picks up exactly where you left off. Every time.

心灵守望者不一样。它为你建立一份**持续成长的心理档案**——你的情绪模式、家庭关系、信念体系、优势资源和人生目标。每次对话都接续上一次。每一次。

And everything stays on your machine. No cloud. No uploads. No one sees your data but you.

而且所有数据只存在你的电脑上。没有云端，没有上传，除了你没人能看到。

---

<a id="features"></a>
## Features / 功能特性

### 🧠 Persistent Memory System / 持久记忆系统

Your counselor never forgets. A comprehensive file-based profile system stores your information locally and loads it automatically at the start of every session.

你的咨询师从不忘记。完整的本地档案系统在每次对话开始时自动加载。

```
~/.counselor/
├── core/           # 核心档案
│   ├── PROFILE.md  # 全人画像：你是谁、关注什么、有什么优势
│   ├── STATE.md    # 当前状态：最近的情绪、上次对话要点、下次方向
│   └── SAFETY.md   # 安全守护：风险评估、预警信号、保护因素
├── maps/           # 心理地图
│   ├── FAMILY.md   # 家庭关系全景：家谱图、三角关系、代际传递
│   ├── BELIEFS.md  # 信念地图：核心信念、思维陷阱、信念松动记录
│   ├── STRENGTHS.md # 优势与资源：性格优势、支持系统、充电方式
│   ├── COMPASS.md  # 生活罗盘：满意度评估、价值观、需求层次
│   ├── STORY.md    # 我的故事：生命线、转折点、问题外化、闪光时刻
│   └── GOALS.md    # 目标与行动：咨询目标、行为实验、情绪追踪
├── sessions/       # 按日期的会话记录（只写不改）
├── journal/        # 来访者日记
├── toolkit/        # 工具箱
│   └── EMERGENCY.md # 情绪急救包：呼吸法、落地法、自我对话
└── archive/        # 历史归档
```

### 🌱 Progressive Rapport Building / 渐进式建档

No intake forms. No questionnaires. Soul Guardian builds your profile through natural conversation over your first four sessions:

没有登记表，没有问卷。心灵守望者在前四次对话中通过自然交流逐步建立你的档案：

| Session / 次数 | Focus / 重点 | Files Updated / 更新的文件 |
|:---:|---|---|
| 1 | Getting to know you / 互相认识 | `PROFILE.md`, `STATE.md` |
| 2 | Your family and important people / 聊聊家人 | `FAMILY.md` |
| 3 | Life satisfaction + strengths / 生活满意度与优势 | `COMPASS.md`, `STRENGTHS.md` |
| 4+ | Your specific concerns / 深入你关注的议题 | Topic-dependent / 按话题而定 |

### 🏠 Family Systems Therapy / 家庭系统治疗

Deep family relationship analysis with structured tools:

深度家庭关系分析，提供结构化工具：

- **Family genogram** — Three-generation relationship mapping / 三代家谱图关系梳理
- **Triangle analysis** — Identifying third-party triangulation patterns / 三角关系识别
- **Unspoken family rules** — Surfacing invisible family rules / 发现"不成文规定"
- **Intergenerational transmission** — Tracing patterns passed down through generations / 代际传递模式追踪
- **Conflict scripts** — Mapping recurring conflict cycles / 反复上演的冲突剧本
- **In-law relations, parenting anxiety, eldercare pressure** / 亲属关系、育儿焦虑、养老压力

### 🔀 Multi-Modal Therapeutic Approach / 多流派融合

- **Person-Centered (Rogers)** — Unconditional positive regard, no judgment / 来访者中心：无条件积极关注
- **Narrative Therapy** — You are not the problem; the problem is the problem / 叙事疗法：你不是问题，问题才是问题
- **CBT** — Practical thinking and behavioral tools / 认知行为：实用的思维和行为工具
- **Family Systems** — Personal issues often root in family relationships / 家庭系统：个人问题往往根植于家庭关系
- **Positive Psychology** — Focus on strengths, not just problems / 积极心理学：关注优势，不只盯着问题

### 🛡️ Crisis Safety Protocol / 危机安全协议

Built-in risk detection with crisis hotline numbers, automatic safety file updates, and clear AI limitation statements.

内置风险识别，包含危机热线号码、自动更新安全档案、明确声明 AI 局限性。

### 🆘 Emotional First Aid Kit / 情绪急救包

Ready-to-use toolkit in `toolkit/EMERGENCY.md`:

- 4-7-8 breathing / 4-7-8 呼吸法
- 5-4-3-2-1 grounding / 5-4-3-2-1 落地法
- Rapid cool-down techniques / 快速降温技巧
- Self-talk scripts / 自我对话脚本

---

<a id="installation"></a>
## Installation / 安装

### 方式一：npx skills（推荐）

```bash
npx skills add taohaowei/soul-guardian -g
```

自动将技能安装到全局 `~/.claude/skills/` 目录，开箱即用。Installs the skill globally to `~/.claude/skills/`.

### 方式二：Claude Code Plugin

在 Claude Code 中执行 / Run inside Claude Code:

```
/plugin marketplace add taohaowei/soul-guardian
/plugin install soul-guardian
/reload-plugins
```

### 方式三：手动克隆 / Manual Clone

```bash
git clone https://github.com/taohaowei/soul-guardian.git
mkdir -p ~/.claude/skills
ln -s "$(pwd)/soul-guardian/skills/counselor" ~/.claude/skills/counselor
```

### 方式四：ClaHub（需先发布）

```bash
npx clawhub install soul-guardian-counselor
```

> **注意**：ClaHub 上 `soul-guardian` slug 已被占用，我们将以 `soul-guardian-counselor` 发布。
> ClaHub 安装路径为 `~/clawd/skills/`，需确保你的 Agent 扫描该路径。

### 方式五：claude-plugins.dev

```bash
npx claude-plugins skills install taohaowei/soul-guardian/counselor
```

> **注意**：claude-plugins.dev 自动索引 GitHub 仓库，可能需要等待同步。
> 如果未找到，请使用方式一或方式二。

---

<a id="quick-start"></a>
## Quick Start / 快速开始

安装完成后，在 Claude Code 中开始你的第一次咨询 / After installation, start your first session in Claude Code:

### 第一次对话 / First Session

```
> /counselor
```

Soul Guardian 会自动创建 `~/.counselor/` 目录、初始化所有模板文件，然后温暖地跟你打招呼。

Soul Guardian will create `~/.counselor/`, initialize templates, and greet you warmly.

### 直接说你想聊的 / Start with a topic

```
> /counselor 最近心情不太好
> /counselor 今天跟婆婆又吵架了
> /counselor I've been feeling really anxious about work lately
> /counselor 最近总是对孩子发火，事后又很内疚
```

你也可以不用 `/counselor` 触发——直接描述你的感受，如果已安装技能，Claude 会自动识别并加载：

You can also just describe how you feel — if the skill is installed, Claude will auto-detect and load it:

```
> 今天好烦，不想上班
> 跟家人吵架了，心里很难受
```

### 后续对话 / Subsequent Sessions

```
> /counselor
```

It loads your profile, picks up where you left off, and updates your files after the session.

它会加载你的档案、接续上次对话，并在结束后更新你的档案文件。

---

## How It Works / 工作原理

```
┌─────────────┐     ┌───────────────────────────────────────────────┐
│  You / 你    │────▶│            Soul Guardian / 心灵守望者           │
│             │     │                                               │
│  /counselor │     │  1. Load profile / 加载档案                     │
│             │     │  2. Check safety / 检查安全状态                  │
│             │     │  3. Resume context / 接续上次话题                │
│             │     │  4. Natural conversation / 自然对话              │
│             │     │  5. Update files / 更新档案                     │
│             │◀────│  6. Warm closure / 温暖收尾                     │
└─────────────┘     └───────────────────────────────────────────────┘
                                        │
                                        ▼
                              ~/.counselor/ (local only)
```

### Topic Routing / 话题路由

| You're talking about / 你在聊 | File loaded / 加载的文件 |
|---|---|
| Family, parents, spouse, in-laws, children / 家人、父母、配偶、婆媳、亲子 | `maps/FAMILY.md` |
| Thoughts, self-image / 想法、自我评价 | `maps/BELIEFS.md` |
| Strengths, support / 擅长什么、支持系统 | `maps/STRENGTHS.md` |
| Life direction, values / 人生方向、价值观 | `maps/COMPASS.md` |
| Past experiences / 过去的经历、转折点 | `maps/STORY.md` |
| Goals, plans / 目标、计划 | `maps/GOALS.md` |
| Emotional crisis / 情绪崩溃 | `toolkit/EMERGENCY.md` |

---

<a id="privacy"></a>
## Privacy / 隐私声明

**Your data never leaves your machine.**

**你的数据永远不会离开你的电脑。**

- All files stored in `~/.counselor/` on your local filesystem / 所有文件存储在本地
- No cloud storage, no remote servers, no telemetry / 没有云存储、没有远程服务器、没有遥测
- No real names recorded — only nicknames / 不记录真实姓名——只用昵称
- You own your data — delete `~/.counselor/` anytime to erase everything / 随时删除即可清除所有内容

---

## Disclaimer / 免责声明

1. **It is not a licensed therapist.** It cannot diagnose or prescribe medication. / **它不是持证咨询师。**
2. **It does not replace professional help.** / **它不能替代专业帮助。**
3. **AI has limitations.** Responses may sometimes be inaccurate. / **AI 有局限性。**
4. **Use at your own discretion.** / **请自行判断使用。**

**Crisis resources / 危机资源：**

| Resource / 资源 | Number / 号码 |
|---|---|
| 全国 24 小时心理援助热线 | 400-161-9995 |
| 北京心理危机研究与干预中心 | 010-82951332 |
| 生命热线 | 400-821-1215 |
| 紧急情况 Emergency | 120 or 110 |

---

## Contributing / 贡献指南

Contributions are welcome! You can:

- **Report issues** / 报告问题
- **Improve therapeutic techniques** / 改进咨询技术
- **Add language support** / 增加语言支持
- **Enhance safety protocols** / 增强安全协议

Please be respectful of the sensitive nature of mental health topics. Test changes thoroughly.

---

## Roadmap / 路线图

- [ ] Mood trend visualization / 情绪趋势可视化
- [ ] Structured journaling prompts / 结构化日记引导
- [ ] Export session summaries to PDF / 导出会话摘要
- [ ] Multi-language support (English, Japanese) / 多语言支持
- [ ] Psychoeducation module / 心理教育模块

---

## License / 开源协议

[MIT](LICENSE)

## Author / 作者

**taohaowei**

---

<p align="center">
  <i>
    "每个人的内心都有自愈的力量，有时候只是需要一个安全的空间去找到它。"
    <br />
    "Everyone has the power to heal within. Sometimes you just need a safe space to find it."
  </i>
</p>
