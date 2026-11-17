## Description:

Analyzes living-room camera footage from a commuter’s first 30 minutes at home to estimate fatigue and trigger gentle smart-home care prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Smart-home users can use this skill to analyze living-room video, optionally with audio, from the period after they arrive home and receive a fatigue report and care suggestions. It describes fatigue monitoring rather than medical diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment rates this release suspicious with high confidence, citing privacy and consent gaps, behavior beyond the stated fatigue-monitoring purpose, and persistent identity and credential handling.

Mitigation: Avoid installation until the developer explains account and token handling, where household video is sent, and how consent and retention are handled.

Risk: The security guidance says export-only behavior needs to be fixed, and the scan was partial because a referenced local item was missing.

Mitigation: Confirm the export-only behavior is corrected and review a complete security scan before use.

## Reference(s):

- [API documentation](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [ClawHub release](https://clawhub.ai/smyx-sunjinhui/skills/smyx-commuter-fatigue-care-analysis)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown, Guidance]

**Output Format:** [Structured fatigue analysis report and Markdown history table]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include fatigue indicators, a 0–100 fatigue index, care suggestions, and report links.]

## Skill Version(s):

1.0.15 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
