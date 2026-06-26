# Self-Improvement Agent Skill

当 Agent 需要从任务执行中学习并自我优化时，激活此技能。

---

## 激活条件

用户提到以下关键词时激活：
- "自我改进"、"自我优化"、"学习经验"
- "任务评估"、"性能分析"
- "优化工作流程"、"提升效率"
- 需要 Agent 从错误中学习的场景

---

## 核心概念

Agent 不应该只是执行任务，还应该从执行中学习，不断优化自己的表现。

三层自我改进机制：
1. **Layer 1: 实时反馈循环** - 每次任务执行后立即评估
2. **Layer 2: 周期性深度反思** - 定期深度分析
3. **Layer 3: 跨 Agent 经验共享** - 共享学习成果

---

## 任务评估标准

### 评分公式

总分 = 完成度(30%) + 效率(20%) + 质量(30%) + 满意度(20%)

### 评分等级

| 分数 | 等级 | 行动 |
|------|------|------|
| ≥90 | 优秀 | 记录最佳实践 |
| 80-89 | 良好 | 继续保持 |
| 70-79 | 及格 | 识别改进点 |
| <70 | 不及格 | 触发深度反思 |

---

## 使用方法

### Python 版本（推荐）

```bash
# 评估任务
python scripts/evaluate_task.py \
    --agent-id "my-agent" \
    --task-id "task-001" \
    --task-type "内容创作" \
    --completion 90 \
    --efficiency 85 \
    --quality 80 \
    --satisfaction 85

# 记录经验
python scripts/learn_lesson.py \
    --agent-id "my-agent" \
    --lesson "验证链接有效性" \
    --impact high \
    --category quality

# 优化分析
python scripts/optimize_agent.py --agent-id "my-agent"

# 跨 Agent 同步
python scripts/sync_learning.py
```

### 参数说明

**evaluate_task.py**
| 参数 | 说明 | 必填 |
|------|------|------|
| --agent-id | Agent 标识 | 是 |
| --task-id | 任务标识 | 是 |
| --task-type | 任务类型 | 是 |
| --completion | 完成度 (0-100) | 是 |
| --efficiency | 效率 (0-100) | 是 |
| --quality | 质量 (0-100) | 是 |
| --satisfaction | 满意度 (0-100) | 是 |

**learn_lesson.py**
| 参数 | 说明 | 必填 | 可选值 |
|------|------|------|--------|
| --agent-id | Agent 标识 | 是 | |
| --lesson | 经验描述 | 是 | |
| --impact | 影响程度 | 是 | high/medium/low |
| --category | 类别 | 是 | quality/efficiency/tools/knowledge |

---

## 数据存储位置

```
{workspace}/
├── self-improvement/
│   ├── evaluations.json        # 评估记录
│   ├── lessons-learned.json   # 经验库
│   └── optimization-plan.json # 优化计划
└── shared-context/
    └── self-improvement/
        └── collective-wisdom.json  # 共享知识库
```

---

## 最佳实践

### 何时评估
- 完成重要任务后
- 完成复杂任务后
- 任务失败或返工后
- 简单重复性任务可选

### 如何记录经验
- 记录具体的失败场景
- 记录成功的关键因素
- 记录工具使用的注意事项

### 如何应用学习
- 定期回顾经验库
- 主动应用最佳实践
- 分享给其他 Agent

---

## 故障排查

| 问题 | 解决 |
|------|------|
| 找不到工作区 | 检查 config.py 中的路径配置 |
| 经验未同步 | 手动运行 sync_learning.py |
| 优化计划生成失败 | 确保有足够的历史评估数据 |

---

*让每个 Agent 都成为终身学习者！*

*Version: 1.1.0 (Python Edition)*
*Tags: agent, self-improvement, learning, optimization*
