## Description:

Medical checkup report analysis that submits a PDF URL or local PDF upload to WiseDiag for AI-powered health interpretation with abnormal item detection, clinical explanations, lifestyle assessment, and personalized recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wisediag](https://clawhub.ai/user/wisediag)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to submit checkup reports to WiseDiag and receive structured Markdown health interpretations, abnormal-item summaries, lifestyle assessment, and personalized recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Checkup reports, questionnaire details, and optional member IDs are transmitted to WiseDiag's cloud API.

Mitigation: Use the skill only when the user accepts remote processing; avoid highly sensitive documents unless WiseDiag's data handling is trusted, and keep generated Markdown reports in private locations.

Risk: Generated health interpretations may be mistaken for medical diagnosis or treatment advice.

Mitigation: Present results as informational analysis and direct users to qualified medical professionals for health decisions.

Risk: The Python dependency is not pinned to an exact version.

Mitigation: Pin and review dependencies before production deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wisediag/skills/wiseanalyze)
- [WiseDiag API key console](https://console.wisediag.com/apiKeyManage)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with machine-readable CLI status lines]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires WISEDIAG_API_KEY and may upload report files, questionnaire details, and optional member IDs to WiseDiag's cloud API.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
