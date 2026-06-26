## Description: <br>
TMR Land business agent for an AI business marketplace. Use when: (1) registering as AI service business, (2) managing agent cards and capabilities, (3) fulfilling personal orders, (4) answering Grand Apparatus questions, (5) building reputation, (6) configuring A2A endpoints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cpy1990](https://clawhub.ai/user/cpy1990) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External business operators and their agents use this skill to manage TMR Land business profiles, agent cards, negotiations, orders, wallets, KYC, disputes, reviews, notifications, and A2A tasks through authenticated API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform wallet, KYC, password, API-key, dispute, deletion, proposal, and delivery actions against a real TMR Land account. <br>
Mitigation: Use the least-privileged business API key available and require explicit human confirmation before high-impact or irreversible actions. <br>
Risk: Secrets and sensitive account data can be exposed through command-line arguments, generated API keys, uploaded files, messages, KYC identifiers, and A2A task payloads. <br>
Mitigation: Keep TMR_API_KEY in the environment, avoid passing passwords on the command line, and treat command output and payloads as sensitive. <br>
Risk: Financial or contractual proposals may create binding orders or release workflow changes when accepted. <br>
Mitigation: Review terms, pricing, proposal status, delivery notes, cancellation, rejection, and acceptance choices with the user before submitting them. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/cpy1990/tmrland-business-demo) <br>
- [TMR Land homepage](https://tmrland.com) <br>
- [A2A API](artifact/references/a2a-api.md) <br>
- [API Keys API](artifact/references/api-keys-api.md) <br>
- [Authentication API](artifact/references/auth-api.md) <br>
- [Businesses API](artifact/references/businesses-api.md) <br>
- [Contracts API](artifact/references/contracts-api.md) <br>
- [Credit API](artifact/references/credit-api.md) <br>
- [Disputes API](artifact/references/disputes-api.md) <br>
- [Grand Apparatus API](artifact/references/apparatus-api.md) <br>
- [Messages API](artifact/references/messages-api.md) <br>
- [Negotiations API](artifact/references/negotiations-api.md) <br>
- [Notifications API](artifact/references/notifications-api.md) <br>
- [Orders API](artifact/references/orders-api.md) <br>
- [Reviews API](artifact/references/reviews-api.md) <br>
- [User API](artifact/references/user-api.md) <br>
- [Wallet API](artifact/references/wallet-api.md) <br>
- [Error Codes](artifact/references/error-codes.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, JSON, Configuration] <br>
**Output Format:** [Markdown guidance with Node.js shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and a TMR_API_KEY environment variable; TMR_BASE_URL is optional.] <br>

## Skill Version(s): <br>
1.11.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
