## Description:

Helps agents submit and check digital-avatar lip-sync jobs using the a7w API and the user's API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2253128](https://clawhub.ai/user/2253128)

### License/Terms of Use:

MIT

## Use Case:

Developers and content creators use this skill to submit source video and audio URLs for a digital-avatar lip-sync job and check the resulting task status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The configurable API host can receive the user's API key.

Mitigation: Review before installing; use a dedicated, revocable, low-balance key and avoid untrusted host or configuration changes.

Risk: Submitted audio and video URLs are processed by an external service.

Mitigation: Submit only media authorized for external processing; avoid confidential media URLs unless that processing is acceptable.

Risk: The bundled client can call other a7w API endpoints beyond lip-sync.

Mitigation: Review commands before execution and limit calls to the intended lip-sync endpoints.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/2253128/skills/sanjianke-lipsync)
- [Getting started and API key setup](references/getting-started.md)
- [Submit API documentation](references/api-submit.md)
- [Query API documentation](references/api-query.md)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [JSON task status and results; Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Submission is asynchronous; calls require an a7w API key and may incur charges.]

## Skill Version(s):

1.0.5 (source: ClawHub release metadata; bundled frontmatter says 1.0.4)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
