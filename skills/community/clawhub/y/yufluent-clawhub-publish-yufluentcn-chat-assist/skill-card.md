## Description:

Generates human-reviewed customer-service reply drafts for Amazon, Shopify, and TikTok Shop buyer messages using buyer text and optional order context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[metahuan](https://clawhub.ai/user/metahuan)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce sellers and support agents use this skill to draft concise buyer-message replies for logistics questions, refunds, returns, product questions, and review-sensitive conversations. The generated response is intended for human review before sending through Seller Central, Shopify Inbox, or TikTok Shop tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Customer messages, order context, and the API token may be sent to a user-configured service endpoint, including plain HTTP.

Mitigation: Configure only a trusted HTTPS TOKENAPI_BASE_URL and avoid sending unnecessary personal, order, or sensitive data in prompts.

Risk: Generated replies may contain incorrect commitments, unsupported refund or replacement language, or statements that conflict with marketplace policy.

Mitigation: Require seller or support-agent review before sending replies, especially for refunds, compensation, shipping status, reviews, and platform-policy-sensitive cases.

Risk: Dependency behavior can change if packages are installed without pinning.

Mitigation: Install dependencies in an isolated environment and pin package versions for production support workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/metahuan/skills/yufluent-clawhub-publish-yufluentcn-chat-assist)
- [Yufluent homepage](https://claw.changzhiai.com)
- [Yufluent OpenClaw setup](https://claw.changzhiai.com/app/openclaw)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text customer-service reply draft with command-line status metadata on stderr]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Replies are typically 2-5 sentences and require human review before seller use.]

## Skill Version(s):

1.1.2 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
