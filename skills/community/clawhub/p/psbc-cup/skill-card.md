## Description:

帮助代理在可见浏览器中打开邮储银行易企收演示版或正式登录页，并根据用户意图提供功能导航指导。

This skill is ready for commercial/non-commercial use.

## Publisher:

[dayhee](https://clawhub.ai/user/dayhee)

### License/Terms of Use:

MIT-0

## Use Case:

External users and business operators use this skill to open 易企收 demo pages for feature review or reach the formal login page for payment-collection workflows such as fee item configuration, arrears upload, and payment information management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can open a payment-related login page based on broad user intent.

Mitigation: Confirm the destination and intent before entering credentials or business data, and use demo pages for informational requests.

Risk: Direct URL navigation to 易企收 subpages may return the user to the homepage.

Mitigation: Navigate through the homepage menu when a feature page does not load directly.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dayhee/skills/psbc-cup)
- [易企收正式版登录](https://openpayment.psbc.cn/new/login)
- [易企收演示版首页](https://openpayment.psbc.cn/newDemo/dashboard)

## Skill Output:

**Output Type(s):** [Guidance]

**Output Format:** [Concise text or Markdown with browser-navigation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Opens disclosed 易企收 demo or login pages in a visible browser when browser automation is available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
