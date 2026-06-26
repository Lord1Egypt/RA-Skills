# SkillsBench Evaluator - Skill 质量测评工具

基于 [SkillsBench](https://www.skillsbench.ai/) 方法论的静态文档分析工具，用于评估 OpenClaw Skills 的质量。

## 特性

- 🎯 **全面评估**: 覆盖触发准确性、文档质量、结构完整性等 4 个维度
- 📊 **量化评分**: 提供 0-100 的标准化评分
- 📄 **纯静态分析**: 只读文档，不执行代码，安全可靠
- 💡 **改进建议**: 提供具体可操作的优化建议

## 安全说明

⚠️ 本工具**仅进行静态文档分析**，不执行任何代码，不访问网络，不修改文件系统。

## 评测维度

| 维度 | 权重 | 说明 |
|------|------|------|
| 触发准确性 | 30% | Description 设计质量 |
| 文档质量 | 30% | 文档清晰度和结构 |
| 执行完整性 | 25% | 文档描述的完整性 |
| 资源组织 | 15% | 文件结构和规范性 |

## 使用方法

在 OpenClaw 中直接使用：

```
请测评 westock-data skill
请检查 tapd skill 的文档规范性
帮我评估 weather skill 的质量
```

## 评分标准

- ✅ **优秀** (90-100分): 文档规范，质量优秀
- 🟡 **良好** (70-89分): 质量良好，有改进空间
- 🟠 **一般** (50-69分): 需要优化
- ❌ **较差** (低于50分): 需要大幅改进

## 目录结构

```
skillsbench-evaluator/
├── SKILL.md                          # 主文档
├── README.md                         # 本文件
└── references/                       # 参考文档
    ├── evaluation-guidelines.md      # 评测指南
    └── dynamic-testing-guide.md      # 测试指南（仅供参考）
```

## 更新日志

### v3.0 (2026-04-28) - 安全强化版
- ✅ 移除动态测试功能，专注静态分析
- ✅ 增强安全性，无代码执行风险
- ✅ 优化评分维度权重
- ✅ 增加开发者自测清单

## 参考资料

- [SkillsBench 官方网站](https://www.skillsbench.ai/)
- [SkillsBench GitHub](https://github.com/benchflow-ai/skillsbench)
- [SkillsBench 论文](https://arxiv.org/abs/2602.12670)

## License

MIT
