## Description:

Send multiple images or files in a single Zalo message using zca-js directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tuanbi97](https://clawhub.ai/user/tuanbi97)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to send multiple local or URL-based attachments to a Zalo contact or group in one message when single-media sending is insufficient.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use stored Zalo credentials to send messages and attachments immediately.

Mitigation: Require explicit confirmation of the recipient, group setting, credential profile, caption, and attachment list before execution.

Risk: Local paths may expose sensitive files, and URL attachments may fetch untrusted remote content.

Mitigation: Avoid sensitive local files and untrusted URLs; use HTTPS-only fetching, URL allowlisting, file size limits, and request timeouts where possible.

Risk: Recipient and profile safeguards are weak for agents that may act automatically.

Mitigation: Use recipient allowlists and profile controls before deploying the skill in automated workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tuanbi97/skills/zalo-multi-send)

## Skill Output:

**Output Type(s):** [Shell commands, Text, JSON]

**Output Format:** [Command-line output with optional JSON API response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May send the selected caption and attachments to a specified Zalo user or group.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
