# 写入路由规则

写入 `.sage` 前，先判断信息类型、确认程度和未来复用价值。

除非用户明确指定其他位置，本文所有路径都以 `$HOME/.sage/` 为根目录。`sage-mirror/` 只用于工作区浏览，写入仍回到 `$HOME/.sage/`。

## 总原则

1. **不确定先入 inbox**：未经确认的信息写入 `inbox/capture.md` 或 `inbox/unresolved.md`。
2. **多维信息拆开写**：一个回答可能同时更新团队、产品、流程和待办。
3. **少写但写准**：不要保存所有聊天，只保存会影响未来判断的信息。
4. **敏感信息谨慎**：联系方式、客户隐私、财务账户、密码、密钥默认不写入。
5. **更新后保持索引可用**：重大变化要同步更新 `INDEX.md` 的摘要或最近更新。

## 路由表

| 用户信息类型 | 写入位置 |
| :--- | :--- |
| 公司名称、定位、核心业务 | `~/.sage/company_profile/basic_info.md`，必要时更新 `~/.sage/INDEX.md` |
| 品牌调性、Logo、标准色、对外表达 | `company_profile/brand_assets.md` |
| 发展历程、重要节点 | `company_profile/history.md` |
| 团队名单、人员变动 | `team_and_roles/roster.csv` + `team_and_roles/org_chart.md` |
| 岗位职责、协作关系、评价标准 | `team_and_roles/role_definitions/` |
| 产品/服务、报价、交付边界 | `products_and_services/catalog.md` 或 `specific_products/` |
| 日常制度、会议、文件管理、报销 | `operations_and_workflows/daily_operations.md` |
| 核心业务流程、项目交付 SOP | `operations_and_workflows/workflows/` |
| 重大决策 | `memory_and_insights/recent_decisions.md` |
| 未关闭问题、后续跟进、风险提醒 | `memory_and_insights/open_loops.md` |
| 会议纪要 | `memory_and_insights/meeting_summaries/` |
| 周回顾 | `memory_and_insights/weekly_reviews/` |
| Agent 观察到的长期模式 | `memory_and_insights/agent_insights.md` |
| 临时想法、待整理材料 | `inbox/capture.md` |
| 冲突信息、需要用户确认的问题 | `inbox/unresolved.md` |

## 决策记录格式

写入 `memory_and_insights/recent_decisions.md` 时使用：

```markdown
### YYYY-MM-DD - 决策标题

- **决策内容**：
- **背景**：
- **考虑过的选项**：
- **为什么这样决定**：
- **影响范围**：
- **后续复盘时间**：
```

## Open Loop 格式

写入 `memory_and_insights/open_loops.md` 时尽量包含：

- 事项是什么
- 为什么重要
- 负责人是谁，如果已知
- 何时需要回看
- 当前状态

## 晋升规则

从 `inbox/capture.md` 晋升到正式文件前，至少满足一个条件：

- 用户明确确认。
- 同一信息在多次对话中重复出现。
- 它会影响未来决策、流程或协作。
- 它是已经发生的事实，而不是临时设想。

## 写入动作协议

写入前先决定动作类型：

| 动作 | 使用场景 | 要求 |
| :--- | :--- | :--- |
| 追加 | 新增一条决策、会议纪要、open loop、历史节点 | 保留原内容，在对应小节追加日期和摘要 |
| 更新 | 公司摘要、团队规模、当前目标、流程状态发生变化 | 修改当前事实，并尽量保留必要背景 |
| 归档 | 信息过期但未来可能需要追溯 | 移到“历史 / 已关闭 / 已归档”区域，不直接删除 |
| 拆分 | 单个文件开始承载过多内容 | 新建更具体文件，并在 `INDEX.md` 或相关导航中登记 |
| 待确认 | 信息来源不稳、冲突或只是猜测 | 写入 `inbox/unresolved.md`，列出需要确认的问题 |

## 写入元信息

重要条目尽量带上：

- 日期：`YYYY-MM-DD`
- 来源：用户确认 / 对话推断 / 会议纪要 / 外部材料
- 置信度：低 / 中 / 高
- 状态：草稿 / 已确认 / 已关闭 / 已归档

示例：

```markdown
- 2026-05-11｜来源：用户确认｜置信度：高｜状态：已确认
  团队当前最主要瓶颈是项目排期不可视化，导致创始人需要频繁手动协调。
```

## 冲突处理

当新信息与已有档案冲突时：

1. 不要直接覆盖原事实。
2. 在 `inbox/unresolved.md` 记录冲突点、两个版本、来源和待确认问题。
3. 向用户提出一个明确确认问题。
4. 用户确认后，再更新正式文件。
