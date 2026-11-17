## Description:

Provides Alipay Open Platform API reference material for merchant onboarding, authorization, file upload, signing, settlement, orders, and notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lentiancn](https://clawhub.ai/user/lentiancn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to look up Alipay Open Platform request parameters, responses, error codes, examples, and workflow notes for merchant signing, service-provider onboarding, token exchange, uploads, settlement, and status or notification flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill covers state-changing Alipay merchant and payment workflows, including create, confirm, cancel, upload, token, and onboarding actions.

Mitigation: Require explicit human approval before using the material to plan or execute any state-changing Alipay workflow.

Risk: The referenced workflows can involve credentials, tokens, passwords, identity numbers, business documents, and bank data.

Mitigation: Keep sensitive data out of prompts and logs where possible, and use approved secret handling and data minimization practices.

Risk: Notification-handler material may be insufficient by itself for secure webhook implementation.

Mitigation: Add independent signature verification and replay protection before implementing or deploying notification handlers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lentiancn/skills/skill-alipay)
- [Alipay API reference index](references/apidocs/apis.md)
- [alipay.open.agent.create](references/apidocs/alipay.open.agent.create.md)
- [alipay.open.agent.common.sign](references/apidocs/alipay.open.agent.common.sign.md)
- [alipay.open.auth.token.app](references/apidocs/alipay.open.auth.token.app.md)
- [alipay.open.file.upload](references/apidocs/alipay.open.file.upload.md)
- [alipay.open.sp.inteop.order.create](references/apidocs/alipay.open.sp.inteop.order.create.md)
- [alipay.open.sp.inteop.product.create](references/apidocs/alipay.open.sp.inteop.product.create.md)
- [alipay.open.sp.inteop.settle.create](references/apidocs/alipay.open.sp.inteop.settle.create.md)
- [alipay.open.sp.inteop.sync.notify](references/apidocs/alipay.open.sp.inteop.sync.notify.md)
- [ant.merchant.expand.bizaccess.order.check](references/apidocs/ant.merchant.expand.bizaccess.order.check.md)
- [ant.merchant.expand.bizaccess.order.create](references/apidocs/ant.merchant.expand.bizaccess.order.create.md)
- [ant.merchant.expand.bizaccess.order.query](references/apidocs/ant.merchant.expand.bizaccess.order.query.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown reference excerpts and prose guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only; no direct tool or API execution.]

## Skill Version(s):

1.0.4 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
