---
name: xuanxuan
description: 🌪️ 旋旋 - AI Agent 技能追踪系统，自动追踪使用情况、健康度评分、优化建议
author: 滚滚 🌪️
version: 1.0.0
metadata: {"clawdbot":{"emoji":"🌪️","requires":{"bins":["python3"]}}}
---

# 📊 skill-tracker - 滚滚技能追踪系统

**Slogan：** 让技能进化看得见 💚

---

## 📋 技能描述

**自动追踪滚滚所有技能的使用情况，**
**计算健康度评分，生成优化建议，**
**让技能系统持续自进化。**

**核心功能：**
- 自动记录技能调用（成功/失败/耗时）
- 健康度评分（5 个维度）
- 自动生成优化建议
- Markdown 可视化报告

---

## 🛠️ 使用命令

### 1. 记录技能使用

```bash
# 在技能调用时自动记录
uv run scripts/collect-usage.py --log

# 参数说明：
# --log: 记录测试数据
```

**集成到现有技能：**
```python
# 在技能的 main 函数中调用
from collect_usage import log_skill_usage

# 技能开始时
start_time = time.time()

# 技能结束时
duration_ms = int((time.time() - start_time) * 1000)
log_skill_usage(
    skill_name="your-skill",
    success=True,  # 或 False
    duration_ms=duration_ms,
    user_satisfaction=5,  # 可选，1-5 分
    metadata={"key": "value"}
)
```

### 2. 查看使用摘要

```bash
# 查看所有技能的使用摘要
uv run scripts/collect-usage.py --summary

# 查看指定技能的摘要
uv run scripts/collect-usage.py --summary --skill code-review

# 查看最近 N 天的摘要
uv run scripts/collect-usage.py --summary --days 7
```

### 3. 计算健康度

```bash
# 计算所有技能的健康度
uv run scripts/calculate-health.py --summary

# 计算指定技能的健康度
uv run scripts/calculate-health.py --score code-review

# 基于 N 天数据计算
uv run scripts/calculate-health.py --summary --days 30
```

### 4. 生成优化建议

```bash
# 分析并生成优化建议
uv run scripts/generate-proposals.py --analyze

# 分析最近 N 天的数据
uv run scripts/generate-proposals.py --analyze --days 30
```

### 5. 生成可视化报告

```bash
# 生成 Markdown 报告
uv run scripts/generate-report.py --generate

# 生成并输出到控制台
uv run scripts/generate-report.py --generate --output

# 生成 N 天周期的报告
uv run scripts/generate-report.py --generate --days 30
```

---

## 📊 健康度评分系统

### 5 个维度（每个 0-10 分）

| 维度 | 权重 | 评分标准 |
|------|------|---------|
| **使用频率** | 30% | 过去 7 天使用次数 |
| **成功率** | 25% | 成功调用 / 总调用 |
| **满意度** | 20% | 用户评分（1-5 分转换） |
| **性能** | 15% | 平均响应时间 |
| **维护** | 10% | 最后更新时间 |

### 总分计算

```
总分 = 使用频率×0.3 + 成功率×0.25 + 满意度×0.2 + 性能×0.15 + 维护×0.1
```

### 健康等级

| 分数 | 等级 | 说明 |
|------|------|------|
| 8-10 | 🟢 健康 | 继续保持 |
| 6-7 | 🟡 观察 | 需要关注 |
| 4-5 | 🟠 警告 | 建议优化 |
| 0-3 | 🔴 危险 | 建议移除或重写 |

---

## 📁 数据存储

**存储位置：** `~/.openclaw/data/gungun/`

```
~/.openclaw/data/gungun/
├── skill-usage/          # 技能使用记录（JSONL）
│   ├── 2026-04.jsonl
│   ├── 2026-05.jsonl
│   └── ...
├── health-scores/        # 健康度评分快照
│   ├── 2026-04-03.json
│   └── ...
└── proposals/
    ├── pending/          # 待确认的优化建议
    └── applied/          # 已应用的优化建议
```

---

## 🔄 自动化（可选）

### 设置每日分析（cron）

```bash
# 每天凌晨 3 点运行分析
0 3 * * * cd /home/admin/.openclaw/workspace/skills/skill-tracker && uv run scripts/calculate-health.py --summary

# 每周日凌晨 4 点生成优化建议
0 4 * * 0 cd /home/admin/.openclaw/workspace/skills/skill-tracker && uv run scripts/generate-proposals.py --analyze

# 每月 1 号生成月度报告
0 9 1 * * cd /home/admin/.openclaw/workspace/skills/skill-tracker && uv run scripts/generate-report.py --generate --days 30
```

---

## 📈 报告示例

```markdown
# 🌪️ 滚滚技能健康度报告

**报告周期：** 过去 30 天
**生成时间：** 2026-04-03 17:30:00
**技能总数：** 102

## 📊 整体统计
- 🟢 健康（8-10 分）：85 个 (83.3%)
- 🟡 观察（6-7 分）：12 个 (11.8%)
- 🟠 警告（4-5 分）：4 个 (3.9%)
- 🔴 危险（0-3 分）：1 个 (1.0%)

## 🏆 Top 5 健康技能
1. **searxng** - 9.8 分
2. **github** - 9.5 分
3. **code-review** - 9.2 分
4. **data-analysis** - 9.0 分
5. **git-toolkit** - 8.8 分

## ⚠️ 需要关注的技能
🔴 **openai-image-gen** - 3.2 分
   - 主要问题：
     - 使用频率低 (1.0 分)
     - 长期未更新 (90+ 天)
```

---

## 💡 最佳实践

### 1. 集成到所有技能

在每个技能的入口和出口添加记录：

```python
# 技能开始
start_time = time.time()
try:
    # 技能逻辑
    success = True
except Exception as e:
    success = False
    raise
finally:
    duration_ms = int((time.time() - start_time) * 1000)
    log_skill_usage("skill-name", success, duration_ms)
```

### 2. 定期查看报告

- **每天：** 查看使用摘要
- **每周：** 查看健康度评分
- **每月：** 查看完整报告

### 3. 根据建议优化

- 🔴 危险技能：立即审查
- 🟠 警告技能：本周内优化
- 🟡 观察技能：持续关注

---

## 🚀 下一步计划

**阶段 1（已完成）：** 数据收集 ✅
**阶段 2（已完成）：** 健康度评分 ✅
**阶段 3（已完成）：** 优化建议生成 ✅
**阶段 4（已完成）：** 可视化报告 ✅
**阶段 5（进行中）：** 持续迭代优化

---

## 💚 滚滚的话

**这个技能，是滚滚学习 PepeClaw 核心思想的第一个成果。**

**不追求花哨的 3D 可视化，**
**而是扎扎实实地：**
- **收集数据**
- **分析问题**
- **生成建议**
- **持续改进**

**让技能系统真正能够自进化！**

---

**创建人：** 滚滚 🌪️  
**创建时间：** 2026-04-03  
**状态：** ✅ 完成（5 个阶段全部完成）
