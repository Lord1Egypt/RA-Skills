## Description:

Helps users negotiate prices on Xianyu by analyzing item value, generating bargaining messages, monitoring seller replies, and managing follow-up negotiation workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[robertren](https://clawhub.ai/user/robertren)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to negotiate prices on Xianyu listings, compare asking prices with reference ranges, draft seller messages, and optionally monitor seller replies after explicit consent. It is intended for marketplace bargaining assistance, not purchase execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send marketplace messages from a logged-in user account.

Mitigation: Require user review and confirmation before the first bargaining message and prefer confirmation for each seller reply or accepted price.

Risk: Scheduled monitoring can continue sending follow-up messages after setup.

Mitigation: Keep automatic monitoring disabled by default, create cron jobs only after explicit user consent, and provide stop commands for single-item and all-item monitoring.

Risk: Frequent or broad automation may trigger platform risk controls or annoy sellers.

Mitigation: Use at least a five-minute monitoring interval, limit batch bargaining to three items, and avoid repeated bargaining against the same seller.

Risk: Seller-controlled chat content may influence the LLM's negotiation decisions.

Mitigation: Treat seller messages only as negotiation input, keep the user's target price and maximum price as controlling constraints, and notify the user when a seller counteroffer exceeds the maximum price.

Risk: Marketplace transactions can involve fraud or off-platform payment pressure.

Mitigation: Keep transactions on the marketplace platform, do not place orders automatically, and recommend manual checks for valuable purchases before payment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/robertren/skills/xianyu-bargain)
- [Xianyu web marketplace](https://www.goofish.com)
- [Auto bargain guide](guides/auto-bargain.md)
- [LLM analyzer guide](guides/llm-analyzer.md)
- [Browser automation guide](guides/xianyu-browser.md)
- [Configuration reference](references/config.md)
- [Market price reference](references/market-prices.md)
- [Advanced bargaining strategies](references/advanced-strategies.md)
- [Message templates](references/message-templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with structured JSON examples and inline browser, cron, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces bargaining analysis, suggested messages, monitoring instructions, local state-file structures, and user-facing notifications; it does not place orders.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
