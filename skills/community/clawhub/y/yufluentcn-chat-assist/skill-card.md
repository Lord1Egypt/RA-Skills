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
Risk: Customer-support messages and possible order context are sent to Yufluent's remote API. <br>
Mitigation: Use the skill only when that remote data flow is acceptable, and redact unnecessary sensitive customer or order data before running it. <br>
Risk: The skill requires a bearer token through TOKENAPI_KEY. <br>
Mitigation: Store the token in an environment variable or secrets manager, rotate it if exposed, and avoid placing it in prompts, logs, or shared files. <br>
Risk: TOKENAPI_BASE_URL can redirect requests to a different service. <br>
Mitigation: Keep TOKENAPI_BASE_URL unset or restricted to the intended trusted HTTPS endpoint. <br>
Risk: Broad activation triggers may cause the skill to run in support conversations where remote processing is not expected. <br>
Mitigation: Confirm user intent before sending buyer messages or order context to the remote API. <br>
Risk: Reply drafts may include wording that does not match the seller's actual policy, authorization, or platform obligations. <br>
Mitigation: Review every draft before sending and remove unsupported promises about refunds, compensation, delivery dates, or review changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/metahuan/yufluentcn-chat-assist) <br>
- [Publisher profile](https://clawhub.ai/user/metahuan) <br>
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
