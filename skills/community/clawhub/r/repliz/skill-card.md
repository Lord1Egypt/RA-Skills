## Description:

Repliz Api helps agents use the Repliz social media management API to manage connected accounts, scheduled posts, and comment queues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[staryone](https://clawhub.ai/user/staryone)

### License/Terms of Use:


## Use Case:

External users and developers with Repliz accounts use this skill to configure API credentials, inspect connected social accounts, create or delete scheduled posts, and reply to queued comments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to use Repliz credentials for public posting and comment replies on connected social accounts.

Mitigation: Require the agent to list the exact account, content, target action, and destination before asking for explicit confirmation.

Risk: Scheduled-post deletion is irreversible.

Mitigation: Before deletion, require confirmation of the schedule item ID, connected account, platform, and scheduled time.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/staryone/skills/repliz)
- [Repliz homepage](https://repliz.com)
- [Repliz API credential settings](https://repliz.com/user/setting/api)
- [Repliz API base URL](https://api.repliz.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Repliz API endpoint guidance, Basic Authentication setup, and request body examples.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
