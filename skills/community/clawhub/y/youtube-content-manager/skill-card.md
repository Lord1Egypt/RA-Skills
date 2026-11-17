## Description:

YouTube Content Manager is a Chinese-language tool for generating YouTube topics, scripts, SEO titles, descriptions, tags, thumbnail copy, publishing records, and basic performance analysis with SkillPay billing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baolige2023](https://clawhub.ai/user/baolige2023)

### License/Terms of Use:

MIT-0

## Use Case:

External YouTube creators and channel operators use this skill to generate Chinese-language content ideas and draft video assets, then track publishing metrics in a local dashboard.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Embedded payment and AI API keys could expose live-looking credentials.

Mitigation: Remove embedded keys, rotate affected secrets, and load credentials from a managed secret store or environment variables.

Risk: Content is sent to SkillPay and SiliconFlow without clear disclosure in the release evidence.

Mitigation: Disclose the payment and AI-provider data flows, including what user content is sent and when.

Risk: Billing behavior and user confirmation steps may not match the advertised per-use charge.

Mitigation: Align displayed fees, payment-link amounts, charge amounts, and confirmation screens before enabling real billing.

Risk: Public debug serving without authentication, authorization, or CSRF protection could expose user data and paid actions.

Mitigation: Disable debug/public serving for release, require authentication and authorization, and add CSRF protection to state-changing routes.

Risk: AI-generated and user-provided content may be rendered into the dashboard unsafely.

Mitigation: Sanitize or safely escape dynamic content before rendering it in the browser.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/baolige2023/skills/youtube-content-manager)
- [SkillPay billing endpoint](https://skillpay.me/api/v1/billing)
- [SiliconFlow chat completions endpoint](https://api.siliconflow.cn/v1/chat/completions)

## Skill Output:

**Output Type(s):** [text, json, configuration, guidance]

**Output Format:** [JSON API responses and Chinese-language dashboard text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces topic lists, scripts, titles, SEO descriptions, tags, thumbnail copy, publishing records, and analytics summaries.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
