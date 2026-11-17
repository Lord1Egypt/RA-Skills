## Description:

Zhixi Mind Map Cloud File Management (知犀思维导图云文件管理): Browse, search, view content, and import Markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mindtwigs](https://clawhub.ai/user/mindtwigs)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent browse, search, preview, and import Markdown into a Zhixi cloud mind-map account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Zhixi cloud credentials.

Mitigation: Use ZHIXI_API_KEY from a managed secret or environment variable and avoid storing credentials in a token file.

Risk: Markdown import uploads local file contents to Zhixi.

Mitigation: Import only files you intend to place in the Zhixi cloud account and review sensitive content before upload.

Risk: The skill can perform cloud file actions through the connected account.

Mitigation: Review requested browse, search, content, and import actions before allowing automated execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mindtwigs/skills/zhixi-mindmap)
- [Zhixi account center](https://www.zhixi.com/account)
- [Zhixi API endpoint](https://www.zhixi.com/api)
- [Zhixi pricing](https://www.zhixi.com/pricing?from=openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown and JSON returned from Zhixi cloud file operations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include file titles, folder IDs, file GUIDs, Markdown content, import results, and online access links.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
