# Phase 1: Design & Contracts

**前提条件**：research.md 完成

## 设计工作流程

### 1. 从功能规范中提取实体 → data-model.md
   - 实体名称、字段、关系
   - 来自需求的验证规则
   - 状态转换（如适用）

### 2. 根据功能需求生成 API 契约
   - 对于每个用户操作 → 端点
   - 使用标准 REST/GraphQL 模式
   - 将 OpenAPI/GraphQL 模式输出到 `/contracts/`

### 3. 代理上下文更新
   - 运行 `.specify/scripts/powershell/update-agent-context.ps1 -AgentType claude`
   - 这些脚本检测正在使用哪个 AI 代理
   - 更新适当的代理特定上下文文件
   - 仅添加来自当前计划的新技术
   - 在标记之间保留手动添加的内容

**输出**：data-model.md、/contracts/*、quickstart.md、代理特定文件