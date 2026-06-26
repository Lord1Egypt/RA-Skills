---
name: triple-memory-lake
version: 1.1.0
description: Quad-layer memory system integration - unifies OpenClaw, Claude Code, and self-improving agent memories into a single knowledge lake
---

# Triple Memory Lake

基于三个记忆系统整合的统一知识湖，已升级为四层结构。

## 四层记忆系统

| Layer | 内容 | 更新频率 |
|-------|------|----------|
| L1 MEMORY.md | 铁律/人物/项目/教训 | 重大决策后 |
| L2 Daily Logs | 每日工作日志 | 每日 |
| L3 Sources+Patterns+Domain+Tools | 原始数据+提炼模式+领域知识+工具配置 | 定期同步 |
| L4 Reviews | 自审+质量评分 | 每周一/触发时 |

## 核心功能

### 1. 三源数据同步
- Claude Code JSONL → memory/sources/claude-code/
- self-improving metrics → memory/sources/self-improving/
- OpenClaw daily logs → memory/sources/mine/

### 2. 模式提炼
- 错误模式汇总 → memory/patterns/error-patterns.md
- 工作流模式 → memory/patterns/workflow-patterns.md
- 用户偏好 → memory/patterns/user-preferences.md

### 3. 知识沉淀
- 长期记忆 → MEMORY.md
- 领域知识 → memory/domain/
- 工具知识 → memory/tools/

### 4. 自省机制
- 质量评分标准 → memory/reviews/memory-quality.md
- 自审模板 → memory/reviews/self-review-template.md
- 自审报告 → memory/reviews/self-review-YYYY-MM-DD.md

## 目录结构

```
memory/
├── index.md              # 统一入口
├── MEMORY.md              # Layer 1: 长期记忆
├── YYYY-MM-DD.md          # Layer 2: 每日日志
├── sources/               # Layer 3a: 原始数据来源
│   ├── claaude-code/      # Claude Code JSONL 日志
│   ├── self-improving/    # self-improving 指标
│   └── mine/              # OpenClaw 每日日志（预留）
├── patterns/              # Layer 3b: 提炼模式
│   ├── error-patterns.md  # 错误模式汇总
│   ├── workflow-patterns.md # Captain工作流模式
│   └── user-preferences.md  # 用户行为偏好
├── domain/                # Layer 3c: 领域知识
│   ├── openclaw.md        # OpenClaw配置/铁律/调度规则
│   └── stock-system.md    # 股票分析系统详情
├── tools/                 # Layer 3d: 工具配置
│   ├── skills.md          # Skills状态一览
│   ├── git-workflow.md    # Git工作流配置
│   └── hook-system.md     # Hook系统配置
└── reviews/               # Layer 4: 自省机制
    ├── memory-quality.md   # 记忆质量评分标准
    ├── self-review-template.md # 自审报告模板
    └── self-review-YYYY-MM-DD.md # 历次自审报告
```

## 自审触发条件

满足任一即触发自审：
1. 每周一自动自审
2. MEMORY.md 超过30天未更新
3. 发现新错误模式时
4. 用户指出记忆错误时
5. 重大系统变更后（如 OpenClaw 升级）

## 质量评分

评估维度：完整性(25%) / 准确性(30%) / 时效性(25%) / 可检索性(20%)

评分：9-10优秀 / 7-8良好 / 5-6及格 / 3-4危险 / 1-2失效

## 使用方式

### 查看知识湖状态
```bash
cat memory/index.md
```

### 执行自审
```bash
# 参考 memory/reviews/self-review-template.md 生成报告
# 保存为 memory/reviews/self-review-YYYY-MM-DD.md
```

### 同步数据源
```bash
# Claude Code
cp ~/.claude/projects/*/sessions/*.jsonl memory/sources/claude-code/

# Self-improving
cp ~/.openclaw/agents/*/metrics.json memory/sources/self-improving/
```

---

_Last updated: 2026-04-03_
