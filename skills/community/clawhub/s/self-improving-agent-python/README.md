# Self-Improving Agent

让 Agent 具备自我评估、学习和迭代的能力。

## 简介

Agent 不应该只是执行任务，还应该从执行中学习，不断优化自己的表现。

三层自我改进机制：
1. **实时反馈循环** - 每次任务执行后立即评估
2. **周期性深度反思** - 定期深度分析，识别系统性问题
3. **跨 Agent 经验共享** - 所有 Agent 共享学习成果

## 评分机制

```
总分 = 完成度(30%) + 效率(20%) + 质量(30%) + 满意度(20%)
```

| 分数 | 等级 | 行动 |
|------|------|------|
| ≥90 | 优秀 | 记录最佳实践 |
| 80-89 | 良好 | 继续保持 |
| 70-79 | 及格 | 识别改进点 |
| <70 | 不及格 | 触发深度反思 |

## 安装

```bash
# 克隆到 WorkBuddy skills 目录
git clone https://github.com/Brandon114/self-improving-agent_python.git ~/.workbuddy/skills/self-improving-agent
```

或手动复制到 `~/.workbuddy/skills/self-improving-agent/`

## 使用方法

```bash
# 1. 评估任务执行
python scripts/evaluate_task.py \
    --agent-id "my-agent" \
    --task-id "task-001" \
    --task-type "内容创作" \
    --completion 90 \
    --efficiency 85 \
    --quality 80 \
    --satisfaction 85

# 2. 记录经验教训
python scripts/learn_lesson.py \
    --agent-id "my-agent" \
    --lesson "验证链接有效性" \
    --impact "high" \
    --category "quality"

# 3. 分析并生成优化计划
python scripts/optimize_agent.py --agent-id "my-agent"

# 4. 跨 Agent 同步学习
python scripts/sync_learning.py
```

## 数据存储

数据保存在工作区目录 `{workspace}/self-improvement/`：

| 文件 | 说明 |
|------|------|
| evaluations.json | 任务评估记录 |
| lessons-learned.json | 经验教训库 |
| optimization-plan.json | 优化计划 |
| collective-wisdom.json | 共享知识库 |

## 适用平台

- **Python 版本**: macOS / Linux / Windows (WSL)
- **PowerShell 版本**: Windows (OpenClaw)

---

MIT License
