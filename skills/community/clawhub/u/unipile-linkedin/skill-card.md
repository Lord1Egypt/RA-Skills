## Description:

Interact with LinkedIn via Unipile API - send messages, view profiles, manage connections, create posts, react to content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sudhanshu746](https://clawhub.ai/user/sudhanshu746)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to let an agent interact with LinkedIn through the Unipile API for messaging, profile lookup, connection management, posting, commenting, and reactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send LinkedIn messages, invitations, posts, comments, reactions, and profile view notifications through a real account.

Mitigation: Require explicit approval before running live-action commands such as send, start-chat, invite, cancel-invite, create-post, comment, react, or profile --notify.

Risk: A Unipile access token can act on the user's LinkedIn account.

Mitigation: Store the token only in a trusted environment, rotate it if exposure is suspected, and revoke it if endpoint or environment configuration may have been changed.

Risk: A misconfigured or untrusted Unipile endpoint could route account actions or data to an unintended service.

Mitigation: Use a trusted Unipile endpoint and verify the DSN before configuring the skill.

## Reference(s):

- [Unipile API](https://www.unipile.com/)
- [Unipile Dashboard](https://dashboard.unipile.com)
- [ClawHub Skill Page](https://clawhub.ai/sudhanshu746/skills/unipile-linkedin)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May perform live LinkedIn account actions through a configured Unipile token.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
