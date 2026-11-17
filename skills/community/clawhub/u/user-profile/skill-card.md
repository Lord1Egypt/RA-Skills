## Description:

Builds a local user profile by recording preferences, summarizing them across sessions, and inferring recurring personality traits into workspace/PROFILE.md.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lyl340321](https://clawhub.ai/user/lyl340321)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to maintain a local, editable profile of user preferences and recurring traits so later sessions can personalize communication and work patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may automatically save personal preferences and inferred traits across sessions.

Mitigation: Require explicit approval before saving memories and review PROFILE.md and memory files periodically.

Risk: Profile entries may include sensitive, stale, or incorrect personal information.

Mitigation: Exclude sensitive categories where possible and delete or correct stale or inaccurate profile entries.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lyl340321/skills/user-profile)
- [ClawHub publisher profile](https://clawhub.ai/user/lyl340321)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown profile files plus JSON state]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates workspace/PROFILE.md, daily memory Markdown files, and memory/profile-state.json.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
