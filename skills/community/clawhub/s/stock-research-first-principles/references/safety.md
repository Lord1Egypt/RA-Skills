# Safety and Communication / 安全与沟通

## Research-only boundary / 仅研究边界

- Never place, prepare, transmit, or simulate an executable broker order. / 不得下达、准备、传输或模拟可执行的券商订单。
- Never request credentials, cookies, account numbers, portfolio values, or private broker data. / 不得索取凭证、Cookie、账户号码、组合市值或私人券商数据。
- Never use private, reverse-engineered, or undocumented broker endpoints. / 不得使用私有、逆向工程或未公开文档化的券商端点。
- Never convert a recommendation into quantity, amount, order type, limit price, or broker payload. / 不得把建议转换为数量、金额、订单类型、限价或券商载荷。

## Required communication / 必需沟通内容

Every completed output must state: / 每份完整输出必须说明：

- it is general research and not personalized investment advice; / 内容属于一般研究，而非个性化投资建议；
- market and fundamental data may be delayed, incomplete, revised, or wrong; / 市场和基本面数据可能延迟、不完整、被修订或错误；
- past performance does not predict future results; / 历史表现不能预测未来结果；
- investing can result in partial or total loss of capital; / 投资可能造成部分或全部本金损失；
- the reader must independently verify material facts and suitability. / 读者必须独立核验重要事实及适用性。

## Conflicts and persuasion / 利益冲突与说服边界

- Ask for disclosure of material holdings, compensation, sponsorship, or issuer relationships when relevant to publication. / 当内容面向发布时，应要求披露重要持仓、报酬、赞助或发行人关系。
- Do not use urgency, guaranteed-return language, fear of missing out, or social-proof pressure. / 不得使用紧迫感、保证收益、错失恐惧或社会证明压力。
- Do not conceal contrary evidence or uncertainty. / 不得隐瞒反向证据或不确定性。
- Separate facts, estimates, assumptions, and opinions visibly. / 明确区分事实、预测、假设和观点。

## Fail-closed conditions / 保守失败条件

Return `watch` or `insufficient evidence` when any material gate is missing: / 任一重要门禁缺失时，返回 `watch` 或 `insufficient evidence`：

- no dated primary source for a decisive claim; / 决定性主张缺少带日期的一手来源；
- no defensible valuation or scenario range; / 缺少可辩护的估值或情景区间；
- unresolved source conflicts; / 来源冲突尚未解决；
- stale price, financial, guidance, or consensus data; / 价格、财务、指引或一致预期数据陈旧；
- missing downside, invalidation, or direct negative evidence review. / 缺少下行风险、失效条件或直接负面证据检查。
