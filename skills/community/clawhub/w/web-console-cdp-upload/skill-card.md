## Description:

平台只有网页后台、没有上传 API 时，用本机已装的 Chrome/Edge + CDP 自动化走完上传/发布/填表流程，复用真实登录态并避免安装浏览器。

This skill is ready for commercial/non-commercial use.

## Publisher:

[oracis](https://clawhub.ai/user/oracis)

### License/Terms of Use:

MIT-0

## Use Case:

开发者可用此技能通过本机 Chrome 或 Edge 完成需要登录的网页后台上传、发布和表单操作，也可检查富文本内容保存后的效果。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CDP automation can access a signed-in browser session and change or publish drafts.

Mitigation: Use an isolated browser profile with only the account session needed for the task; review each intended change and reload the page to confirm saved state.

Risk: A browser debugging endpoint can expose control of the active browser session.

Mitigation: Keep the debugging endpoint local, review the WebSocket-origin settings before connecting, and close the debugging browser when the task is complete.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/oracis/skills/web-console-cdp-upload)
- [Publisher profile](https://clawhub.ai/user/oracis)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown guide with shell commands, JavaScript snippets, and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instructions and examples for browser-backed web workflows.]

## Skill Version(s):

1.3.2 (source: server-resolved release; frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
