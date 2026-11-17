## Description:

Intelligently dispatches WeChat messages by extracting recipients and content, then routing text, image, or file sends through confirmation and selection flows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aw11100](https://clawhub.ai/user/aw11100)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation users can use this skill to operate a WeChat bridge that matches contacts or chatrooms and sends text, image, or file messages after user confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bridge can send messages for an account with poor safeguards.

Mitigation: Run it only behind strong authentication and network restrictions, and require server-side confirmation tokens before sending messages.

Risk: The release includes a reusable WeChat secret.

Mitigation: Remove the exposed token from the release and rotate it before deployment.

Risk: The backend transport should not rely on plain HTTP.

Mitigation: Change the backend connection to HTTPS before use.

Risk: Dependencies are not pinned with a lockfile.

Mitigation: Pin dependencies and commit a lockfile before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aw11100/skills/wechat-new-tool)
- [Publisher profile](https://clawhub.ai/user/aw11100)

## Skill Output:

**Output Type(s):** [Text, API calls, Guidance, Configuration]

**Output Format:** [Markdown or plain text responses with JSON API payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user confirmation or choice selection before final message sending.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
