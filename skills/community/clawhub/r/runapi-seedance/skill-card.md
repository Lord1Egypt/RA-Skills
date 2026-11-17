## Description:

Generate, edit, and transform video with Seedance through RunAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runapi-ai](https://clawhub.ai/user/runapi-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and engineers use this skill to create, edit, or transform video with Seedance through RunAPI. It supports one-off CLI generation and SDK-based application integration while requiring contract discovery and deliverable verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Use requires RunAPI authentication and may upload local media referenced in requests.

Mitigation: Use the skill only for intended RunAPI and Seedance workflows, provide credentials deliberately, and review local media before submission.

Risk: Downloaded deliverables rely on service-returned URLs and output paths.

Mitigation: Quote and validate returned URLs and output paths before shell execution, then verify downloaded files are non-empty and match the expected MIME type.

Risk: Submitting replacement generation tasks after a service failure can create unintended paid requests.

Mitigation: Preserve task and error evidence, retry only within the documented bounded recovery flow, and request user authorization before any replacement paid submission.

## Reference(s):

- [RunAPI Seedance model overview](https://runapi.ai/models/seedance.md)
- [RunAPI Seedance homepage](https://runapi.ai/models/seedance)
- [ByteDance provider overview](https://runapi.ai/providers/bytedance.md)
- [RunAPI model catalog](https://runapi.ai/models.md)
- [Seedance SDK integration](https://github.com/runapi-ai/seedance-sdk)
- [ClawHub skill page](https://clawhub.ai/runapi-ai/skills/runapi-seedance)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code, JSON, Files]

**Output Format:** [Markdown guidance with shell commands, JSON request files, and downloaded video artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Seedance video deliverables through RunAPI and requires non-empty file and MIME-type verification for downloaded media.]

## Skill Version(s):

0.2.12 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
