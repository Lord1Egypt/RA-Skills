## Description:

Analyzes facial videos for expression and emotion cues, then returns a structured report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

People reviewing facial video clips can request basic, micro-expression, or broader emotion analyses and receive a structured report. The skill can also retrieve previously generated reports associated with the account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release is marked suspicious for identity and credential handling, remote account registration, and possible analysis during export-only mode; the scan was partial.

Mitigation: Review what facial media, identity details, and account data are sent or stored, and confirm whether export-only mode can trigger analysis before using the skill.

Risk: Emotion reports can be mistaken for reliable evidence of a person's inner state.

Mitigation: Treat findings as tentative expression cues, account for video quality and occlusion, and do not use the report as a substitute for professional assessment or as the sole basis for consequential decisions.

## Reference(s):

- [API interface notes](references/api_doc.md)
- [Analysis API details](skills/smyx_analysis/references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [ClawHub release page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-emotion-analysis)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Structured text or JSON analysis report with a report export link]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include expression and emotion cues, suggestions, and report links; output detail can be selected.]

## Skill Version(s):

1.0.22 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
