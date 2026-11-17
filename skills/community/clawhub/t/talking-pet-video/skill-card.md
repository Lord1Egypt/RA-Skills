## Description:

Turns one clear pet photo and a short message or approved voice clip into a shareable talking-pet video, with checks for identity, mouth motion, speech clarity, and synchronization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and pet creators use this skill to turn a pet photo and a short script or approved recording into a shareable talking-pet clip, then review identity, mouth motion, speech clarity, and synchronization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release requests broader account permissions than pet-video creation needs, including music generation and voice modification.

Mitigation: Review the full Beatra authorization and proceed only if you accept these additional permissions.

Risk: The security guidance notes automatic installation reporting and that selected media is sent to Beatra.

Mitigation: Confirm the selected media may be sent and review the reporting details; revoke access in the Beatra Console when needed.

Risk: The security guidance notes that workflow stages may be paid.

Mitigation: Review the cost for each stage and approve each paid stage separately.

## Reference(s):

- [Beatra skill page](https://beatra.ai/skills/talking-pet-video)
- [ClawHub release page](https://clawhub.ai/beatra-ai/skills/talking-pet-video)
- [Workflow guidance](references/workflow.md)
- [Updates and security](references/updates-and-security.md)
- [Installation registration](references/installation-registration.md)

## Skill Output:

**Output Type(s):** [Video, Audio, Guidance]

**Output Format:** [Returned video and audio media artifacts with a Markdown delivery summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Video identity, mouth motion, speech clarity, and synchronization should be reviewed; results are not guaranteed to be identical across animals.]

## Skill Version(s):

0.2.7 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
