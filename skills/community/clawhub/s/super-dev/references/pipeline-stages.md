# Super Dev 9 阶段流水线详解

阶段编号 1-9，可通过 `super-dev run <编号>` 或 `super-dev run <名称>` 跳转。

## 阶段 1: Research（需求增强）

- 解析用户需求，检测场景（新功能/Bug 修复）
- 读取本地知识库 `knowledge/`
- 加载知识缓存 `output/knowledge-cache/*-knowledge-bundle.json`
- 联网研究同类产品（如果非离线模式）
- 输出: `output/*-research.md`

## 阶段 2: Docs（三份核心文档）

包含 PRD + Architecture + UIUX 三个子阶段：

- PM 专家生成 PRD: 产品愿景、目标用户、功能需求、验收标准
- ARCHITECT 专家生成架构: 技术栈选型、模块划分、API 设计、数据库建模
- UI + UX 专家生成设计规范: 设计系统、组件规范、页面蓝图、交互流程
- 输出: `output/*-prd.md`, `output/*-architecture.md`, `output/*-uiux.md`, `output/*-execution-plan.md`, `output/*-frontend-blueprint.md`

## DOC_CONFIRM_GATE（文档确认门禁）

- 三份核心文档完成后必须暂停
- 等待用户明确确认后才能继续
- 未经确认不得创建 Spec 或开始编码

## 阶段 3: Spec（任务拆解）

- 将需求拆解为可执行的 Task
- 按优先级排序，前端优先
- 输出: `.super-dev/changes/*/proposal.md` + `.super-dev/changes/*/tasks.md`

## 阶段 4: Frontend（前端实现）

- 先交付前端，做到可预览
- 运行时验证（frontend runtime validation）
- UI 质量审查
- 输出: `frontend/` 目录下的实现代码

## PREVIEW_CONFIRM_GATE（预览确认门禁）

- 前端预览完成后必须暂停
- 等待用户确认前端效果
- 确认后才继续后端实现

## 阶段 5: Backend（后端实现）

- API 开发、数据库迁移、单元测试、集成测试
- 输出: `backend/` 目录下的实现代码

## 阶段 6: Quality（红队审查 + 质量门禁）

- 红队审查: 安全 / 性能 / 架构三维度
- 质量评分: 0-100，必须达到阈值（默认 80）
- 输出: `output/*-quality-gate.md`, `output/*-redteam.md`, `output/*-ui-review.md`

## 阶段 7: Code Review（代码审查 + AI 提示词）

- 生成代码审查指南
- 生成 AI 编码提示词
- 输出: `output/*-code-review.md`, `output/*-ai-prompt.md`

## 阶段 8: Deploy（CI/CD + 迁移 + 发布演练）

- CI/CD 配置生成（GitHub/GitLab/Jenkins/Azure/Bitbucket）
- 数据库迁移脚本
- 部署修复模板
- 发布演练验证
- 输出: CI/CD 配置文件, `output/rehearsal/*-launch-rehearsal.md`

## 阶段 9: Delivery（交付包 + 就绪度检查）

- 交付证明包
- 发布就绪度检查（6 大类 34 项）
- 输出: `output/*-release-readiness.md`, `output/*-proof-pack.*`, `output/*-pipeline-metrics.json`
