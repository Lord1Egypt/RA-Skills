## Description:

Analyzes plant images or videos for early signs of wilting and returns structured findings, severity estimates, and early-warning guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Growers and crop-monitoring teams can submit plant photos or videos to assess early wilting, consider environmental or disease-related causes, and receive monitoring guidance. Results are early-warning references; the skill advises consulting plant-health experts for final diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The partial security scan flagged account handling, credential storage, network activity, and media uploads beyond the described plant analysis; some service behavior and network destinations could not be verified.

Mitigation: Review those behaviors and destinations before use, and submit only plant media and account-linked data you are comfortable sending to the service.

## Reference(s):

- [API interface documentation](skills/smyx_analysis/references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown, Guidance]

**Output Format:** [Structured analysis results and recommendations in JSON; history report lists in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts local image or video files and network URLs; can query linked historical reports. The skill describes its findings as early-warning references, not a final diagnosis.]

## Skill Version(s):

1.0.21 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
