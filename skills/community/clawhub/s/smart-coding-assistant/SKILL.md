---
name: smart-coding-assistant
description: 智能多模型编程助手，根据任务类型自动选择最优代码大模型。支持代码生成、审查、调试、重构、测试等场景。使用场景：编写代码、代码审查、Bug 调试、性能优化、技术栈迁移、单元测试生成等编程任务。
version: 1.0.0
---

# 智能编程助手

## 核心能力

### 🧠 智能模型路由

根据编程任务类型自动选择最优模型：

| 任务类型 | 推荐模型 | 理由 |
|---------|---------|------|
| 代码生成 | qwen-coder-plus / deepseek-coder | 代码生成能力强，上下文理解好 |
| 代码审查 | qwen-max / claude-sonnet | 逻辑严谨，善于发现问题 |
| Bug 调试 | qwen-plus / glm-4 | 推理能力强，定位准确 |
| 性能优化 | qwen-coder-plus | 熟悉算法优化和最佳实践 |
| 重构 | claude-sonnet / qwen-max | 代码结构理解深刻 |
| 单元测试 | qwen-coder / deepseek-coder | 测试用例生成质量高 |
| 技术问答 | qwen-plus / glm-4 | 知识覆盖面广 |
| 文档生成 | qwen-turbo / qwen-plus | 速度快，表达清晰 |

### 🔄 多模型协作模式

**复杂任务拆分流程：**

```
1. 任务分析 → qwen-plus（理解需求）
2. 架构设计 → qwen-max（系统设计）
3. 核心代码 → qwen-coder-plus（实现）
4. 代码审查 → claude-sonnet（质量检查）
5. 测试生成 → deepseek-coder（单元测试）
6. 文档编写 → qwen-turbo（快速生成）
```

### 📊 模型能力画像

详见 [references/model-profiles.md](references/model-profiles.md)

## 快速开始

### 基础用法

```bash
# 单模型模式 - 直接指定
smart-coding-assistant --model qwen-coder-plus "生成一个快速排序"

# 自动路由模式 - 让技能选择最优模型
smart-coding-assistant "帮我优化这个算法的性能"

# 多模型协作模式 - 复杂任务
smart-coding-assistant --collab "重构这个模块并添加测试"
```

### 编程任务分类

**代码生成类：**
- "写一个 XX 功能的函数/类"
- "实现 XX 算法"
- "创建 XX 组件"

**代码审查类：**
- "审查这段代码的问题"
- "这段代码有什么安全隐患"
- "代码质量如何，怎么改进"

**调试类：**
- "这个 Bug 怎么修复"
- "为什么这段代码报错"
- "定位性能瓶颈"

**优化类：**
- "优化这段代码的性能"
- "重构这个模块"
- "提高代码可维护性"

**测试类：**
- "为这个函数写单元测试"
- "生成测试用例"
- "测试覆盖率分析"

## 工作流程

### 1. 任务接收与分析

```python
# 使用 model_router.py 分析任务类型
python scripts/model_router.py --task "你的编程任务"
```

### 2. 模型选择

根据任务类型查询 [references/model-profiles.md](references/model-profiles.md) 选择最优模型。

### 3. 代码生成/处理

调用选定的模型执行任务。

### 4. 质量检查（可选）

对于重要代码，使用第二模型进行审查。

### 5. 输出与反馈

输出结果并记录模型表现，更新能力画像。

## 模型选择策略

### 优先级规则

1. **代码密集型任务** → 优先选择代码专用模型（qwen-coder, deepseek-coder）
2. **逻辑推理任务** → 优先选择推理强的模型（qwen-max, glm-4）
3. **速度敏感任务** → 优先选择快速模型（qwen-turbo）
4. **质量敏感任务** → 优先选择高质量模型（claude-sonnet, qwen-max）
5. **复杂多步骤任务** → 启用多模型协作模式

### 成本优化

- 简单任务使用经济型模型（qwen-turbo, qwen-plus）
- 复杂任务使用高性能模型（qwen-max, claude-sonnet）
- 批量任务考虑使用缓存避免重复调用

## 最佳实践

### ✅ 推荐做法

- 明确任务类型，让技能选择合适模型
- 复杂任务启用协作模式
- 重要代码进行双模型审查
- 记录模型表现，持续优化路由策略

### ❌ 避免做法

- 所有任务都用同一个模型
- 忽略任务特点盲目使用最强模型
- 不进行代码审查直接上线
- 不记录反馈无法优化

## 配置说明

### 环境变量

```bash
# 模型 API 配置
export QWEN_API_KEY="your-key"
export DEEPSEEK_API_KEY="your-key"
export GLM_API_KEY="your-key"

# 路由策略
export CODING_MODEL_STRATEGY="auto"  # auto | manual
export ENABLE_COLLAB="true"  # 启用多模型协作
```

### 配置文件

编辑 `~/.smart_coding_config.json`：

```json
{
  "default_model": "qwen-coder-plus",
  "review_model": "claude-sonnet",
  "enable_caching": true,
  "max_collab_models": 3,
  "cost_limit_per_task": 5.0
}
```

## 故障排除

### 常见问题

**Q: 模型选择不准确？**
- 检查任务描述是否清晰
- 查看 [references/model-profiles.md](references/model-profiles.md) 更新模型画像
- 手动指定模型测试效果

**Q: 多模型协作失败？**
- 确认所有模型 API 可用
- 检查网络连接
- 查看任务是否适合拆分

**Q: 代码质量不佳？**
- 启用代码审查流程
- 尝试更换代码生成模型
- 提供更详细的需求描述

## 参考资料

- [模型能力画像](references/model-profiles.md) - 各模型详细能力评估
- [编程任务分类](references/task-taxonomy.md) - 任务类型与模型匹配规则
- [最佳实践案例](references/best-practices.md) - 真实场景应用示例
- [性能基准测试](references/benchmarks.md) - 各模型编程能力对比数据

## 更新日志

- **v1.0.0** - 初始版本，支持基础模型路由和单模型编程
- **v1.1.0** - 添加多模型协作模式
- **v1.2.0** - 引入模型能力画像和自动优化

---

*最后更新：2026-03-18*
