## Description:

基于道家理念，构建知识智能体分发系统，支持深度阅读、知识连接、资产加密、数字分身与微信生态变现。

This skill is ready for commercial/non-commercial use.

## Publisher:

[interccy-stack](https://clawhub.ai/user/interccy-stack)

### License/Terms of Use:

MIT-0

## Use Case:

External content creators and developers use this skill to organize personal knowledge, generate structured notes and digital persona assets, protect or share knowledge files, and prepare monetized distribution workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mailbox automation and local-note indexing require access to sensitive communications and personal knowledge files.

Mitigation: Install and run the skill only when that level of mailbox and local-file access is acceptable for the intended environment.

Risk: The automatic fulfillment workflow can be used around payment and referral handling.

Mitigation: Use separate verified payment-provider checks before fulfilling real purchases or issuing paid access.

Risk: Secrets may be exposed if mailbox passwords or API tokens are stored in project files.

Mitigation: Keep secrets in environment variables or a managed secret store and avoid committing configuration files that contain credentials.

Risk: Encryption and ephemeral sharing features are described as convenience protection rather than strong confidentiality.

Mitigation: Treat encrypted or self-destructing bundles as limited-protection artifacts until the KDF, backup, overwrite, and disclosure issues are fixed.

Risk: Pinned dependencies may lag security fixes.

Mitigation: Review and upgrade pinned dependencies before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/interccy-stack/skills/zero-one-two-three)
- [README_EN.md](artifact/README_EN.md)
- [README.md](artifact/README.md)
- [Published demo link](https://speech.actoncode.cn/agent/chat?vid=6222474042&userId=5619137)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated local artifacts such as reports, encrypted bundles, audio files, and knowledge indexes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require local files, mailbox credentials, API tokens, Python dependencies, and optional model downloads depending on the workflow]

## Skill Version(s):

1.0.16 (source: server release metadata; artifact frontmatter lists 16.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
