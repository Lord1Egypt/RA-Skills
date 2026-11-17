## Description:

Analyzes smart construction technologies for bridges, tunnels, and highways using patent, academic, web, exhibition, and commercialization evidence, then helps agents produce structured HTML and Word reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Infrastructure analysts, technology intelligence teams, and agents use this skill to plan and produce source-backed research on smart construction technologies, including patent layouts, academic activity, competitor positions, engineering cases, and trend judgments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled Word generator can be mistaken for live analysis because it is a static sample/template.

Mitigation: Use the Word generator only after the agent has run the described searches and inserted source-backed findings.

Risk: Without PatSnap MCP authorization, the skill cannot retrieve live patent or paper evidence.

Mitigation: Enable and authorize the PatSnap MCP tools before relying on database-backed conclusions; otherwise use the skill only as an analysis framework.

Risk: Technology claims, counts, and negative conclusions may be misleading if they are not backed by fresh evidence.

Mitigation: Require source labels for core conclusions, quote matched totals from tool outputs, and avoid negative conclusions unless full pagination or equivalent coverage has been verified.

## Reference(s):

- [Smart Construction Analysis Framework](references/analysis_framework.md)
- [PatSnap Open Platform](https://open.zhihuiya.com/)
- [ClawHub Skill Page](https://clawhub.ai/yuanzhian-patsnap/skills/smart-construction-analysis)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Chinese-language analysis guidance with HTML report content and python-docx Word report generation instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PatSnap MCP authorization for live patent and paper retrieval; the bundled Word generator should be treated as a static template unless fresh, source-backed findings are added.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
