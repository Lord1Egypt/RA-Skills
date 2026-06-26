# 🧠 Token Tracker 智能模型推荐系统

## 📊 功能概述

Token Tracker 现在支持智能模型推荐系统，可以根据任务复杂度、使用场景、模型性价比等维度，自动推荐最优模型使用方案，帮助您节省 token 费用。

## ✨ 核心功能

### 1. 多模型实时追踪
- 自动追踪所有使用模型的 token 消耗
- 计算每个模型的成本、使用频率、平均消耗
- 实时更新模型统计信息

### 2. 智能模型推荐
根据以下维度自动推荐：
- **任务复杂度**：简单/中等/复杂/非常复杂
- **使用场景**：简单查询、代码生成、数据分析等
- **模型性价比**：成本/性能平衡
- **历史使用数据**：基于实际使用情况分析

### 3. 成本优化分析
- 分析当前所有模型的成本分布
- 计算优化后的预计节省
- 提供具体的优化建议

## 🚀 使用方法

### 命令行界面

#### 1. 查看模型分析报告
```bash
# 查看详细的模型分析报告
token-tracker models
# 或使用 npm script
npm run token:models
```

报告内容包括：
- 📊 所有模型的使用统计
- 📈 任务复杂度分析
- 💰 成本优化分析
- 🎯 使用场景推荐
- 💡 模型使用建议

#### 2. 根据任务复杂度推荐模型
```bash
# 推荐100 tokens任务的模型
token-tracker recommend 100

# 推荐500 tokens任务的模型
token-tracker recommend 500

# 推荐1000 tokens任务的模型
token-tracker recommend 1000
```

示例输出：
```
🎯 模型推荐
==================================================
任务: 100 tokens
首选模型: zai/glm-4.7-flash
备选模型: zai/glm-4.7
推荐理由: 简单任务（100 tokens），使用成本最低的模型可节省 55%
预期节省: 55%
价格对比: zai/glm-4.7-flash: $0.0004/M < zai/glm-4.7: $0.0009/M (便宜 55%)
```

#### 3. 根据使用场景推荐模型
```bash
# 根据场景推荐（支持中文场景名）
token-tracker recommend 100 simple-query
token-tracker recommend 500 code-generation
token-tracker recommend 1000 data-analysis
token-tracker recommend 500 text-creation
token-tracker recommend 100 translation
token-tracker recommend 500 summarization
token-tracker recommend 200 question-answering
token-tracker recommend 500 complex-reasoning
```

#### 4. 分析成本优化空间
```bash
# 查看成本优化建议
token-tracker optimize
# 或使用 npm script
npm run token:optimize
```

示例输出：
```
💰 成本优化分析
==================================================
当前总成本: $0.0123
优化后成本: $0.0055
预计节省: $0.0068 (55%)
每月节省: $0.204

💡 优化建议：
1. 优先使用 zai/glm-4.7-flash
   可节省 55%
```

### 交互式菜单

启动交互式菜单，新增选项：

```
📊 Token Tracker 交互式菜单
==================================================
1. 📅 今日统计
2. 📆 本周统计
3. 📊 累计统计
4. 📜 历史记录
5. 💡 节省建议
6. 📤 导出数据
7. 📈 趋势分析
8. 🔔 定时提醒
9. 🚀 Web 仪表板
10. 🧠 模型分析
11. 🎯 模型推荐
12. 💰 成本优化
0. 🚪 退出
==================================================
请输入选项 (0-12):
```

选择 **10. 🧠 模型分析** - 查看详细的分析报告
选择 **11. 🎯 模型推荐** - 根据任务推荐模型
选择 **12. 💰 成本优化** - 查看成本优化建议

## 📋 模型价格配置

当前支持的模型及价格（每百万 token）：

| 模型 | 输入价格 ($/1M) | 输出价格 ($/1M) | 平均价 ($/1M) | 等级 |
|------|----------------|----------------|--------------|------|
| zai/glm-4.7-flash | $0.0001 | $0.0003 | $0.0004 | 高效 |
| zai/glm-4.7 | $0.0003 | $0.0006 | $0.0009 | 标准 |
| zai/glm-4.7-pro | $0.0006 | $0.0012 | $0.0018 | 高级 |
| gpt-4 | $0.03 | $0.06 | $0.045 | 企业 |
| gpt-3.5-turbo | $0.0005 | $0.0015 | $0.0010 | 经济 |
| claude-3-opus | $0.015 | $0.075 | $0.045 | 高级 |
| claude-3-sonnet | $0.003 | $0.015 | $0.009 | 平衡 |
| unknown | $0.001 | $0.002 | $0.0015 | 默认 |

