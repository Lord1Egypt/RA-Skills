## Description: <br>
Ptengine Heatmap Analyze fetches heatmap metrics through a user-installed ptengine-cli tool and guides CRO behavior analysis with a four-stage psychology model. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaichen](https://clawhub.ai/user/zhaichen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External marketers, CRO practitioners, analysts, and site operators use this skill to analyze Ptengine heatmap data, compare segments, validate A/B tests, evaluate ad performance, and identify conversion barriers or opportunities on landing pages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review says the skill needs review because it tells the agent to handle a Ptengine API key despite also saying it does not. <br>
Mitigation: Configure ptengine-cli manually or through a secure credential prompt, do not paste API keys into chat, and prefer a least-privileged Ptengine key. <br>
Risk: Heatmap queries and generated reports may expose sensitive business analytics. <br>
Mitigation: Limit use to authorized Ptengine profiles and avoid sharing outputs outside the teams approved to view the underlying analytics. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/zhaichen/ptengine-heatmap-analyze) <br>
- [ptengine-cli upstream repository](https://github.com/Kocoro-lab/ptengine-cli) <br>
- [ptengine-cli releases](https://github.com/Kocoro-lab/ptengine-cli/releases) <br>
- [ptengine-cli command reference](references/ptengine-cli.md) <br>
- [Data transform reference](references/data-transform.md) <br>
- [Page classification reference](references/page-classification.md) <br>
- [Page types reference](references/page-types.md) <br>
- [Quality constraints reference](references/quality-constraints.md) <br>
- [Single page analysis task](references/single-page-task.md) <br>
- [Segment comparison task](references/compare-task.md) <br>
- [A/B test validation task](references/ab-test-task.md) <br>
- [Ad performance analysis task](references/ad-performance.md) <br>
- [Audience analysis task](references/audience-analysis.md) <br>
- [Block analysis reference](references/block-analysis.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with inline shell commands and evidence-grounded recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Ptengine CLI JSON responses as the authoritative data source and presents concise CRO findings, barriers, opportunities, and next steps.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
