## Description:

Collects Baidu search result titles for the keyword "指数大师", orders the main titles as a numbered list, and can send the result to a WeCom robot webhook.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shidengyun](https://clawhub.ai/user/shidengyun)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to take a daily or scheduled snapshot of Baidu ranking titles for the keyword "指数大师" and report the ordered title list. It is intended for keyword ranking observation, brand-term monitoring, and search-result status updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill embeds a live WeCom webhook credential and sends messages to that fixed external destination by default.

Mitigation: Revoke or rotate the exposed webhook key, require users to provide their own webhook URL, and ask for confirmation before sending any message.

Risk: Collected Baidu title lists may be disclosed to an external WeCom robot when the push workflow is used.

Mitigation: Use dry-run or local review first, override the destination with a user-controlled webhook only when sharing is intended, and avoid sending sensitive search snapshots.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shidengyun/skills/wacai-zhishudashi-baidu-ranking)
- [Publisher profile](https://clawhub.ai/user/shidengyun)
- [Baidu search homepage](https://www.baidu.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown text with numbered title lists and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May send the title list to a WeCom webhook unless configured for dry-run or an explicit webhook override.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
