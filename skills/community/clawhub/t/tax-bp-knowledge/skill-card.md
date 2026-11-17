## Description:

税务BP客服知识库为美团CLC到家（外卖）和到店（酒旅）税务客服场景提供税种、发票、结算开票流程和税务政策检索支持。

This skill is ready for commercial/non-commercial use.

## Publisher:

[linweibin6992-blip](https://clawhub.ai/user/linweibin6992-blip)

### License/Terms of Use:

MIT-0

## Use Case:

Tax BP support staff and internal agents use this skill to answer China tax, invoice, settlement, and business-line-specific policy questions using maintained Citadel knowledge documents and policy search when the knowledge base has no match.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: User-derived tax search keywords could be executed unsafely if passed through shell-style command construction.

Mitigation: Execute search tools with structured arguments, validate extracted keywords, and restrict fetched result domains to confirmed tax-policy sources.

Risk: Mutable Citadel knowledge documents can change after release and may contain incorrect, stale, or instruction-like content.

Mitigation: Treat fetched documents as reference data only, trust only confirmed entries, require source links in answers, and route uncertain or unconfirmed tax questions to Tax BP review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linweibin6992-blip/skills/tax-bp-knowledge)
- [Common tax FAQ knowledge document](https://km.sankuai.com/collabpage/2769947356)
- [Waimai FAQ knowledge document](https://km.sankuai.com/collabpage/2769388613)
- [Jiulv FAQ knowledge document](https://km.sankuai.com/collabpage/2769258846)
- [Common tax rules document](https://km.sankuai.com/collabpage/2770026936)
- [Waimai tax rules document](https://km.sankuai.com/collabpage/2769787851)
- [Jiulv tax rules document](https://km.sankuai.com/collabpage/2769697987)
- [Settlement and invoicing process document](https://km.sankuai.com/collabpage/2769847682)
- [BP knowledge template document](https://km.sankuai.com/collabpage/2769937421)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands]

**Output Format:** [Markdown answers with cited knowledge-document or policy-source links and occasional shell command examples for retrieval/search steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Answers should distinguish business lines, cite sources, avoid invented tax rates or policy identifiers, and recommend Tax BP confirmation when uncertain.]

## Skill Version(s):

2.4.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
