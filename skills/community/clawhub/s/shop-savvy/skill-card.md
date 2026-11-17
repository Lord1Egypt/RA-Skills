## Description:

Shop Savvy helps agents compare products, search discounts, summarize reviews, analyze value, and advise purchase timing across common shopping categories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill for shopping decisions, including product comparison, coupon and discount search, review summarization, value analysis, and purchase-timing advice. It is intended to help agents produce concise buying guidance rather than execute purchases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can store usage history and user preferences in its directory.

Mitigation: Review, minimize, or disable the learner workflow before use, and provide a way to inspect and delete learned_patterns.json.

Risk: The learning workflow can feed learned content back into skill instructions.

Mitigation: Require human review before any learned content is written back to SKILL.md or otherwise changes agent behavior.

Risk: Shopping recommendations may be based on incomplete or stale web information.

Mitigation: Ask the agent to cite current sources for prices, coupons, reviews, and availability before acting on purchase advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qq435912743/skills/shop-savvy)
- [ClawHub publisher profile](https://clawhub.ai/user/qq435912743)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands]

**Output Format:** [Markdown with structured comparison tables, recommendation summaries, and optional shell command snippets for the learning helper]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May rely on web search results and local learned_patterns.json history when the learning workflow is used.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
