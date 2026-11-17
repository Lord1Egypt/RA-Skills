## Description:

Analyzes fixed-camera video and optional audio in dementia care settings for signs of confusion or disorientation and provides orientation-soothing actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Care teams in dementia facilities or home-care settings use the skill to analyze video and optional audio for possible disorientation cues and receive structured reports and orientation-soothing suggestions. The skill states that it does not provide medical diagnoses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review rates the skill suspicious due to reported concerns about account and identity handling, possible exposure of care reports, and video processing despite an export-only option. The scan is partial because a referenced path was missing.

Mitigation: Review identity and token handling, care-report access, and remote video processing before installation, and account for the scan's missing-path limitation.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/smyx-sunjinhui/skills/smyx-dementia-confusion-orientation-analysis)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [API documentation](artifact/references/api_doc.md)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Guidance]

**Output Format:** [Structured analysis report with detected cues, soothing actions or suggestions, and report links when available; supports basic, standard, and JSON detail levels.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Analyzes a supplied local file or URL; audio is optional.]

## Skill Version(s):

1.0.13 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
