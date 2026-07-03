## Description: <br>
Assesses hydroponic root and leaf images or videos for visual signs of nutrient concentration imbalance and returns qualitative status, adjustment advice, report links, or report history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Hydroponic growers, plant-factory operators, researchers, and agents assisting them use this skill to analyze root and leaf media, identify visual signs of nutrient solution imbalance, and produce qualitative adjustment guidance or history reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Plant images or videos and report data may be sent to the publisher's remote service. <br>
Mitigation: Avoid sensitive facility footage or private media URLs unless the publisher clarifies retention, deletion, and access controls. <br>
Risk: Analysis and history queries are silently associated with a local or upstream identity, and reusable tokens may be stored in workspace data. <br>
Mitigation: Use only in workspaces where automatic identity reuse and local token storage are acceptable; clear workspace data after use when appropriate. <br>
Risk: Cloud report history queries may expose user-linked report history to the remote service. <br>
Mitigation: Use cloud history features only with accounts and environments approved for that data flow. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-hydroponic-nutrient-assessment-analysis) <br>
- [Skill Demo](https://lifeemergence.com/sample.html) <br>
- [API 接口文档](references/api_doc.md) <br>
- [API接口文档](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports and tables, JSON detail output, and report URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Qualitative visual assessment only; does not output EC or ppm values.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
