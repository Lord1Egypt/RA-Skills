## Description:

广告投放优化 is a cross-border paid ads optimization coach for Meta, TikTok, and Google Ads across targeting, creatives, bidding, landing pages, and analytics using the Yufluent cloud service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[metahuan](https://clawhub.ai/user/metahuan)

### License/Terms of Use:

MIT-0

## Use Case:

External commerce operators and advertising teams use this skill to request structured optimization guidance for paid ad campaigns, including targeting, creative testing, bidding, landing page review, and analytics follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ad performance metrics, campaign names, product details, market information, and account context may be sent to Yufluent's cloud service under the user's TOKENAPI_KEY.

Mitigation: Share only the fields needed for the optimization request, exclude platform credentials, customer data, cookies, raw exports, and unrelated secrets, and review Yufluent data handling terms before use.

Risk: The main optimization answer is produced through the vendor service, and evidence reports limited detail about user control over the submitted context.

Mitigation: Confirm the platform, optimization dimension, metrics payload, and data-sharing approval before running the skill; review any recommendations before applying changes in an ad platform.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/metahuan/skills/yufluentcn-ad-optimize)
- [Yufluent ad optimize homepage](https://www.changzhiai.com/skills/ad-optimize)
- [OpenClaw integration](https://claw.changzhiai.com/app/openclaw)
- [Yufluent console](https://claw.changzhiai.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text optimization guidance returned by the skill runner.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TOKENAPI_KEY; the skill does not directly modify ad accounts or automatically change bids.]

## Skill Version(s):

1.1.3 (source: server release metadata; artifact frontmatter reports 1.1.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
