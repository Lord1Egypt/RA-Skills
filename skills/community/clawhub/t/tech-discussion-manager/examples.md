# 使用示例

## 示例 1：基础讨论流程

**用户**：我们讨论一下 API 接口的设计方案

**Agent**：✅ 已创建技术讨论记录：
📝 `tech-discussions/docs/discussions/2026-05-09-API接口设计-api-design.md`

请开始讨论，我会实时记录要点和决策。

**用户**：我觉得应该用 RESTful，因为我们团队熟悉，而且前端对接方便。但 GraphQL 的灵活性更好...

**Agent**：（更新讨论文件，记录要点：RESTful vs GraphQL 的权衡）

**用户**：还是 RESTful 吧，简单够用就行

**Agent**：（记录决策结论）

**用户**：讨论结束

**Agent**：
✅ 讨论已结束，核心结论已整理。
📝 讨论文件已更新：状态 → 已完成
📋 索引已更新：`tech-discussions/docs/discussions/index.md`

---

## 示例 2：从讨论到开发的完整流程

**用户**：列出讨论

**Agent**：
📋 技术讨论索引

| 日期 | 主题 | 状态 |
|------|------|------|
| 2026-05-09 | API接口设计 | ✅已完成 |
| 2026-05-08 | 数据库选型 | ✅已完成 |

**用户**：生成决策

**Agent**：✅ 决策文档已生成：`tech-discussions/docs/decisions/api-design-decision.md`

**用户**：生成架构

**Agent**：✅ 架构文档已生成：`tech-discussions/docs/architecture/api-design-architecture.md`

**用户**：开始开发

**Agent**：
📋 已完成讨论：
1. [2026-05-09] API接口设计
2. [2026-05-08] 数据库选型
请选择要开发的讨论（输入序号）：

**用户**：1

**Agent**：
✅ 开发规划已生成：`tech-discussions/docs/dev-plans/api-design-plan.md`
📂 代码目录已创建：`tech-discussions/code-output/api-design/`

---

## 示例 3：版本记录（有 Git）

**用户**：记录版本

**Agent**：请提供版本号（例如 v1.0.0）：

**用户**：v1.0.0

**Agent**：请提供版本说明：

**用户**：初始版本，完成核心 API 接口

**Agent**：
✅ 版本 v1.0.0 已记录
🌿 `[版本] v1.0.0 - 初始版本，完成核心 API 接口`
🏷️ Git tag: v1.0.0
