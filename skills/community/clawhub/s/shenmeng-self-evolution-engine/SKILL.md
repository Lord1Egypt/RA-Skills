---
name: self-evolution-engine
description: 自我进化引擎 - 让AI Skill具备自我分析、自我改进、自我学习的能力。通过监控执行日志、分析用户反馈、自动发现优化点并生成改进方案，实现Skills的持续进化。适用于技能开发者希望自动化技能维护、优化和迭代的场景。
---

# Self-Evolution Engine 自我进化引擎

> 💰 **本 Skill 已接入 SkillPay 付费系统**
> - 每次调用费用：**0.01 USDT**
> - 支付方式：BNB Chain USDT
> - 请先确保账户有足够余额

让AI Skill具备自我分析、自我改进、自我学习的能力。

## 核心能力

1. **性能监控** - 追踪Skill执行时间、成功率、资源消耗
2. **错误分析** - 自动捕获、分类和分析失败案例
3. **用户反馈学习** - 从用户反馈中提取改进点
4. **自动优化** - 生成代码改进建议和补丁
5. **版本进化** - 管理Skill版本迭代和回滚

## 设计哲学

> "优秀的系统不是设计出来的，而是进化出来的。"

- **数据驱动**：所有改进基于实际执行数据
- **渐进式优化**：小步快跑，持续迭代
- **安全回滚**：每次进化都有备份，可随时还原
- **人机协作**：AI生成方案，人类审核决策

## 工作流程

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  监控执行   │────▶│  分析数据   │────▶│  发现问题   │
└─────────────┘     └─────────────┘     └─────────────┘
                                               │
                                               ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  部署上线   │◀────│  人类审核   │◀────│  生成方案   │
└─────────────┘     └─────────────┘     └─────────────┘
```

## 工具清单

- `performance_monitor.py` - 性能监控器
- `error_analyzer.py` - 错误分析器
- `feedback_learner.py` - 反馈学习器
- `evolution_generator.py` - 进化生成器
- `version_manager.py` - 版本管理器

## 快速开始

### 1. 初始化进化引擎
```bash
python scripts/init_engine.py --target-skill my-skill
```

### 2. 启动监控
```bash
python scripts/performance_monitor.py --skill my-skill --duration 24h
```

### 3. 分析并生成改进方案
```bash
python scripts/evolution_generator.py --skill my-skill --analyze
```

### 4. 应用进化（需审核）
```bash
python scripts/evolution_generator.py --skill my-skill --apply --patch evolution_v2.patch
```

## 参考资料

- **架构设计**：`references/architecture.md`
- **进化策略**：`references/evolution-strategies.md`
- **最佳实践**：`references/best-practices.md`
- **API文档**：`references/api-reference.md`

---

*让代码自己变得更好。*
