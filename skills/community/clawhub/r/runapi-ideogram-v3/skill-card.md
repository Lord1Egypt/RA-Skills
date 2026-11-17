## Description:

Guides agents to generate and edit images with Ideogram V3 through RunAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runapi-ai](https://clawhub.ai/user/runapi-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and developers use this skill to generate or edit Ideogram V3 images through RunAPI, either as one-off tasks or in application integrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing an untrusted CLI or connecting to an untrusted service could expose credentials or content.

Mitigation: Confirm trust in RunAPI and its Homebrew tap before installation; use an environment-provided API key or explicit token import.

Risk: Image prompts and local media used for editing may be sent to RunAPI and Ideogram.

Mitigation: Share only prompts and media authorized for the external service.

Risk: Submitting another task after a failure may incur additional charges.

Mitigation: Preserve the existing task and error details; obtain user approval before any additional paid submission.

## Reference(s):

- [RunAPI Ideogram V3 model overview](https://runapi.ai/models/ideogram-v3.md)
- [RunAPI Ideogram V3 model page](https://runapi.ai/models/ideogram-v3)
- [RunAPI Ideogram provider overview](https://runapi.ai/providers/ideogram.md)
- [RunAPI Ideogram V3 SDK integration](https://github.com/runapi-ai/ideogram-v3-sdk)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Images]

**Output Format:** [Markdown guidance, CLI commands or SDK code, and downloaded image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires RunAPI authentication; verifies downloaded images are nonempty and have the expected MIME type.]

## Skill Version(s):

0.3.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
