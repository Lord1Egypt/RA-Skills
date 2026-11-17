## Description:

分析小分子结构、理化性质、作用机制、合成路线和研发风险，用于化合物档案、项目评审和药化团队信息准备。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Medicinal chemistry and small-molecule R&D teams use this skill to prepare compound dossiers, compare candidate molecules, inspect physicochemical and ADMET signals, and summarize R&D risks for project review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill evidence reports an exposed reusable API key in the instructions.

Mitigation: Remove the embedded key, rotate it before release, and require deployment-time secret configuration.

Risk: Chemistry queries are routed to an external MCP service without enough disclosure about data handling.

Mitigation: Disclose what data is sent to the service and avoid proprietary or pre-publication compounds until confidentiality and service terms are approved.

Risk: Database coverage and predicted ADMET or toxicity values may be incomplete or uncertain.

Mitigation: Label predictions clearly, cite returned sources, and require experimental or primary-source confirmation for research decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanzhian-patsnap/skills/small-molecule-rd-analysis)
- [Publisher profile](https://clawhub.ai/user/yuanzhian-patsnap)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured Markdown reports and comparison tables with source annotations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include compound identifiers, physicochemical properties, ADMET summaries, interaction findings, uncertainty notes, and database or literature references.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
