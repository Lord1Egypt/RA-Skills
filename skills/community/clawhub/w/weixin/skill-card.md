## Description: <br>
Weixin is a WeChat ecosystem development assistant for Official Accounts, Mini Programs, WeChat Pay V3, and Enterprise WeChat integrations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangifonly](https://clawhub.ai/user/zhangifonly) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill for implementation guidance and examples across WeChat Official Account backends, Mini Program login and cloud development, WeChat Pay V3 orders and notifications, JSSDK setup, and Enterprise WeChat integrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Credential exposure through WeChat AppSecret, access_token, session_key, or payment keys used in example workflows. <br>
Mitigation: Keep secrets server-side, avoid pasting real credentials into chat, and use test accounts where possible. <br>
Risk: Production-impacting changes from examples that create menus, send messages, create orders, issue refunds, or handle payment notifications. <br>
Mitigation: Review generated code and commands before use, validate payment signatures and notification idempotency, and test against non-production accounts before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhangifonly/weixin) <br>
- [Publisher profile](https://clawhub.ai/user/zhangifonly) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline code blocks and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only output; examples may reference live WeChat APIs and credential placeholders.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
