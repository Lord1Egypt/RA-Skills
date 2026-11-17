## Description:

Automates bulk friend additions in the WeCom PC client from phone-number lists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whailon](https://clawhub.ai/user/whailon)

### License/Terms of Use:

MIT-0

## Use Case:

Employees or operators using WeCom on Windows use this skill to parse phone-number lists and run bundled desktop automation for adding contacts in bulk.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow can send a friend request to a hard-coded test phone number.

Mitigation: Make setup side-effect-free and require explicit confirmation before any outbound friend request.

Risk: Window targeting and saved coordinates can cause typing or clicking in the wrong application.

Mitigation: Fail closed unless the WeCom window is positively identified, revalidate saved coordinates before use, and keep the target window visible.

Risk: The skill operates a logged-in WeCom desktop account and can send real friend requests.

Mitigation: Review behavior before installation and avoid primary accounts unless confirmations and window-targeting safeguards are in place.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/whailon/skills/wecom-add-friend)
- [ClawHub publisher profile](https://clawhub.ai/user/whailon)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Windows-only WeCom desktop automation; requires Python and the bundled bin/wecom_auto_add.py file.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
