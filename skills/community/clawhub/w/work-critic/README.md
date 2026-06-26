# Work Critic — 评委式批评助手
# Work Critic — Reviewer-in-AI

> 在重要工作定稿前，以评委视角主动挑刺。
> Get your work critiqued by a simulated expert reviewer before it goes public.

## 是什么 / What It Is

Work Critic 是一个 AI 助手 skill，专门在重要作品交出去之前做一次"模拟评委"审查。

Work Critic is an AI agent skill that simulates an expert reviewer — finding the weakest points in your work before real critics do.

不只是语法检查或润色——它会站在评委/教授/审稿人的角度，**主动找出最容易被攻击的弱点**，让你在面对真实质询之前就有准备。

It goes beyond grammar or polish: it puts itself in the shoes of a professor, reviewer, or committee member to **find the most attackable weaknesses** — so you're prepared before the real questioning begins.

---

## 适用场景 / Use Cases

| 场景 / Scenario | 说明 / Description |
|----------------|-------------------|
| 🎤 面试 PPT / 学术演示 | 博士面试、会议演讲、课题组汇报 |
| 📄 留学申请材料 | PS、SOP、CV 等申请文书 |
| 📋 研究计划 | Proposal / Research Statement |
| 💻 代码 / 技术方案 | Architecture, RTL, 算法设计 |
| 📝 任何重要工作 | 交出去之前想获得建设性批评 |

---

## 触发方式 / How to Trigger

```
请评委审查 [你的工作内容]
请批评
挑刺
弱点在哪里？
哪里会被攻击？

"review my work before I submit it"
"critique this presentation from a reviewer's perspective"
```

---

## 工作方式 / How It Works

1. **接收背景** — 告诉 AI 你的工作是什么、受众是谁
2. **系统审查** — 从 6 个维度打分批评（目标匹配度、逻辑严谨性、证据充分性等）
3. **结构化输出** — 🔴严重 / 🟡中等 / 🟢可优化，三级分层
4. **模拟提问** — 给出 3-5 个真实评委最可能追问的问题
5. **最终一句话** — 最需要记住的核心建议

---

## 示例输出 / Sample Output

```
## 🎯 评委审查报告
**被审查内容**：PhD 面试 PPT
**整体评分**：6.5/10

---

### 🔴 严重弱点（必须处理）
1. 缺乏量化对比数据  →  评委第一反应是"效果如何证明"  →  建议加柱状图
2. 相关工作引用不足  →  无法回答"和 LoRA 区别在哪"  →  补充 Related Work 页

### 🟡 中等问题（建议处理）
- 开场缺钩子，难留第一印象
- 结尾没有明确 Takeaway

---

### 🎤 如果我是评委，我会问...
1. "压缩到 rank 32 时 PPL 涨了多少？"
2. "你这篇 ICCAD 审稿意见怎么样了？"
3. "和 LoRA 的核心区别是什么？"

### 📌 评委对你说的最后一句话
> 你有方向匹配度，但目前缺乏 Evidence 证明你有能力完成这个研究。
```

---

## 安装 / Installation

```bash
# via clawhub
clawhub install work-critic

# via skillhub
skillhub install work-critic
```

---

## 文件结构 / File Structure

```
work-critic/
├── SKILL.md   # 核心 Skill 定义（AI 使用 / For AI agent）
└── README.md  # 本文件（人类阅读 / For human readers）
```

---

## 设计理念 / Design Philosophy

| 原则 / Principle | 说明 / Description |
|-----------------|-------------------|
| 🔴 问题优先 | 先说问题，正面评价留到最后 / Critique first, praise later |
| 🎯 攻击最弱点 | 找"一被问就倒"的关键 / Find the one thing that collapses under pressure |
| 📋 结构化可操作 | 每个问题有：描述 + 危险性 + 改进建议 / Every issue: what, why, how to fix |
| 🗣️ 模拟真实评委 | 问题要像真实评审会问的 / Questions must sound like real reviewers, not generic |

---

*好的作品不是没有问题，而是知道自己哪里有问题，并且有应对。*
*Great work isn't work without problems — it's work that knows its problems and has answers ready.*
