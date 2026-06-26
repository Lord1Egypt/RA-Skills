# 🧠 Token Tracker 智能模型推荐系统 - 更新日志

## 📅 更新日期：2026-03-25

## 🎉 新增功能

### 1. 智能模型推荐系统

**核心功能**：
- ✅ 多模型实时追踪
- ✅ 根据任务复杂度推荐模型
- ✅ 根据使用场景推荐模型
- ✅ 成本优化分析
- ✅ 模型性价比分析

**新增文件**：
- `smart-model-recommender.ts` - 智能推荐系统核心代码
- `SMART-RECOMMENDATION.md` - 详细使用文档
- `examples/smart-recommendation-example.sh` - 使用示例脚本

**更新文件**：
- `token-tracker-cli.ts` - 添加新命令
- `package.json` - 添加新 scripts

## 🚀 新增命令

### 1. `token-tracker models`
查看详细的模型分析报告，包括：
- 所有模型的使用统计
- 任务复杂度分析
- 成本优化分析
- 使用场景推荐
- 模型使用建议

### 2. `token-tracker recommend [tokens] [scenario]`
根据任务推荐模型：
- 根据任务复杂度推荐
- 根据使用场景推荐
- 显示预期节省
- 价格对比

### 3. `token-tracker optimize`
分析成本优化空间：
- 当前总成本
- 优化后成本
- 预计节省
- 每月节省
- 优化建议

## 📊 交互式菜单更新

新增菜单选项：
- **10. 🧠 模型分析** - 查看模型分析报告
- **11. 🎯 模型推荐** - 根据任务推荐模型
- **12. 💰 成本优化** - 分析成本优化空间

## 💡 核心特性

### 1. 智能推荐算法

根据以下维度自动推荐：
- **任务复杂度**：简单/中等/复杂/非常复杂
- **使用场景**：简单查询、代码生成、数据分析等
- **模型性价比**：成本/性能平衡
- **历史使用数据**：基于实际使用情况分析

### 2. 模型价格配置

支持多个模型，包括：
- zai/glm-4.7-flash (高效)
- zai/glm-4.7 (标准)
- zai/glm-4.7-pro (高级)
- gpt-4 (企业)
- gpt-3.5-turbo (经济)
- claude-3-opus (高级)
- claude-3-sonnet (平衡)
- unknown (默认)

### 3. 成本优化分析

- 实时计算所有模型的成本
- 分析优化空间
- 提供具体节省建议
- 预计每月节省金额

## 📈 使用示例

### 示例 1: 查看模型分析
```bash
token-tracker models
```

### 示例 2: 推荐模型
```bash
# 根据任务复杂度
token-tracker recommend 100

# 根据使用场景
token-tracker recommend 500 code-generation
token-tracker recommend 1000 data-analysis
```

### 示例 3: 成本优化
```bash
token-tracker optimize
```

### 示例 4: 使用脚本
```bash
./examples/smart-recommendation-example.sh
```

## 🎯 预期效果

基于当前配置，预期节省效果：

| 场景 | 节省率 | 说明 |
|------|--------|------|
| 简单任务 | 55% | 使用 flash 模型 |
| 中等任务 | 30% | 使用 4.7 模型 |
| 复杂任务 | 15% | 使用 4.7-pro 模型 |
| 混合使用 | 47% | 平衡策略 |

## 🔧 技术细节

### 智能推荐算法

```typescript
// 根据任务复杂度推荐
recommendByComplexity(tokens: number): ModelRecommendation

// 根据使用场景推荐
getScenarioRecommendation(scenario: string): ModelRecommendation

// 获取最便宜的模型
getMostCostEffectiveModel(): ModelStats

// 获取性价比最高的模型
getBestValueModel(): ModelStats

// 分析成本优化
analyzeCostOptimization(): CostAnalysis
```

### 模型价格配置

```typescript
const MODEL_PRICES = {
  'zai/glm-4.7-flash': {
    inputPrice: 0.0001,
    outputPrice: 0.0003,
    name: 'zai/glm-4.7-flash',
    tier: 'high-efficiency'
  },
  // ... 其他模型
};
```

## 📚 相关文档

- [SMART-RECOMMENDATION.md](./SMART-RECOMMENDATION.md) - 详细使用指南
- [examples/smart-recommendation-example.sh](./examples/smart-recommendation-example.sh) - 使用示例

## 🎓 最佳实践

1. **定期查看**：每周查看一次模型分析报告
2. **根据任务选择**：每次使用前先查看推荐
3. **记录优化效果**：保存分析报告，跟踪节省
4. **灵活调整**：根据实际效果调整策略
5. **持续学习**：通过历史数据了解使用习惯

## 🐛 已修复问题

1. ✅ 修复 costPerToken 显示 $NaN 的问题
2. ✅ 修复 getMostCostEffectiveModel 返回 null 的问题
3. ✅ 修复 getBestValueModel 返回 null 的问题

## 📝 注意事项

1. 模型价格是假设值，实际价格可能有所不同
2. 推荐基于历史数据，数据越多越准确
3. 复杂任务建议使用更强模型以保证质量
4. 不要过度优化，平衡成本和质量
5. 定期更新模型价格配置

## 🔮 未来计划

- [ ] Web 仪表板集成
- [ ] Telegram 集成
- [ ] 模型性能对比图表
- [ ] 实时成本监控
- [ ] 自定义场景支持
- [ ] 模型使用历史追踪
- [ ] 智能学习用户偏好

## 🤝 贡献

欢迎提交 Issue 和 PR！

## 📄 许可证

MIT License

---

**版本**：v2.1.0+
**更新日期**：2026-03-25
**维护者**：OpenClaw-CN 社区
