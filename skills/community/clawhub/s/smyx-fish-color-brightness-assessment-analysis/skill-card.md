## Description:

Analyzes ornamental fish images or videos for color saturation and brightness, then produces species-aware vibrancy scores and reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Aquarium hobbyists, aquaculture staff, and aquarium operators can assess ornamental fish color from side-view images or video and review species-based vibrancy reports over time. The results are husbandry indicators, not veterinary diagnoses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment reports account, credential, and remote-service behavior beyond the stated fish-color analysis purpose, with privacy and execution-control concerns.

Mitigation: Before installation, independently review account and credential handling, permitted remote destinations, media-upload disclosure, and export-only behavior, as advised by the security evidence.

Risk: Image, video, or URL inputs may be processed by a remote service, creating privacy exposure for media the user is not authorized to share.

Mitigation: Use only authorized media, disclose remote processing to affected people where appropriate, and avoid images that contain unrelated sensitive information.

Risk: The security scan was partial and could not resolve one local reference in SKILL.md, leaving connected behavior unverified.

Mitigation: Resolve and review that reference and the behavior it connects to before relying on the skill.

## Reference(s):

- [ClawHub release](https://clawhub.ai/smyx-sunjinhui/skills/smyx-fish-color-brightness-assessment-analysis)
- [API reference](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Text, JSON, Markdown]

**Output Format:** [Structured JSON analysis reports and Markdown history tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include HSV measurements, species-baseline comparisons, vibrancy scores and trends, alerts, and husbandry suggestions; not a disease diagnosis.]

## Skill Version(s):

1.0.18 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
