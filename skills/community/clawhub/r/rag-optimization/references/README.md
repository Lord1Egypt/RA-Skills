# RAG检索优化技能

> 一套完整的RAG系统优化方案，涵盖17+种优化策略

## 技能信息

- **名称**: RAG检索优化
- **版本**: 1.0.0
- **适用领域**: RAG系统开发、知识库问答、搜索引擎优化
- **前置技能**: embedding, knowledge, llm

## 核心能力

### ✅ 已覆盖的优化策略

| 类别 | 策略 | 效果提升 | 实现难度 |
|------|------|---------|---------|
| 分块优化 | 语义分块 | 0.30→0.50 | ⭐⭐ |
| 分块优化 | 由小到大检索 | 0.30→0.85 | ⭐⭐ |
| 检索优化 | 混合检索 | +0.33 | ⭐⭐ |
| 检索优化 | HyDE | +0.15 | ⭐ |
| 检索优化 | 多跳检索 | 支持复杂问题 | ⭐⭐⭐ |
| 排序优化 | 重排序 | +0.20 | ⭐⭐ |
| 后处理 | 上下文压缩 | 节省token | ⭐⭐ |
| 后处理 | 引用溯源 | 提升可信度 | ⭐ |
| 架构优化 | Graph RAG | 支持推理 | ⭐⭐⭐⭐ |
| 架构优化 | 分层路由 | 多知识库支持 | ⭐⭐⭐ |

### ✅ 提供的能力

- 📊 **诊断工具**: 快速识别RAG系统问题
- 🔧 **实现代码**: 每种策略的完整Python实现
- ⚙️ **配置模板**: 开箱即用的配置文件
- 📈 **评估框架**: 系统化的评估指标和方法
- 🎯 **决策指南**: 策略选择决策树

## 快速开始

```python
# 1. 查看快速入门指南
# quickstart.md

# 2. 使用配置模板
# config-template.json

# 3. 运行评估
python evaluate.py --test-data test-cases-example.json
```

## 文件结构

```
rag-optimization/
├── skill.md              # 完整技能文档（核心）
├── quickstart.md         # 5分钟快速入门
├── config-template.json  # 配置模板
├── evaluate.py           # 评估脚本
├── test-cases-example.json  # 测试用例示例
└── README.md             # 本文件
```

## 推荐使用顺序

1. **新手**: 先看 `quickstart.md`，了解基础概念
2. **开发**: 阅读 `skill.md`，选择适合的策略实现
3. **配置**: 参考 `config-template.json` 调整参数
4. **评估**: 使用 `evaluate.py` 验证效果

## 核心建议

> 如果只能选一个策略，**由小到大检索**是性价比最高的升级

```
准确率提升: 0.30 → 0.85
实现复杂度: ⭐⭐
推荐优先级: 🥇
```

## 发布与部署

详见 [DEPLOYMENT.md](./DEPLOYMENT.md)，包括：

- **快速使用**：直接引用文档
- **项目集成**：Python/Next.js集成示例
- **发布到平台**：打包发布流程
- **Git发布**：版本标签管理

### 快速开始

```bash
# 1. 查看文档
cat skill.md

# 2. 运行评估示例
python evaluate.py --test-data test-cases-example.json

# 3. 复制配置到你的项目
cp config-template.json your-project/
```

---

## 相关资源

- **相关技能**: embedding技能、knowledge技能、llm技能
- **推荐工具**: Ragas、TruLens、LlamaIndex
- **论文**: [RAG原始论文](https://arxiv.org/abs/2005.11401)

---

*版本: 1.0.0 | 持续更新中，欢迎反馈优化建议*
