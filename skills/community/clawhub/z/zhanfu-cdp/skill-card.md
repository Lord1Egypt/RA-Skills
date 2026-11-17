## Description:

Automates Zhanfu shop management through its WebDriver API and uses Playwright for requested browser page tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangzhang1997](https://clawhub.ai/user/zhangzhang1997)

### License/Terms of Use:

MIT-0

## Use Case:

External users can ask an agent to manage Zhanfu shops, including opening, closing, listing, and configuring them. For requested page tasks, the agent can automate a shop browser with Playwright.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cache or log cleanup may delete local data without confirmation.

Mitigation: Review the requested cleanup scope and target before running a cache-clearing operation.

Risk: Retries after communication failures and a background watcher may continue work beyond a single request.

Mitigation: Check active shop operations and stop them explicitly when appropriate.

Risk: Some skill files were only partially inspected, so the security evidence is incomplete.

Mitigation: Review the full skill and its dependencies before installing or running it.

## Reference(s):

- [Zhanfu WebDriver API reference](artifact/reference.md)
- [ClawHub skill page](https://clawhub.ai/zhangzhang1997/skills/zhanfu-cdp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration]

**Output Format:** [Markdown guidance with shell command examples and JSON operation results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Operation results may include shop IDs and WebDriver ports.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
