# Actions JSON Schema — Skills-Summarize-Audit v9.2.2

本格式只交接建议，不由 Audit 执行。代码实现：scripts/recommendation_contract.py。

每项必需字段：
- target / priority（P0/P1/P2）/ problem / evidence / judgment / suggested_action。
- steps：按顺序列具体步骤；来源未定位先取证，不能提前填写入命令。
- execution_agent：所需能力，不臆造宿主 Agent 名称或模型。
- verification：同目标复查与适用测试。
- rollback：实施前快照、失败恢复和复验；没有实际变更时明确未执行。
- status：默认 suggested，实际实施与验收完成后才由执行 Agent 更新。
- fact_status：observed/inferred/estimated/unavailable。
- install_scope：project/global/plugin/defer；target_path；scope_reason。
- market：source_url、license、stars、last_commit、last_release、maintenance_status、security_statement、price、price_verified、checked_at、confidence、scoring_basis。
- exposure：executes_local_commands、requires_network、requires_token、arbitrary_shell、offline_review、upstream_overwrite；各含 status/value。

evidence_urls 是外部证据 URL 的概念集合，可在 market.source_url 及 evidence 中记录。
confirmation_required 由执行 Agent 按已有用户授权判断；本报告不以建议为外部写入许可。
未知字段为 null/unavailable。禁止复制虚构包名、下载量、漏洞比例或 ROI。
