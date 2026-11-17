## Description:

Automates drafting, approval notification, and publishing of Weibo posts with text and images through Puppeteer and Feishu review messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hmyaoyuan](https://clawhub.ai/user/hmyaoyuan)

### License/Terms of Use:

ISC

## Use Case:

Social media operators and agents use this skill to prepare Weibo post drafts, send review requests, and publish approved text or image posts using a stored Weibo session. It is intended for controlled Weibo account automation with human approval before publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stored Weibo session cookies can authorize account-changing actions.

Mitigation: Use a dedicated Weibo account, restrict local access to cookies.json, and rotate the session if cookies may have been exposed.

Risk: Publishing and deletion tools can change account content without reliable code-enforced approval.

Mitigation: Run only the documented request and approval flow, and remove or gate direct publisher and deletion scripts before use with sensitive or shared accounts.

Risk: Shell-based command construction and local path handling can be unsafe with untrusted inputs.

Mitigation: Pass only trusted chat IDs, post content, and image paths; replace shell interpolation with structured process calls and validate pending records before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hmyaoyuan/skills/weibo-manager)
- [Publisher profile](https://clawhub.ai/user/hmyaoyuan)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files]

**Output Format:** [Markdown guidance with command examples, JSON pending-post records, and status notifications.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local Weibo cookies, local pending post files, optional image paths, and Feishu notification commands.]

## Skill Version(s):

1.0.2 (source: server release metadata; package.json declares 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
