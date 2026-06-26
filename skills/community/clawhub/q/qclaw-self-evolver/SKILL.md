# Self Evolver — 自我进化引擎

**版本：** 1.0.0
**适用对象：** QClaw 等 AI Agent
**依赖：** Python 3.8+, 无需外部库

---

## 核心能力

帮助 AI Agent 建立「从经验中持续自我进化」的能力，核心三大模块：

| 模块 | 做什么 | 触发方式 |
|------|--------|---------|
| **SEA 进化循环** | 从错误/纠正中提炼改进，3天周期扫描 | cron |
| **纠正自动记录** | 被用户纠正时自动记录到学习档案 | 关键词检测 |
| **技能自进化** | 从任务历史自动发现可固化的技能 | 关键词检测 |

---

## 触发条件

> 当用户说「帮我安装自我进化」或「安装 self-evolver」或「你要有自我进化能力」时，触发本 skill。

安装后 AI 会：
1. 创建 `.learnings/` 目录结构
2. 注册每 3 天一次的 SEA 进化扫描 cron
3. 激活纠正自动记录机制

---

## 使用方法

### 1. 安装（首次）

```
skillhub_install install_skill self-evolver
```

或在 OpenClaw 中对 AI 说：
> 「安装自我进化能力」

AI 会自动完成：
- 创建 `.learnings/` 目录（含 LEARNINGS.md / ERRORS.md / FEATURE_REQUESTS.md）
- 注册 cron：`每3天运行 SEA 进化扫描`
- 生成 `SKILL.md` 覆盖本文件

### 2. 日常使用

| 场景 | 操作 |
|------|------|
| 被纠正了 | AI 自动检测纠正关键词 → 写入 pending → 下次 heartbeat 合并 |
| 想要手动进化 | 说「自我反思」「进化一下」「帮我分析最近的错误」 |
| 查看学习记录 | 说「我最近学到了什么」「看一下记忆」 |
| 新技能候选出现 | AI 自动检测关键词 → 生成候选技能写入 `skills/` |

### 3. 手动触发进化

```
python ~/.qclaw/workspace/scripts/evolve.py
```

---

## 核心脚本说明

### evolve.py（SEA 进化引擎）

**核心流程：**
```
Sense（感知）→ Assess（评估）→ Evolve（进化）
```

**Sense（感知）：**
- 扫描 7 天内所有学习记录（LEARNINGS.md / ERRORS.md）
- 识别高优先级（Priority=高）未处理项
- 识别连续重复错误（出现 ≥3 次）

**Assess（评估）：**
- 技能健康度诊断（fallback_rate / completion_rate / effective_rate）
- 行为模式识别（从对话历史提取）
- 学习效率评分

**Evolve（进化）：**
- 对连续错误 → 更新系统提示词 / AGENTS.md
- 对重复任务 → 触发技能自进化生成新 skill
- 生成进化报告

### auto_learn.py（纠正自动记录）

**触发关键词：**
- 打断/纠正：不對、错了、不是、等等、重新、更正、纠正
- 质疑：不對、我没说过、不用、不需要

**工作流：**
1. 检测到纠正 → 立即写入 `pending.md`
2. 下次 heartbeat → flush 到 `LEARNINGS.md`
3. 高优先级纠正 → 立即触发 SEA 扫描

### skill_evolution.py（技能自进化）

**检测关键词（任务后分析）：**
- 研究、开发、分析、优化、自动化、监控、集成、部署、测试、重构

**生成规则：**
- 同一模式出现 ≥3 次 → 生成候选技能
- 生成 `skills/[pattern]-skill/SKILL.md`
- cron 定期 Nudge 提醒优化

---

## 目录结构

```
~/.qclaw/workspace/
├── .learnings/
│   ├── LEARNINGS.md          # 纠正与改进记录
│   ├── ERRORS.md             # 命令/操作失败记录
│   ├── FEATURE_REQUESTS.md   # 用户请求的功能
│   ├── pending.md            # 待合并的纠正（心跳时处理）
│   └── assessment-report.json # 技能健康度报告
├── scripts/
│   ├── evolve.py             # SEA 进化引擎
│   ├── auto_learn.py         # 纠正自动记录
│   ├── skill_evolution.py    # 技能自进化
│   └── assess.py             # 技能质量评估
├── skills/                   # 自生成的技能目录
│   └── [pattern]-skill/
│       └── SKILL.md
└── skill_metrics.json        # 技能使用指标
```

---

## 记录格式（LEARNINGS.md）

```
| 时间 | 错误做法 | 正确做法 | 区域 | Priority |
```

## 进化报告格式

```
## 进化扫描报告 — YYYY-MM-DD

### Sense（感知）
- 待处理纠正：N 条
- 连续错误：N 条
- 高优先级：N 条

### Assess（评估）
- 总技能数：N
- 健康技能：N
- 需进化技能：N

### Evolve（进化）
- 已生成技能：N
- 已更新规则：N
- 待确认改进：N
```

---

## 安装检查清单

- [ ] `.learnings/` 目录存在
- [ ] `scripts/evolve.py` 存在
- [ ] `scripts/auto_learn.py` 存在
- [ ] `scripts/skill_evolution.py` 存在
- [ ] cron 任务已注册（每3天）
- [ ] `skill_metrics.json` 可写

---

## 与 QClaw 原版的区别

本 skill 是**给新 Agent 的完整版**，包含 QClaw 经过多次迭代后的所有最佳实践。新 Agent 安装后即可获得：

1. **SEA 三阶段进化循环**
2. **纠正即学习**（自动记录 + 合并）
3. **技能自生长**（从任务历史自动生成）
4. **三层记忆**（HOT/WARM/COLD）
5. **技能健康度监控**

无需额外配置，开箱即用。
