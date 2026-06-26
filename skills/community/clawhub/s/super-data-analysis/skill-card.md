## Description: <br>
Guides agents through data analysis and visualization, including metric definition, chart selection, statistical checks, and decision-ready reporting from SQL, spreadsheets, BI tools, notebooks, and exported tables. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[subaru0573](https://clawhub.ai/user/subaru0573) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and business stakeholders use this skill to turn raw or ambiguous data requests into metric contracts, rigorous analysis plans, charts, and concise decision briefs. It is suited for KPI debugging, experiment readouts, cohort and funnel analysis, anomaly reviews, executive reporting, and data quality checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The published metadata includes unrelated crypto and purchase capability tags that may overstate what the documentation-only skill does. <br>
Mitigation: Review the capability tags before release and remove tags that are not supported by the artifact behavior. <br>
Risk: Future use with real databases or sensitive exports could expose private or business-critical data if the agent is granted tools or credentials. <br>
Mitigation: Review each agent action separately before connecting to databases, handling sensitive exports, running queries, or installing related skills. <br>
Risk: Data analysis outputs can be misleading when metric definitions, sample size, confounders, or source quality are unclear. <br>
Mitigation: Use the skill's metric contract, statistical rigor checklist, caveat, and escalation guidance before presenting conclusions or recommendations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/subaru0573/super-data-analysis) <br>
- [Publisher profile](https://clawhub.ai/user/subaru0573) <br>
- [Metric contracts](artifact/metric-contracts.md) <br>
- [Chart selection](artifact/chart-selection.md) <br>
- [Decision briefs](artifact/decision-briefs.md) <br>
- [Analytical pitfalls](artifact/pitfalls.md) <br>
- [Analysis techniques](artifact/techniques.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with optional SQL, Python, spreadsheet formulas, chart specifications, and report templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only skill; no external endpoints, persistent memory, or local storage are required by default.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
