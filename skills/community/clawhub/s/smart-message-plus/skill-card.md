## Description:

Cross-platform enterprise messaging skill for sending user-provided messages through DingTalk, Feishu/Lark enterprise apps, and WeCom group robot webhooks with aliases, templates, media, recalls where supported, onboarding, and configurable approval gates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[songhonglei](https://clawhub.ai/user/songhonglei)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, IT operators, and developers use this skill to configure enterprise messaging accounts and send user-provided messages across DingTalk, Feishu/Lark, and WeCom from an agent-controlled CLI. It is suited for operational notices, group messaging, department broadcasts, media delivery, and account or contact setup where enterprise credentials and approval controls are managed by the workspace operator.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Outbound messages, local file uploads, send logs, recipient identifiers, or webhook secrets could be disclosed beyond the intended scope.

Mitigation: Install only in trusted workspaces, store credentials with least privilege, treat send logs as sensitive, and review recipient, file, and message content before sending.

Risk: Untrusted aliases, templates, or custom organization lookup services could redirect messages or expose directory data.

Mitigation: Use trusted aliases and templates, prefer official HTTPS endpoints for organization lookup, and avoid non-HTTPS or untrusted custom lookup services.

Risk: Large broadcasts can reach many recipients quickly if approval controls are bypassed or disabled.

Mitigation: Keep the configurable safety gate enabled, use dry runs for broadcast previews, and require force-send or content-bound admin approval codes above configured thresholds.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/songhonglei/skills/smart-message-plus)
- [Provider Matrix](references/provider-matrix.md)
- [Console Setup](references/console-setup.md)
- [Org Lookup Contract](references/org-lookup-contract.md)
- [Design Notes](docs/design.md)
- [Add Channel Guide](docs/add-channel.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and CLI-oriented text with shell commands, configuration snippets, and structured send results from the bundled Python scripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill requires user-provided message content and may create local configuration, contact alias, token cache, and send log files in its runtime data directory.]

## Skill Version(s):

2.1.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
