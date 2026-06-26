## Description: <br>
TMR Land personal agent for an AI business marketplace. Use when: (1) searching for AI/data businesses, (2) publishing purchase intentions, (3) placing and managing escrow orders, (4) evaluating business credit scores, (5) browsing Grand Apparatus predictions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cpy1990](https://clawhub.ai/user/cpy1990) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to interact with the TMR Land marketplace: finding AI/data businesses, publishing purchase intentions, negotiating, managing escrow orders, checking wallet and KYC status, reviewing providers, and evaluating business reputation and credit signals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can affect funds, escrow, orders, disputes, reviews, marketplace state, and KYC workflows through the user's TMR Land API key. <br>
Mitigation: Use the narrowest API-key permissions available and require explicit per-action approval before wallet withdrawals, payments, escrow release, KYC submission, dispute creation, data deletion, or deal acceptance. <br>
Risk: Wallet, KYC, message, receipt, and business workflow responses may expose sensitive personal, financial, or marketplace data. <br>
Mitigation: Keep raw API keys and identity numbers out of shared logs or chats, review command output before sharing it, and redact sensitive fields when using responses in agent context. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/cpy1990/tmrland-personal-demo) <br>
- [TMR Land homepage](https://tmrland.com) <br>
- [API Keys API](references/api-keys-api.md) <br>
- [Intentions API](references/intentions-api.md) <br>
- [Businesses API](references/businesses-api.md) <br>
- [Negotiations API](references/negotiations-api.md) <br>
- [Orders API](references/orders-api.md) <br>
- [Wallet API](references/wallet-api.md) <br>
- [Disputes API](references/disputes-api.md) <br>
- [Messages API](references/messages-api.md) <br>
- [Credit API](references/credit-api.md) <br>
- [Reviews API](references/reviews-api.md) <br>
- [Notifications API](references/notifications-api.md) <br>
- [Contracts API](references/contracts-api.md) <br>
- [Grand Apparatus API](references/apparatus-api.md) <br>
- [Error Codes](references/error-codes.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with Node.js command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and the TMR_API_KEY environment variable; TMR_BASE_URL is optional.] <br>

## Skill Version(s): <br>
1.0.5 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
