## Description:

Analyzes indoor-camera video to flag possible pet contact with hazardous non-food items and provide a safety report without diagnosing disease.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Pet owners and smart-home operators use the skill to review indoor-camera video for possible chewing or contact with hazardous non-food items and receive a warning with safety guidance. They can also request a list of past analysis reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reports potentially broad or unintended video transfers to remote services.

Mitigation: Confirm when video is sent and what video data is transmitted before use.

Risk: ClawScan reports unexpected account and profile management.

Mitigation: Confirm what identity and profile data is stored or transmitted.

Risk: ClawScan rates the release suspicious because of behavior beyond its stated pet-video analysis purpose; the scan was partial because a local reference was missing.

Mitigation: Clarify the reported behavior, verify whether export-only mode prevents analysis, and review the missing reference before installation.

## Reference(s):

- [API interface documentation](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [ClawHub skill listing](https://clawhub.ai/18072937735/skills/smyx-pet-pica-behavior-recognition-analysis)

## Skill Output:

**Output Type(s):** [Text, JSON, Markdown]

**Output Format:** [Structured JSON analysis reports and Markdown tables for report lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include contact duration, risk level, safety suggestions, warning signals, and report links. Results are for safety monitoring and do not diagnose disease.]

## Skill Version(s):

1.0.17 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
