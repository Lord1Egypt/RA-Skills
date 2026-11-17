## Description:

Guides an agent through recreating a single-file financial institution risk management HTML platform using PatSnap/Eureka science and technology risk data, including rating-change analysis, risk snapshots, batch inspections, quarterly warning lists, and report export flows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

External users and business developers use this skill to recreate a browser-based financial risk monitoring platform that presents PatSnap/Eureka-backed company risk signals and exportable reports. The skill is best suited for authorized enterprise risk analysis workflows where users have the required PatSnap/Eureka access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Enterprise names, credit codes, or client portfolio lists may be sent to PatSnap/Eureka MCP services during real-data workflows.

Mitigation: Use the skill only with authorized PatSnap/Eureka access and confirm that the data is approved for submission to those services.

Risk: Generated risk reports may be mistaken for final credit decisions.

Mitigation: Treat generated reports as decision-support analysis and require qualified human review before any credit, lending, or portfolio action.

Risk: Without MCP configuration or account authorization, live data retrieval may be unavailable or incomplete.

Mitigation: Complete the PatSnap/Eureka setup and verify MCP availability before relying on live-data sections.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanzhian-patsnap/skills/qiye-risk-platform)
- [PatSnap open platform](https://open.zhihuiya.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with inline implementation prompts and HTML/CSS/JavaScript requirements]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces instructions and acceptance checks for generating a single-file HTML risk platform; real-data behavior depends on authorized PatSnap/Eureka MCP access.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
