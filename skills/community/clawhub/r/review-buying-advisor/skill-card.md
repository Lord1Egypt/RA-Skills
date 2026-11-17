## Description:

Analyze a product from name plus platform, read public reviews, and turn evidence into a practical buying recommendation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to evaluate whether a product is worth buying by asking an agent to inspect accessible public reviews, summarize recurring positives and risks, and give a practical recommendation with confidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product review access may be blocked, sparse, or incomplete, which can make a recommendation uncertain.

Mitigation: State what review evidence was accessible, switch to a limited conclusion when needed, and lower confidence instead of presenting unsupported certainty.

Risk: A product name may map to multiple listings, variants, or platforms, causing review evidence to apply to the wrong item.

Mitigation: Ask one clarifying question when identification is ambiguous and avoid variant-specific claims unless the variant is clear.

Risk: Public reviews may include generic, promotional, shipping-only, or unrepresentative comments.

Mitigation: Use representative samples across positive, negative, mixed, and recent reviews, downweight weak comments, and separate repeated issues from isolated complaints.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/harrylabsj/skills/review-buying-advisor)
- [Publisher profile](https://clawhub.ai/user/harrylabsj)

## Skill Output:

**Output Type(s):** [guidance, text, markdown]

**Output Format:** [Markdown recommendation with verdict, evidence summary, buyer fit, positives, risks, checks before purchase, final advice, and confidence.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce a limited low-confidence conclusion when public review evidence is blocked, weak, ambiguous, or incomplete.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
