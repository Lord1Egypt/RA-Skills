## Description:

Analyzes pet ear images or videos for visible redness, discharge, and wax buildup, then provides observations and suggests when to seek veterinary care without making a diagnosis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Pet owners, boarding centers, and veterinary clinics can use the skill to review ear images or videos for visible signs that may warrant closer attention or veterinary follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review rates this release suspicious, citing remote media uploads and account and report-history handling.

Mitigation: Review the data flows, account behavior, and report-history handling before installation; avoid submitting sensitive media until transfer and retention are understood.

Risk: The security review reports that the export-only option may still run analysis.

Mitigation: Do not rely on the export-only option to prevent execution; verify behavior before invoking it.

Risk: Security analysis was partial because a local path-like reference was missing, leaving the evidence incomplete.

Mitigation: Resolve the missing reference and complete a fresh security review before deployment.

## Reference(s):

- [API documentation](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [ClawHub release](https://clawhub.ai/smyx-sunjinhui/skills/smyx-ear-health-snapshot-analysis)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Guidance]

**Output Format:** [Structured analysis results and Markdown report listings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include visual observations, alerts, recommendations, and report links; not a medical diagnosis.]

## Skill Version(s):

1.0.17 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
