## Description: <br>
Automates Remnawave account creation, internal squad assignment, subscription retrieval, onboarding email delivery, account lookup, account updates, and local creation logging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[uepuer](https://clawhub.ai/user/uepuer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operations and administrative users use this skill to create and manage Remnawave user accounts, assign internal squads, retrieve subscription details, send onboarding email, and run follow-up search or verification workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Privileged Remnawave account operations can create, modify, delete, search, email, and store sensitive user account data. <br>
Mitigation: Install only in a controlled admin environment, use least-privilege Remnawave and SMTP credentials, and require confirmation before create, delete, or group-change actions. <br>
Risk: Subscription URLs, generated passwords, account identifiers, and recipient data can appear in terminal output, onboarding email, or local logs. <br>
Mitigation: Redact subscription URLs and generated passwords from output and logs, restrict log access, and verify every recipient and CC before sending onboarding email. <br>
Risk: TLS certificate verification may be disabled for Remnawave or SMTP configuration. <br>
Mitigation: Enable certificate verification where possible and use trusted certificates in production environments. <br>
Risk: Automatic delete-and-retry behavior can remove existing accounts unexpectedly. <br>
Mitigation: Remove the automatic delete-and-retry path or require explicit human approval with confirmed account identity before deletion. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/uepuer/remnawave-account-creator) <br>
- [README](artifact/README.md) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [Workflow guide](artifact/WORKFLOW.md) <br>
- [API reference](artifact/API-REFERENCE.md) <br>
- [Account search SOP](artifact/SOP-搜索账号.md) <br>
- [Squad update SOP](artifact/SOP-更新分组.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with command-line examples, JSON configuration snippets, and script output text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce Remnawave account identifiers, subscription URLs, email delivery status, and local log entries that can contain sensitive account data.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
