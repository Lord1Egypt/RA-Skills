## Description: <br>
Provides Alipay API reference material for agent-assisted development. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lentiancn](https://clawhub.ai/user/lentiancn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to look up Alipay Open Platform API parameters, request and response fields, error codes, and workflow notes while building or reviewing Alipay integrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill references sensitive payment, authorization, merchant identity, bank, settlement, phone, and certificate data. <br>
Mitigation: Use sandbox or test credentials where possible, avoid logging or hardcoding secrets, redact examples before sharing, and handle tokens and identity data as sensitive. <br>
Risk: The referenced Alipay operations include mutating actions such as create, confirm, cancel, upload, and onboarding workflows. <br>
Mitigation: Require explicit confirmation before running mutating Alipay API calls and review parameters before execution. <br>


## Reference(s): <br>
- [Alipay API index](references/apidocs/apis.md) <br>
- [alipay.open.agent.common.sign](references/apidocs/alipay.open.agent.common.sign.md) <br>
- [alipay.open.agent.commonsign.confirm](references/apidocs/alipay.open.agent.commonsign.confirm.md) <br>
- [alipay.open.agent.create](references/apidocs/alipay.open.agent.create.md) <br>
- [alipay.open.agent.order.query](references/apidocs/alipay.open.agent.order.query.md) <br>
- [alipay.open.agent.signstatus.query](references/apidocs/alipay.open.agent.signstatus.query.md) <br>
- [alipay.open.auth.token.app](references/apidocs/alipay.open.auth.token.app.md) <br>
- [alipay.open.file.upload](references/apidocs/alipay.open.file.upload.md) <br>
- [alipay.open.sp.inteop.appauth.create](references/apidocs/alipay.open.sp.inteop.appauth.create.md) <br>
- [alipay.open.sp.inteop.order.cancel](references/apidocs/alipay.open.sp.inteop.order.cancel.md) <br>
- [alipay.open.sp.inteop.order.confirm](references/apidocs/alipay.open.sp.inteop.order.confirm.md) <br>
- [alipay.open.sp.inteop.order.create](references/apidocs/alipay.open.sp.inteop.order.create.md) <br>
- [alipay.open.sp.inteop.order.query](references/apidocs/alipay.open.sp.inteop.order.query.md) <br>
- [alipay.open.sp.inteop.product.create](references/apidocs/alipay.open.sp.inteop.product.create.md) <br>
- [alipay.open.sp.inteop.settle.create](references/apidocs/alipay.open.sp.inteop.settle.create.md) <br>
- [alipay.open.sp.inteop.sync.notify](references/apidocs/alipay.open.sp.inteop.sync.notify.md) <br>
- [ant.merchant.expand.bizaccess.order.cancel](references/apidocs/ant.merchant.expand.bizaccess.order.cancel.md) <br>
- [ant.merchant.expand.bizaccess.order.check](references/apidocs/ant.merchant.expand.bizaccess.order.check.md) <br>
- [ant.merchant.expand.bizaccess.order.create](references/apidocs/ant.merchant.expand.bizaccess.order.create.md) <br>
- [ant.merchant.expand.bizaccess.order.query](references/apidocs/ant.merchant.expand.bizaccess.order.query.md) <br>
- [ant.merchant.expand.indirect.image.upload](references/apidocs/ant.merchant.expand.indirect.image.upload.md) <br>
- [Official Alipay Open Docs](https://opendocs.alipay.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown reference guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only; does not provide executable tools or direct API calls.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
