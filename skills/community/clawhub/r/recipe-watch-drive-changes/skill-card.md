## Description:

Subscribe to change notifications on a Google Drive file or folder.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this recipe to create, list, and renew Google Workspace Drive change notification subscriptions for a target Drive file or folder.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The recipe creates Google Drive event subscriptions against a specified Drive resource and Pub/Sub topic.

Mitigation: Review the Drive ID, Google Cloud project, Pub/Sub topic permissions, event types, and resource payload setting before running the create command.

Risk: Unneeded or expired subscriptions can continue to affect notification handling if not managed.

Mitigation: List active subscriptions regularly and renew, clean up, or let expire subscriptions according to operational needs.

## Reference(s):

- [Recipe Watch Drive Changes on ClawHub](https://clawhub.ai/googleworkspace-bot/skills/recipe-watch-drive-changes)
- [googleworkspace-bot publisher profile](https://clawhub.ai/user/googleworkspace-bot)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gws command-line tool and the gws-events skill.]

## Skill Version(s):

0.22.5 (source: frontmatter); ClawHub release 1.0.12

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
