## Description:

在挖象浏览器中登录（如有需要）并打开用户指定分组中的店铺。

This skill is ready for commercial/non-commercial use.

## Publisher:

[randydai](https://clawhub.ai/user/randydai)

### License/Terms of Use:

MIT-0

## Use Case:

挖象浏览器用户可让代理在指定分组中打开指定店铺；如尚未登录，流程使用用户提供的凭据登录。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Logging in uses user-provided Waxiang credentials.

Mitigation: Review the runtime warning and provide credentials only when you intend to log in.

Risk: The local debugging port and returned shop port can allow same-machine automation to control the browser session while running.

Mitigation: Run only on a trusted device, keep debug ports local and disconnect the debugging connection when finished.

Risk: Restarting an existing Waxiang Browser instance can interrupt an active session.

Mitigation: Obtain explicit user consent before closing a running browser.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/randydai/skills/waxiang-store)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Text]

**Output Format:** [Markdown instructions and text with JSON-formatted browser response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports started status, reason and available local shop debugging port.]

## Skill Version(s):

1.0.4 (source: skill frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
