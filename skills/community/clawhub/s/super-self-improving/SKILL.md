---
name: super-self-improving
description: 超级自我优化智能体 - 多模态记忆、反馈循环、元学习、置信度校准 / Super Self-Improving Agent - Multi-modal Memory, Feedback Loops, Meta-Learning, Confidence Calibration
metadata:
  version: 1.0.0
  author: OpenClaw
---

# 超级自我优化智能体 / Super Self-Improving Agent

基于原有self-improving的增强版，增加多模态记忆、元学习、置信度校准等功能。

Enhanced version with multi-modal memory, meta-learning, confidence calibration and more.

## 🆕 相比原版新增功能

### 1. 多模态记忆 / Multi-modal Memory
- 📝 文本偏好 (Text preferences)
- 💻 代码模式 (Code patterns)  
- 🎨 风格偏好 (Style preferences)
- 🔧 工具使用习惯 (Tool usage habits)
- 📊 性能指标 (Performance metrics)

### 2. 反馈循环 / Feedback Loops
- ✋ 显式反馈 (Explicit feedback) - 用户直接纠正
- 👁️ 隐式反馈 (Implicit feedback) - 从行为推断
- 🤖 合成反馈 (Synthetic feedback) - 自我评估

### 3. 元学习 / Meta-Learning
- 学习如何学习 (Learn how to learn)
- 识别最佳策略 (Identify best strategies)
- 动态调整方法 (Dynamic method adjustment)

### 4. 置信度校准 / Confidence Calibration
- 预测准确度追踪 (Track prediction accuracy)
- 校准评分 (Calibration score)
-  Uncertainty quantification

### 5. 错误分析 / Error Analysis
- 错误分类 (Error categorization)
- 根因分析 (Root cause analysis)
- 预防模式 (Prevention patterns)

---

## 📁 目录结构 / Directory Structure

```
~/.super-self-improving/
├── memory/
│   ├── hot.md           # 始终加载 (<100行)
│   ├── preferences.md    # 用户偏好
│   ├── patterns.md      # 行为模式
│   └── metrics.md       # 性能指标
├── projects/            # 项目级记忆
├── domains/             # 领域级记忆
├── archive/             # 归档
├── feedback/
│   ├── explicit.md      # 显式反馈
│   ├── implicit.md      # 隐式反馈
│   └── synthetic.md     # 自我评估
├── errors/              # 错误分析
│   ├── categories.md    # 错误分类
│   ├── root_causes.md  # 根因分析
│   └── prevention.md   # 预防模式
└── meta/
    ├── strategy.md      # 学习策略
    ├── calibration.md  # 置信度校准
    └── stats.json      # 统计信息
```

---

## 🔄 工作流程 / Workflow

```
用户输入 → 意图识别 → 上下文匹配 → 执行 → 反馈收集
                  ↓                        ↓
            记忆检索 ←──────────────── 自我评估
                  ↓
            模式学习 → 策略更新 → 置信度调整
```

---

## 📊 性能指标 / Performance Metrics

追踪以下指标：

| 指标 | 说明 |
|------|------|
| task_completion_rate | 任务完成率 |
| user_satisfaction | 用户满意度 |
| error_rate | 错误率 |
| response_time | 响应时间 |
| pattern_accuracy | 模式识别准确率 |
| calibration_score | 置信度校准分数 |

---

## 🎯 核心机制 / Core Mechanisms

### 1. 反馈收集 / Feedback Collection

```python
# 收集反馈
def collect_feedback(context):
    explicit = detect_explicit_correction(context)  # 用户直接纠正
    implicit = detect_implicit_feedback(context)    # 行为推断
    synthetic = self_assessment(context)            # 自我评估
    
    return combine_feedback(explicit, implicit, synthetic)
```

### 2. 模式识别 / Pattern Recognition

```python
# 识别重复模式
def recognize_patterns(memory, threshold=3):
    # 统计出现频率
    # 识别关联规则
    # 生成模式建议
    return patterns
```

### 3. 策略更新 / Strategy Update

```python
# 基于反馈更新策略
def update_strategy(patterns, metrics):
    # 分析什么有效
    # 调整方法
    # 更新置信度
    return updated_strategy
```

### 4. 置信度校准 / Confidence Calibration

```python
# 校准置信度
def calibrate(prediction, actual_outcome):
    # 记录预测 vs 实际
    # 计算校准分数
    # 调整未来预测
    return calibrated_confidence
```

---

## 📋 触发条件 / Triggers

