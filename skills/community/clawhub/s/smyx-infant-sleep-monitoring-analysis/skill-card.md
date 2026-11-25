## Description:

Identifies infant sleep states such as deep sleep, light sleep, waking, and restlessness, and generates daily sleep reports and schedule analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Parents and caregivers use the skill to analyze infant sleep-monitoring videos, review sleep-state and timing summaries, and view daily or historical reports. The results are for parenting reference and do not replace pediatric advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates this release suspicious with high confidence, citing unclear account and credential handling, infant video transfers without a clear consent gate or destination, and possible analysis during export-only mode.

Mitigation: Consider not installing until account and credential behavior, video consent and destinations, and export-only behavior are explained. The scan was partial because one local reference could not be matched, so review of all referenced material is not established.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-infant-sleep-monitoring-analysis)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [API reference](references/api_doc.md)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown, Report links]

**Output Format:** [Structured sleep analysis reports, with Markdown tables for historical report lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include sleep-state classifications, sleep timing and waking summaries, recommendations, and report links; results are for parenting reference, not medical advice.]

## Skill Version(s):

1.0.19 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
