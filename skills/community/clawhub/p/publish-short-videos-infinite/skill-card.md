## Description:

Coordinates short-video publishing across Kuaishou, Douyin, and Xiaohongshu in sequence, publishing on Kuaishou and saving drafts on Douyin and Xiaohongshu.

This skill is ready for commercial/non-commercial use.

## Publisher:

[infiniteask](https://clawhub.ai/user/infiniteask)

### License/Terms of Use:

MIT-0

## Use Case:

Content operators and creators use this skill to coordinate one short-video asset across three Chinese social video platforms with a fixed platform order and platform-specific final actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can publish a video publicly on Kuaishou.

Mitigation: Require explicit user confirmation before any live publish action and verify the intended video, title, description, tags, and permissions before submission.

Risk: The workflow depends on three local child skills that the security evidence describes as unaudited.

Mitigation: Review and trust the referenced child skills before installation or execution.

Risk: Platform-specific final actions differ: Kuaishou is published live, while Douyin and Xiaohongshu are saved as drafts.

Mitigation: Keep the documented execution order and final-action checks visible during use so draft-only steps are not accidentally converted into publish actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/infiniteask/skills/publish-short-videos-infinite)
- [ClawHub publisher profile](https://clawhub.ai/user/infiniteask)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown instructions with ordered workflow steps and local skill paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Coordinates browser-based platform actions and delegates platform-specific details to local child skills.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
