## Description:

用户反馈虾 analyzes Chinese user reviews, complaints, NPS responses, and support feedback to identify sentiment, recurring issue themes, priorities, and product improvement recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tujinsama](https://clawhub.ai/user/tujinsama)

### License/Terms of Use:

MIT-0

## Use Case:

Product, operations, and customer support teams use this skill to turn Chinese-language customer feedback from reviews, support tickets, surveys, and pasted text into prioritized issue analysis and action recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Customer feedback may contain personal, customer, or confidential business information.

Mitigation: Redact sensitive information before supplying feedback datasets to the agent.

Risk: Chinese NLP sentiment and theme classification can produce incorrect labels, especially for dialect, slang, or ambiguous comments.

Mitigation: Review outputs manually and spot-check representative samples before using the analysis for product decisions.

Risk: Small datasets can produce weak or misleading priority rankings.

Mitigation: Treat analyses of fewer than 50 feedback items as directional only and disclose the sample-size limitation.

## Reference(s):

- [Improvement Templates](references/improvement-templates.md)
- [Issue Taxonomy](references/issue-taxonomy.md)
- [Sentiment Lexicon](references/sentiment-lexicon.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown analysis report with tables, representative feedback excerpts, trend observations, and prioritized recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on user-provided feedback data; the skill instructs agents to state limited reliability for samples under 50 items.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