## 🎯 使用场景推荐

| 场景 | 首选模型 | 备选模型 | 预期节省 |
|------|---------|---------|---------|
| 简单查询 | zai/glm-4.7-flash | zai/glm-4.7 | 55% |
| 代码生成 | zai/glm-4.7 | zai/glm-4.7-pro | 30% |
| 数据分析 | zai/glm-4.7-pro | zai/glm-4.7 | 15% |
| 文本创作 | zai/glm-4.7 | zai/glm-4.7-pro | 30% |
| 翻译 | zai/glm-4.7-flash | zai/glm-4.7 | 55% |
| 总结 | zai/glm-4.7-flash | zai/glm-4.7 | 55% |
| 问答 | zai/glm-4.7 | zai/glm-4.7-flash | 30% |
| 复杂推理 | gpt-4 | claude-3-opus | 0% |

## 💡 使用建议

### 1. 根据任务复杂度选择
```bash
# 简单任务（<100 tokens）
token-tracker recommend 50
# 推荐：zai/glm-4.7-flash

# 中等任务（100-1000 tokens）
token-tracker recommend 500
# 推荐：zai/glm-4.7

# 复杂任务（1000-10000 tokens）
token-tracker recommend 5000
# 推荐：zai/glm-4.7-pro

# 非常复杂（>10000 tokens）
token-tracker recommend 20000
# 推荐：gpt-4
```

### 2. 根据使用场景选择
```bash
# 每次查询前先查看推荐
token-tracker recommend <tokens> <scenario>

# 示例
token-tracker recommend 200 simple-query
token-tracker recommend 1000 code-generation
token-tracker recommend 3000 data-analysis
```

### 3. 定期查看成本优化
```bash
# 每周查看一次成本优化建议
token-tracker optimize
```

### 4. 结合历史数据分析
```bash
# 查看模型分析报告
token-tracker models
# 了解哪些模型使用最多，哪些最省钱
```

## 📈 预期节省效果

基于当前配置，预期节省效果：

| 场景 | 当前成本 | 优化后成本 | 节省 | 节省率 |
|------|---------|-----------|------|--------|
| 100% 简单任务 | $0.04 | $0.018 | $0.022 | 55% |
| 100% 中等任务 | $0.09 | $0.063 | $0.027 | 30% |
| 100% 复杂任务 | $0.18 | $0.153 | $0.027 | 15% |
| 混合使用（50/50） | $0.115 | $0.0605 | $0.0545 | 47% |

## 🔧 高级用法

### 自定义场景推荐
如果需要自定义场景，可以修改 `smart-model-recommender.ts` 中的 `getScenarioRecommendation` 方法：

```typescript
const customRecommendation = {
  primaryModel: 'your-model',
  fallbackModel: 'your-fallback-model',
  reason: '自定义推荐理由',
  expectedSavings: 50,
  costPerTokenComparison: '价格对比信息'
};
```

### 扩展模型价格配置
在 `MODEL_PRICES` 中添加新的模型：

```typescript
const MODEL_PRICES = {
  'your-model': {
    inputPrice: 0.0001,
    outputPrice: 0.0002,
    name: 'your-model',
    tier: 'your-tier'
  },
  // ... 其他模型
};
```

### 导出分析报告
```bash
# 查看报告后，可以保存到文件
token-tracker models > model-analysis.txt
token-tracker optimize > cost-optimization.txt
```

## 📚 相关命令

| 命令 | 说明 |
|------|------|
| `token-tracker models` | 查看模型分析报告 |
| `token-tracker recommend [tokens] [scenario]` | 推荐模型 |
| `token-tracker optimize` | 成本优化分析 |
| `token-tracker today` | 今日统计 |
| `token-tracker week` | 本周统计 |
| `token-tracker total` | 累计统计 |
| `token-tracker history` | 历史记录 |

## 🎓 最佳实践

1. **养成习惯**：每次使用前先查看推荐
2. **定期检查**：每周查看一次成本优化建议
3. **记录分析**：保存分析报告，跟踪优化效果
4. **灵活调整**：根据实际效果调整模型选择策略
5. **持续学习**：通过历史数据了解自己的使用习惯

## 📝 注意事项

1. 模型价格是假设值，实际价格可能有所不同
2. 推荐基于历史数据，数据越多推荐越准确
3. 复杂任务建议使用更强模型以保证质量
4. 不要过度优化，平衡成本和质量
5. 定期更新模型价格配置

---

**版本**：v2.1.0+
**更新日期**：2026-03-25
**维护者**：OpenClaw-CN 社区
