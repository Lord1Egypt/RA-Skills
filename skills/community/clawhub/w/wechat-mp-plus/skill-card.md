## Description:

Automate WeChat Official Account management with draft publishing, menu editing, auto-reply checking, and Markdown-to-HTML formatting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huuuwnnn-droid](https://clawhub.ai/user/huuuwnnn-droid)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators who manage WeChat Official Accounts use this skill to create drafts from Markdown, upload article images, inspect auto-reply rules, and manage custom menus.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use high-impact WeChat Official Account access through AppID and AppSecret credentials.

Mitigation: Install only from a trusted publisher, run in a controlled environment, and test with a non-production WeChat account first.

Risk: AppSecret values may be exposed if stored in repositories, logs, or shell history.

Mitigation: Keep credentials in environment variables or protected secret files and avoid committing or echoing them.

Risk: Publishing workflows process Markdown and local image paths that may come from untrusted sources.

Mitigation: Avoid untrusted Markdown, review local image paths before upload, and inspect formatted content before creating drafts.

Risk: Draft and menu delete commands can affect account content without an additional confirmation step.

Mitigation: Review command arguments carefully and restrict delete operations to accounts and environments where rollback is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huuuwnnn-droid/skills/wechat-mp-plus)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, environment configuration, and JSON examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create WeChat drafts, menus, uploaded media, and formatted HTML through WeChat API calls when executed.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
