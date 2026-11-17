## Description:

Generates customer-service reply drafts for Amazon, Shopify, and TikTok Shop buyer messages through a Yufluent cloud service with messaging guardrails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[metahuan](https://clawhub.ai/user/metahuan)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce sellers and support operators use this skill to draft buyer-message replies for logistics, refunds, product questions, and service recovery across Amazon, Shopify, and TikTok Shop. The generated reply is intended as a human-reviewed draft before sending through the seller's platform.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends buyer messages, order context, and API credentials through a Yufluent cloud service.

Mitigation: Avoid sending unnecessary personal data, order identifiers, or tracking details, and keep TOKENAPI_KEY out of commits and logs.

Risk: The runtime depends on an unreviewed Python client loaded through broad path manipulation.

Mitigation: Install only from a source that includes or verifies the yufluent_api client, and prefer pinned dependencies for reproducible installs.

Risk: Generated replies may contain inaccurate logistics, refund, or compensation language if the order context is incomplete.

Mitigation: Provide verified order context where available and review every draft before sending through Seller Central, Shopify Inbox, or TikTok seller tools.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/metahuan/skills/yufluentcn-chat-assist)
- [Yufluent Chat Assist homepage](https://www.changzhiai.com/skills/chat-assist)
- [OpenClaw documentation](https://claw.changzhiai.com/app/openclaw)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text reply draft, with Markdown and shell command examples in the skill documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reply drafts are typically 2-5 sentences and require seller review before sending.]

## Skill Version(s):

1.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
