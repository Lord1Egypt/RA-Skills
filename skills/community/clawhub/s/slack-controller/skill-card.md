## Description:

Control Slack via Browser Automation to send messages, manage huddles, screen share, set status, and react as the logged-in user.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adeel-powerhouse](https://clawhub.ai/user/adeel-powerhouse)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to control an authenticated Slack Web or Desktop session through agent or CLI commands for messaging, huddles, screen sharing, status, file upload, reactions, and search.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can operate a real Slack session as the logged-in user, including sending messages, uploading files, starting huddles, and sharing the screen.

Mitigation: Require explicit confirmation before any Slack action that sends content, changes status or presence, uploads files, starts or joins huddles, shares the screen, or searches sensitive workspaces.

Risk: The skill requires desktop automation permissions that can broaden the impact of misuse or mistakes.

Mitigation: Install only from a trusted source, use the narrowest practical desktop and Slack permissions, and review commands before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/adeel-powerhouse/skills/slack-controller)
- [Slack Web Client](https://app.slack.com)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with inline CLI command examples and text results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May perform Slack workspace actions as the logged-in user, including sending messages, uploading files, changing presence, starting huddles, and sharing the screen.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact skill.yaml reports 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
