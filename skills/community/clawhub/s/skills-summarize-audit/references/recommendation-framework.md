# 技能/插件推荐操作

先解决用户现有工具的实际问题，再考虑新候选。推荐是证据支持的建议，不执行安装或修复。

## 决策顺序

1. 从用户请求、项目画像和可归因事件确认需求。兴趣、名称提及与真实调用分开。
2. 检查来源、重复、版本、冲突、依赖、运行证据与用户画像；没有证据不判“僵尸”。
3. 对缺口经授权查询 GitHub/官方文档，从 skill-marketplaces.md、mcp-marketplaces.md 发现候选。
4. 每个需求选 2–3 项，与已安装方案在相同任务、客户端、许可证及成本约束下比较。
5. 输出保留 / 升级 / 替换 / 引入 / 共存 / 归档，或“补充证据，暂不变更”；附执行 Agent、验证、回滚和状态。

“升级”需要本地版本与当前上游版本证据；“替换”需要可重复的能力差异；“归档/卸载”不能只凭低分或无日志。
首次全景、后续增量见 execution-flow.md。综合分门禁见 ecosystem-optimization.md。

## 市场取证字段

每条候选记录：source_url、license、stars、last_commit、last_release、maintenance_status、security_statement、price、price_verified、checked_at、confidence、scoring_basis。
不可得项为 null 并说明；Stars 只反映关注度，不证明质量、运行能力、活跃用户或付费意愿。
价格与许可证分别核验；目录排名和第三方宣称不能作为本机安全结论。
来源与时间逐条保留，不把旧调研数字固定在代码中。

## CLI 输入契约

--market-path 读取 JSON object，以 `skill:<id>` 或 `mcp:<server>` 为键；值包含上述字段、status=market_observed 和 0–10 的 score。
评分至少需要真实 https source_url、license、带时区且 30 天内的 checked_at、明确 scoring_basis。不能用占位 URL 填充事实。
来源内容核验由 Agent 执行，脚本只验证结构、时间与数值，不能自动认证真实性。

## 风险与作用域

每项记录 executes_local_commands、requires_network、requires_token、arbitrary_shell、offline_review、upstream_overwrite，各自给 status/value/证据。
配置声明执行命令不证明已经启动；没有 env Token 不证明不需要凭证；本地 MCP 也可能联网。
优先项目级：只服务当前仓库且证据充分。全局级：跨项目有明确用途。未知用 defer；不猜写入路径或未验证的隐藏接口。

## 行动格式

按 actions-schema.md；用 recommendation-examples.md 查看无虚构数字的输出示例。
按 P0（阻断/安全证据）→P1（修复）→P2（改进）排序，最多五项上首屏。
