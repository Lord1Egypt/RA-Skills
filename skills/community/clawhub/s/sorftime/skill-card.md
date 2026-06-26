## Description: <br>
Provides guidance for using the sorftime-cli package to call Sorftime ecommerce data APIs across Amazon, Shopee, and Walmart. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangfaguo](https://clawhub.ai/user/zhangfaguo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, ecommerce operators, and data analysts use this skill to install and authenticate sorftime-cli, then compose CLI calls for bulk product, category, keyword, monitoring, account, and cross-platform analytics workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Sorftime Account-SK credentials for authenticated API access. <br>
Mitigation: Protect the Account-SK like a password, keep it out of shared logs or prompts, and verify the active profile before issuing commands. <br>
Risk: Account-changing commands can delete profiles or monitoring subscriptions. <br>
Mitigation: Require explicit user confirmation before deletions, subscription changes, or other account-state changes. <br>
Risk: High-volume requests, monitoring subscriptions, and image uploads may consume paid credits or account quota. <br>
Mitigation: Confirm the intended volume and check request or credit balance before running batch, monitoring, upload, or recurring workflows. <br>


## Reference(s): <br>
- [Sorftime CLI quick reference](README.md) <br>
- [Sorftime CLI skill guide](SKILL.md) <br>
- [Common CLI reference, domain table, and error codes](resources/_common.md) <br>
- [Account management endpoints](resources/account.md) <br>
- [Amazon workflow recipes](resources/amazon-recipes.md) <br>
- [Sorftime CLI GitHub repository](https://github.com/sorftime/sorftime-cli) <br>
- [sorftime-cli npm package](https://www.npmjs.com/package/sorftime-cli) <br>
- [Sorftime CLI account setup](https://www.sorftime.com/cli) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, code] <br>
**Output Format:** [Markdown with inline shell commands and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include API endpoint names, domain IDs, JSON request payloads, and credential-handling reminders.] <br>

## Skill Version(s): <br>
0.1.10 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
