## Description:

User Insight helps an assistant build and update a local user profile from conversations, then use that profile to personalize replies and suggest conversation topics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chasezxs](https://clawhub.ai/user/chasezxs)

### License/Terms of Use:


## Use Case:

External users and agent developers use this skill to personalize conversational assistance by extracting interests, preferences, habits, message snippets, and engagement patterns into a local profile. It can also recommend topics and conversation openers based on the accumulated profile.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persistently profiles users by saving interests, habits, message snippets, engagement patterns, and topic exploration history.

Mitigation: Use only with explicit opt-in consent and make profiling visible to the user before collection starts.

Risk: The artifact describes pause, delete, forget, and reset commands, but the security evidence says enforceable consent and deletion controls are not present.

Mitigation: Add working pause, delete, reset, and export controls before deployment, and verify that scripts honor those controls.

Risk: Profile data is stored in local memory files that may contain personal details and message previews.

Mitigation: Restrict file permissions, minimize stored message text, and narrow file access to the specific profile and exploration files required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chasezxs/skills/user-insight)
- [ClawHub publisher profile](https://clawhub.ai/user/chasezxs)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance, Configuration]

**Output Format:** [Markdown guidance and JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes and reads local memory files under ~/.openclaw/workspace/memory when its scripts are used.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
