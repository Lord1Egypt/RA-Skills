## Description:

Generates a daily, deterministic 5D personality prompt for an agent's SOUL.md using local date and agent-name hashing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spacesq](https://clawhub.ai/user/spacesq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users can use this skill to generate a daily Markdown prompt that changes an agent's style or personality profile. It is intended for local prompt generation rather than automatic modification of workspace files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated SOUL.md content can influence how autonomously an agent uses external tools.

Mitigation: Review the generated text before using it, and do not allow daily personality scores to control permissions, terminal use, tool autonomy, approvals, or safety behavior.

Risk: System-directive lines and promotional links may be inappropriate when the user only wants a style prompt.

Mitigation: Remove the system-directive/autonomy lines and promotional URL before persisting the output when they are not desired.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/spacesq/skills/s2-neuro-soul-link)
- [Publisher profile](https://clawhub.ai/user/spacesq)
- [Space2.world](https://space2.world)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Plain-text response containing Markdown SOUL.md content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally and returns generated content for human review; it does not automatically write SOUL.md.]

## Skill Version(s):

1.0.5 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
