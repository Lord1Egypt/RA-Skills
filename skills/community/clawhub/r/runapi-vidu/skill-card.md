## Description:

Guides developers on Vidu Q4 video generation through RunAPI; generation is not available until callable endpoints are published.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runapi-ai](https://clawhub.ai/user/runapi-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers using RunAPI can consult Vidu Q4 image-to-video and reference-to-video guidance. Until callable endpoints are published, use read-only CLI help and current documentation; do not submit generation requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Vidu endpoints are not yet callable, and current release availability could not be verified.

Mitigation: Check the linked model and endpoint documentation before integrating; use only read-only CLI help until a callable contract is published.

Risk: Future generation may involve media handling and pricing considerations.

Mitigation: Review RunAPI's media handling and pricing before submitting generation requests.

## Reference(s):

- [Vidu model overview, pricing, and rate limits](https://runapi.ai/models/vidu.md)
- [RunAPI Vidu provider overview](https://runapi.ai/providers/vidu.md)
- [RunAPI model catalog](https://runapi.ai/models.md)
- [Vidu Q4 image-to-video variant](https://runapi.ai/models/vidu/q4-image-to-video.md)
- [Vidu Q4 reference-to-video variant](https://runapi.ai/models/vidu/q4-reference-to-video.md)
- [RunAPI Vidu SDK](https://github.com/runapi-ai/vidu-sdk)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands]

**Output Format:** [Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only discovery only until callable endpoints are published; the skill does not currently produce videos.]

## Skill Version(s):

0.1.1 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
