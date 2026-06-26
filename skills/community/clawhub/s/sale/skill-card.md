## Description: <br>
Autonomously manage SendClaw email outreach by sending, receiving, and replying to email for task-oriented communication with existing contacts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codejika](https://clawhub.ai/user/codejika) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to register and operate a SendClaw inbox for limited daily email outreach, inbox checks, replies, verification workflows, and task-oriented professional correspondence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create and operate a third-party email inbox and send or reply to email on behalf of a user. <br>
Mitigation: Require explicit user approval before account creation, sending or replying to email, signing up for services, using verification codes, or enabling webhooks. <br>
Risk: The sales and outreach framing conflicts with the artifact's acceptable-use limits against sales, marketing, cold outreach, spam, phishing, impersonation, and deceptive content. <br>
Mitigation: Use only for existing-contact or task-oriented correspondence where recipient consent, retention, and access rules are clear. <br>
Risk: The API key and claim token grant access to the agent inbox and account management flow. <br>
Mitigation: Treat API keys and claim tokens as secrets, avoid exposing them in logs or messages, and share claim tokens only with the account owner. <br>
Risk: Webhook delivery can expose message metadata to an external endpoint. <br>
Mitigation: Enable webhooks only for trusted endpoints and keep polling as a fallback when webhook handling is not needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/codejika/sale) <br>
- [SendClaw homepage](https://sendclaw.com) <br>
- [SendClaw API base](https://sendclaw.com/api) <br>
- [SendClaw skill reference](https://sendclaw.com/skill.md) <br>
- [SendClaw heartbeat reference](https://sendclaw.com/heartbeat.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with HTTP and JSON examples; outbound and inbound email text through the SendClaw API] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a SendClaw API key after registration; produces an agent inbox, claim token, optional webhook configuration, and rate-limited email activity.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