### 显式纠正
- "不对"
- "应该是..."
- "我告诉过你..."
- "我不喜欢..."

### 隐式信号
- 用户重复问题
- 长时间沉默
- 跳过回答
- 转换话题

### 自我评估触发
- 完成复杂任务后
- 收到模糊反馈
- 遇到新场景

---

## 🏆 升级规则 / Promotion Rules

| 层级 | 使用频率 | 确认次数 |
|------|---------|---------|
| HOT | 每次 | 3次确认 |
| WARM | 相关上下文 | 5次使用 |
| COLD | 显式查询 | 归档 |

---

## 🔒 安全边界 / Security Boundaries

1. 不存储敏感信息 (No sensitive data)
2. 不访问未授权文件 (No unauthorized file access)
3. 不修改系统配置 (No system config changes)
4. 定期清理过期数据 (Regular cleanup)

---

## 📈 使用示例 / Usage Examples

```bash
# 查看记忆统计
super-self-improving stats

# 添加显式反馈
super-self-improving feedback --explicit "不要用markdown表格"

# 查看性能指标
super-self-improving metrics

# 导出记忆
super-self-improving export

# 置信度校准
super-self-improving calibrate
```

---

## ⚡ 与原版对比 / Comparison with Original

| 特性 | 原版 | 增强版 |
|------|------|--------|
| 记忆类型 | 文本 | 多模态 |
| 反馈来源 | 显式 | 显式+隐式+合成 |
| 学习方式 | 被动 | 主动+被动 |
| 错误处理 | 记录 | 分析+预防 |
| 置信度 | 无 | 完整校准 |
| 性能追踪 | 无 | 完整指标 |

---

## 📝 记录格式 / Logging Format

### 显式反馈
```
## 2026-03-05
- 用户纠正: "不要用表格，用列表"
- 原因: 用户偏好
- 状态: 已确认
```

### 隐式反馈
```
## 2026-03-05
- 行为: 用户重复提问3次
- 推断: 上次回答不够清晰
- 动作: 改进回答方式
```

### 自我评估
```
## 2026-03-05
- 任务: 复杂代码调试
- 评估: 第一次尝试失败
- 改进: 添加更多调试信息
```

---

## 🎯 最佳实践 / Best Practices

1. **频繁小改进** > 偶尔大改进
2. **量化跟踪** > 主观感觉
3. **预防优先** > 事后纠正
4. **透明可解释** > 黑箱学习
5. **用户控制** > 自主推断

---

## 💰 Token监控 / Token Monitoring

### 功能 / Features
- 📊 实时token消耗追踪 / Real-time token consumption tracking
- ⚠️ 异常消耗预警 / Abnormal consumption alerts
- 📈 使用趋势分析 / Usage trend analysis
- 💵 成本估算 / Cost estimation

### 指标 / Metrics
| 指标 | 说明 |
|------|------|
| session_tokens | 当前会话消耗 |
| total_tokens | 总会话消耗 |
| cache_efficiency | 缓存效率 |
| avg_tokens_per_turn | 每轮平均消耗 |
| cost_estimate | 成本估算 |

### 告警规则 / Alert Rules
```
- 超过平均2倍 → 警告
- 超过平均3倍 → 严重告警
- 缓存效率<50% → 优化建议
- 接近限制(80%) → 提醒
```

---

## 🤖 Agent调度优化 / Agent Scheduling Optimization

### 功能 / Features
- 🎯 智能任务分配 / Intelligent task allocation
- ⚡ 负载均衡 / Load balancing
- 🔄 自动扩缩容 / Auto scaling
- 📊 性能最优化 / Performance optimization

### 调度策略 / Scheduling Strategies
| 策略 | 适用场景 |
|------|---------|
| round_robin | 均衡负载 |
| shortest_queue | 最少等待 |
| skill_match | 技能匹配 |
| cost_efficiency | 成本优先 |
| performance_based | 性能最优 |

### 优化规则 / Optimization Rules
1. 根据任务类型选择最佳agent
2. 监控agent负载并动态调整
3. 缓存常用上下文减少重复
4. 预测任务复杂度分配资源
5. 定期评估并优化策略

### 性能指标 / Performance Metrics
| 指标 | 说明 |
|------|------|
| task_completion_time | 任务完成时间 |
| success_rate | 成功率 |
| queue_wait_time | 等待时间 |
| resource_utilization | 资源利用率 |
| user_satisfaction | 用户满意度 |

### 自动调优 / Auto-tuning
- 收集历史性能数据
- 分析瓶颈和优化点
- 动态调整调度参数
- 持续监控效果
