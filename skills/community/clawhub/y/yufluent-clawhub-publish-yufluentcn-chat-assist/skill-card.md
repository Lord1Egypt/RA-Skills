## Description: <br>
Generates human-reviewed cross-border ecommerce buyer-message reply drafts for Amazon, Shopify, and TikTok Shop using Yufluent's cloud service and platform messaging guardrails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[metahuan](https://clawhub.ai/user/metahuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External ecommerce sellers and support agents use this skill to draft buyer-message replies for logistics questions, refund requests, product questions, and review-sensitive cases. Sellers must review the draft before sending it through Amazon, Shopify, or TikTok Shop. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Buyer messages, product information, and provided order context are sent to Yufluent's cloud service. <br>
Mitigation: Redact unnecessary personal data such as full addresses, phone numbers, emails, or complete order identifiers before use. <br>
Risk: Changing TOKENAPI_BASE_URL or another base-url setting could send requests to an unintended service. <br>
Mitigation: Keep base-url settings pointed only at the intended HTTPS service. <br>
Risk: The skill requires a TOKENAPI_KEY credential for cloud execution. <br>
Mitigation: Store the token in environment variables or a secrets manager and do not include it in prompts, logs, or shared files. <br>
Risk: Reply drafts may include wording that is not appropriate for a seller's actual policy, authorization, or platform obligations. <br>
Mitigation: Review every draft before sending and remove unsupported promises about refunds, compensation, delivery dates, or review changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/metahuan/yufluent-clawhub-publish-yufluentcn-chat-assist) <br>
- [Yufluent homepage](https://claw.changzhiai.com) <br>
- [OpenClaw integration](https://claw.changzhiai.com/app/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text] <br>
**Output Format:** [Plain text buyer-message reply draft] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Typically 2-5 sentences; human review is required before sending.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
