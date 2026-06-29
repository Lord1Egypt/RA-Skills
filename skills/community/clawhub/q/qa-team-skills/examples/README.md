# 示例目录

> 所有示例均来自真实测试场景（脱敏处理），展示每个指令的完整输入输出。

## 示例索引

| 示例 | 指令 | 场景 | 亮点 |
|------|------|------|------|
| [prd-demo.md](./prd-demo.md) | `/qa-prd` | 订单改价功能需求评审 | 11 维度扫描 + 业务分层建议 |
| [login-demo.md](./login-demo.md) | `/qa-case` | 登录功能用例设计 | 35 条用例，6 类型 × 9 方法 × 3 业务层 |
| [case-demo.md](./case-demo.md) | `/qa-case` | 订单改价功能用例设计 | 评审问题→用例自动转化 |
| [agent-demo.md](./agent-demo.md) | `/qa-agent` | 智能客服 Agent 测试 | 16 维度覆盖，含 RAG + 幻觉 + 偷懒 |
| [bug-demo.md](./bug-demo.md) | `/qa-bug` | 支付超时缺陷分析 | 不达标被驳回 → 补全 → 根因分析 + 批量 |
| [report-demo.md](./report-demo.md) | `/qa-report` | 三段话 → 日报/周报 | 演示非结构化输入的自动提取 |
| [team-demo.md](./team-demo.md) | `/qa-team` | 迭代末团队管理 | 进度看板 + 缺陷趋势 + 成员产出 + 准出 |

## 快速场景速查

| 你想做什么 | 看哪个示例 |
|-----------|-----------|
| 评审一份 PRD，找问题 | [prd-demo.md](./prd-demo.md) |
| 设计测试用例，覆盖全面 | [login-demo.md](./login-demo.md) |
| 拿到评审问题，转化为用例 | [case-demo.md](./case-demo.md) |
| 测试一个 AI 智能体产品 | [agent-demo.md](./agent-demo.md) |
| 分析一个 Bug 的根因 | [bug-demo.md](./bug-demo.md) |
| 写今天的工作日报 | [report-demo.md](./report-demo.md) |
| 作为测试经理看团队全局 | [team-demo.md](./team-demo.md) |

## 示例结构

每个示例包含三个部分：

```
## 原始输入        ← 用户实际输入了什么
## AI 输出         ← AI 返回了什么（完整、未删减）
## 使用技巧        ← 这个场景下的最佳实践
```

所有示例均可直接复制输入部分到 Claude Code 中验证输出效果。
