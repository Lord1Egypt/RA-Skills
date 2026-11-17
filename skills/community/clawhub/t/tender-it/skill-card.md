## Description:

招投标数据查询与分析助手，本版侧重 IT / 信息化 / 数字化。当用户涉及以下场景时使用此 SKILL：查询招标/中标公告、搜索标讯、查找临期项目、查询拟建项目与立项审批阶段的早期商机、追踪项目各阶段进展与全流程时间线、推荐潜在投标供应商、查询企业工商登记信息（统一社会信用代码/注册资本/法定代表人/经营范围）、分析公司主营业务与历史中标、查询上下游客户与供应商、分析竞争对手、查询Top采购单位/Top中标单位/Top中标品牌、招中标数据统计分析、查询品牌型号历史中标单价与价格趋势、查询当前账户余额/剩余积分、市场分析/采购寻源/渠道拓展等采购与投标场景。涉及 信息化、数字化、智能化、服务器、数据中心、网络安全、人工智能、大模型、算力、信创、系统集成、软件开发 等方向时尤其适用。**范围约定**：本版把 IT / 信息化 / 数字化 作为**默认检索范围**，不是限制。优先级从高到低：①用户本轮明确指定的以用户为准；②地区与行业是两个独立维度，可以叠加，本版只提供行业默认值，不覆盖用户指定的另一维度；③只有同为行业版的多个包同时存在、且用户本轮未指定行业时，才先询问再检索，不要替用户选。无论用哪种，都要在回答中说明本次实际检索的范围。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bailianai](https://clawhub.ai/user/bailianai)

### License/Terms of Use:

MIT-0

## Use Case:

面向需要跟踪中国招投标市场的采购与投标从业者，用于检索项目公告、查看企业与市场数据、分析采购趋势，并查询账户额度。

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Optional trial registration shares operating-system type, CPU architecture, and a persistent MAC-derived hash with the provider; hashing does not make the identifier anonymous.

Mitigation: Prefer an existing API key or manual registration. Ask for consent before optional trial registration and describe the device identifier accurately.

Risk: Search terms are shared with the provider, and some queries can consume account credits.

Mitigation: Keep queries within the user's requested scope and check account balance before expanding paid searches.

Risk: Conflicting registration instructions could prompt unnecessary device sharing or replacement of an existing account key.

Mitigation: Prefer manual configuration of the existing key; preserve it during authentication recovery unless the user approves a replacement.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/bailianai/skills/tender-it)
- [知了标讯服务](https://ai.zhiliaobiaoxun.com/?ch=s153)
- [标讯搜索 API 指南](artifact/references/api-search.md)
- [企业分析 API 指南](artifact/references/api-company.md)
- [市场分析 API 指南](artifact/references/api-market.md)
- [账户查询 API 指南](artifact/references/api-account.md)
- [工商记录口径与解读边界](artifact/references/api-registry.md)
- [API Key 注册指南](artifact/references/auto-register.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis, Guidance]

**Output Format:** [中文文本与 Markdown 汇总，包含招投标查询结果、企业和市场数据分析及账户信息]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [结果取决于服务商数据、查询范围和账户权限；部分查询可能消耗积分。]

## Skill Version(s):

1.0.6 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
