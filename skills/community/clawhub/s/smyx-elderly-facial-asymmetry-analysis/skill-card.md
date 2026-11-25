## Description:

Analyzes frontal images or short videos of older adults for facial asymmetry and mouth-corner deviation, producing a facial asymmetry index and screening alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Caregivers and elder-care providers use the skill to review facial asymmetry in frontal images or short videos as an early screening aid. Its score and alerts are not a medical diagnosis; possible stroke symptoms require prompt medical attention.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marked the release suspicious for account provisioning, credential storage, and network behavior it could not reconcile; the review is partial.

Mitigation: Review account and credential handling and network destinations before use. Use only a trusted service and avoid sending sensitive media until these behaviors are understood.

Risk: The scan flagged possible analysis when users expect it not to, including unexpected media processing.

Mitigation: Confirm when analysis can run and obtain the subject’s informed consent before processing facial images or video. Disable automatic triggers unless they are explicitly intended.

Risk: A screening score or alert could be mistaken for a clinical diagnosis or delay urgent care.

Mitigation: Treat results as screening information only. Seek urgent medical evaluation for possible stroke symptoms rather than relying on the score.

## Reference(s):

- [API documentation](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-elderly-facial-asymmetry-analysis)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown, Guidance]

**Output Format:** [Structured JSON analysis results and Markdown summaries with screening indicators and report links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a facial asymmetry index (0–100%), side and risk indicators, and follow-up prompts; screening support only, not diagnosis]

## Skill Version(s):

1.0.13 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
