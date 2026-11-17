# Data Quality and Provenance / 数据质量与溯源

## Source tiers / 来源分级

1. Primary: regulator filings, issuer releases, audited statements, official transcripts, and official statistical sources. / 一级：监管文件、发行人公告、审计财报、官方电话会文本和官方统计来源。
2. Direct structured providers: licensed or documented market-data services with clear timestamps and fields. / 二级：具有明确时间戳和字段定义的持牌或文档化结构化市场数据服务。
3. Reputable secondary analysis: established research or journalism that links primary evidence. / 三级：能够链接一手证据的可信研究或新闻分析。
4. Discovery-only signals: search snippets, social posts, rumors, technical patterns, and options-flow discussion. / 四级：搜索摘要、社交帖子、传闻、技术形态和期权流讨论，仅用于发现线索。

Do not let a lower tier overrule stronger direct evidence without explaining the conflict. / 未解释冲突时，不得让低等级来源推翻更强的直接证据。

## Minimum provenance fields / 最低溯源字段

For each material datapoint capture: / 每个重要数据点应记录：

- publisher and source URL; / 发布方和来源 URL；
- publication time and retrieval time; / 发布时间和获取时间；
- fiscal or market period covered; / 覆盖的财务或市场期间；
- timezone and market session when relevant; / 相关时区和市场交易时段；
- raw versus derived status; / 原始或派生状态；
- transformation, formula, or adjustment policy for derived values. / 派生值的转换、公式或复权政策。

## Freshness gates / 时效性门禁

- Label price data with market session and as-of time; never call an undated value “latest.” / 价格数据必须标明交易时段和截至时间；不得把无日期数值称为“最新”。
- Match financial statements, guidance, consensus, and valuation inputs to explicit periods. / 财务报表、指引、一致预期和估值输入必须匹配明确期间。
- Recheck event-sensitive facts after earnings, guidance, financing, regulatory, or corporate-action events. / 财报、指引、融资、监管或公司行动发生后，应重新核验事件敏感事实。
- Downgrade confidence when a source cannot be refreshed or independently checked. / 来源无法刷新或独立核验时，应降低置信度。

## Conflict handling / 冲突处理

Show conflicting values side by side, identify likely causes such as period, currency, adjustment, or update lag, and state which value is used and why. / 并列展示冲突数值，识别期间、币种、调整方式或更新延迟等可能原因，并说明采用哪个数值及其理由。

Never silently average incompatible data. / 不得静默平均不可比数据。
