## Description:

微信公众号调研 + 监控 + 报告推送。每个产品独立目录，互不影响。

This skill is ready for commercial/non-commercial use.

## Publisher:

[a1003916989-blip](https://clawhub.ai/user/a1003916989-blip)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and marketing operators use this skill to research WeChat public accounts for a product, confirm monitored accounts, generate local account configuration, and produce recurring Markdown monitoring reports with content-topic suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles an mptext API credential.

Mitigation: Set MPTEXT_API_KEY through an environment variable or secret manager and do not edit the script with a real key.

Risk: Scheduled monitoring can repeatedly transmit account identifiers and retrieve article data from a third-party service.

Mitigation: Review the scheduler, destination, transmitted data, and removal steps before enabling recurring runs.

Risk: The script creates, reads, and deletes files in per-product directories using a command-line product name.

Mitigation: Run it only with simple product names you control and review generated account and report paths before automation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/a1003916989-blip/skills/wechat-monitor)
- [mptext API base URL](https://down.mptext.top/api/public/v1)
- [mptext service](https://down.mptext.top)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports with inline shell commands and JSON configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes per-product account lists and dated Markdown reports under the skill workspace.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
