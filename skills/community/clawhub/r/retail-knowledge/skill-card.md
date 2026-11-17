## Description:

Product knowledge Q&A and policy lookup for retail digital employees using the configured knowledge base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fangwei-frank](https://clawhub.ai/user/fangwei-frank)

### License/Terms of Use:

MIT-0

## Use Case:

Retail digital employees and customer-facing agents use this skill to answer product, policy, promotion, FAQ, store information, and membership questions from a configured store knowledge base.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The configured knowledge base may contain information that should not be disclosed to customers or staff.

Mitigation: Review the knowledge base before deployment and include only content appropriate for the intended retail assistant audience.

Risk: Retail answers about prices, promotions, and inventory can become stale when freshness metadata is missing or outdated.

Mitigation: Maintain accurate knowledge-base freshness metadata and add caveats or hand off when the data is beyond the configured staleness threshold.

Risk: Broad retail triggers may cause the skill to answer questions that should be handled by recommendation, inventory, or complaint workflows.

Mitigation: Keep routing rules enabled so recommendation, inventory, and complaint requests are handed off to their dedicated skills.

## Reference(s):

- [Answer Style Guide](references/answer-style-guide.md)
- [Conversation Patterns](references/conversation-patterns.md)
- [Knowledge Base Schema Reference](references/kb-schema.md)
- [Knowledge Base Search Strategy](references/search-strategy.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown or plain text answers, with JSON search results from the local helper when used.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Answers should be grounded in the configured knowledge base and use fallback responses when the relevant domain is missing.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
