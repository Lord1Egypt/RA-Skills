## Description:

查询指定亚马逊 ASIN 的流量关键词，以及搜索量、自然及广告排名、流量占比和 PPC 竞价参考。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

电商卖家和分析人员使用此技能反查亚马逊商品的流量来源词，对比搜索需求、自然及广告排名与 PPC 竞价参考。

### Deployment Geography for Use:

Global (supported Amazon marketplaces: US, JP, UK, DE, FR, IT, ES, CA, IN, MX, BR, AU, AE)

## Known Risks and Mitigations:

Risk: Setup may install or upgrade Node.js and qhkit or change the host PATH.

Mitigation: Review installation steps before use; prefer a preinstalled, pinned qhkit version.

Risk: The skill requires a Qinghu API token for paid service calls.

Mitigation: Approve credential setup explicitly and handle the token as a secret.

Risk: Keyword lookups spend Qinghu credits, and charges may vary with the call.

Mitigation: Check the current estimate and obtain approval before making paid calls.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/autoagc/skills/qinghu-amazon-traffic-keyword)
- [qhkit package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Concise written analysis with optional tabular file for larger results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results identify marketplace and period; paid calls report Qinghu credits consumed.]

## Skill Version(s):

0.1.1 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
