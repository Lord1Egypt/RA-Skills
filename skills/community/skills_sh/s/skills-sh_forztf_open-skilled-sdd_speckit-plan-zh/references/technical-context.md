# 技术上下文参考

## Speckit 工作流程架构

### 组件说明
- **功能规范 (Feature Spec)**: 描述要实现的功能需求
- **实施计划 (Impl Plan)**: 结构化的实施计划和模板
- **研究阶段 (Phase 0)**: 分析技术未知项和依赖关系
- **设计阶段 (Phase 1)**: 生成数据模型和 API 契约

### 目录结构规范
```
.specify/
├── memory/
│   ├── constitution.md          # 项目章程/约束条件
│   └── agent-context/           # AI 代理上下文文件
├── scripts/
│   └── powershell/              # PowerShell 脚本
├── templates/
│   └── impl-plan.md            # 实施计划模板
├── contracts/                   # API 契约文件
├── research.md                 # 研究结果
├── data-model.md              # 数据模型
└── quickstart.md              # 快速开始指南
```

### 代理类型支持
- **Claude**: 使用 claude-context.md
- **ChatGPT**: 使用 chatgpt-context.md
- **Auto**: 自动检测环境变量 AI_AGENT_TYPE

### 关键概念
- **NEEDS CLARIFICATION**: 需要进一步澄清的技术项
- **Gate violations**: 违反项目约束条件
- **Constitution checks**: 项目章程合规性检查
- **Agent context**: AI 代理的项目特定上下文信息

## 最佳实践

1. **研究阶段**: 确保所有技术未知项得到解决
2. **设计阶段**: 遵循 REST/GraphQL 标准模式
3. **上下文管理**: 保留手动添加的内容在标记之间
4. **错误处理**: 在关键失败点抛出 ERROR
5. **文档维护**: 保持文档与实施同步