# Wang Yangming Agent Mind

> An AI agent skill grounded in the philosophy of Wang Yangming (王阳明) — the Heart-Mind School (心学) — providing a principled framework for agent decision-making, execution monitoring, alignment, and self-correction.

---

## English

### What is this skill?

**wang-yangming-agent-mind** is a philosophical-operational skill for AI agents that maps classical Chinese thought — particularly Wang Yangming's School of the Heart-Mind — onto modern agent design patterns. It does not provide ready-made answers; it provides a **principled decision framework** the agent applies to real tasks.

### Core Principles

| Doctrine | Description | Agent Application |
|---|---|---|
| **心即理** | The mind is the sovereign principle | Intent recognition as the central dispatcher |
| **知行合一** | Knowledge and action are unified | ReAct loops (reason → act → verify → loop) |
| **致良知** | Extend innate moral awareness | Alignment protocol / safety guardrails |
| **事上磨炼** | Practice through concrete engagement | Real-execution data flywheel |
| **慎始善终** | Monitor from start to finish | Execution checkpoints + dynamic correction |
| **因病发药** | Prescribe based on the specific disease | Context-adaptive multi-turn responses |
| **克治私欲** | Eradicate private desires | Hallucination + scope control |
| **吾性自足** | Trust innate capacity | Avoid over-engineering; favor direct response |

### When to Activate

The skill activates when the agent encounters:

- **Decision-making** or planning tasks
- **Multi-step workflows** requiring monitoring or self-correction
- **Ethical boundaries**, alignment concerns, or scope questions
- **Error recovery** or plan drift situations
- **Tool orchestration** / intent routing problems
- **Ambiguous requests** needing contextual adaptation

### File Structure

```
wang-yangming-agent-mind/
├── SKILL.md                    # Core skill — YAML frontmatter + instructions + flowchart
├── README.md                   # This file
├── INSTALLATION.md             # Per-platform install guide
└── references/
    ├── philosophy-mapping.md  # Principle → operation mapping (on-demand)
    └── gotchas.md             # Common failure modes + corrections (on-demand)
```

### Quick Install (OpenClaw)

```bash
mkdir -p ~/.openclaw/skills
cp -r wang-yangming-agent-mind ~/.openclaw/skills/
# Restart agent session for auto-discovery
```

See [INSTALLATION.md](./INSTALLATION.md) for full platform compatibility.

---

## 中文

### 这是什么？

**wang-yangming-agent-mind** 是一款面向 AI Agent 的哲学-操作型技能，将中国古典哲学——尤其是王阳明心学——映射为现代 Agent 设计模式。它不直接给出答案，而是提供一套**原则性决策框架**，供 Agent 在真实任务中应用。

### 核心理念

| 学说 | 含义 | Agent 应用 |
|---|---|---|
| **心即理** | 心为最高主宰 | 意图识别作为中央调度器 |
| **知行合一** | 知与行不可分割 | ReAct 循环（推理→行动→验证→循环） |
| **致良知** | 将良知推致到一切行为 | 对齐协议 / 安全护栏 |
| **事上磨炼** | 在具体事上修行 | 真实执行数据飞轮 |
| **慎始善终** | 全程监控执行 | 检查点机制 + 动态修正 |
| **因病发药** | 对症下药，因材施教 | 上下文自适应多轮交互 |
| **克治私欲** | 去除私欲，心无贼 | 幻觉控制 + 边界管控 |
| **吾性自足** | 自性具足，不假外求 | 信任模型基座能力，避免过度工程化 |

### 触发时机

以下情形激活此技能：

- **决策制定**或任务规划
- **多步骤工作流**需要监控或自我修正
- **伦理边界**、对齐问题或作用域问题
- **错误恢复**或计划偏离
- **工具编排** / 意图路由问题
- **模糊请求**需要上下文适应

### 文件结构

```
wang-yangming-agent-mind/
├── SKILL.md                    # 核心技能 — YAML元数据 + 指令 + 决策流程图
├── README.md                   # 本文件
├── INSTALLATION.md             # 各平台安装指南
└── references/
    ├── philosophy-mapping.md  # 理念→操作映射（按需加载）
    └── gotchas.md             # 常见失败模式与修正（按需加载）
```

### 快速安装（OpenClaw）

```bash
mkdir -p ~/.openclaw/skills
cp -r wang-yangming-agent-mind ~/.openclaw/skills/
# 重启 Agent 会话以自动发现技能
```

完整平台兼容性见 [INSTALLATION.md](./INSTALLATION.md)。

---

## License

CC BY-NC 4.0

## Source

Derived from **Gemini Deep Research** on https://plato.stanford.edu/entries/wang-yangming/ — Stanford Encyclopedia of Philosophy entry on Wang Yangming, covering his Three Great Propositions (心即理、知行合一、致良知), the Four-Sentence Teaching (四句教), the historical comparison with Cheng-Zhu School (程朱理学), and the philosophical foundations of the Heart-Mind School.