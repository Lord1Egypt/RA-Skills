## Description:

Quant Strategy Searcher searches quantitative stock strategies, retrieves strategy holdings, and produces traceable stock analysis using financial, market, news, and prospectus-style data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gdyz](https://clawhub.ai/user/gdyz)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to search quantitative equity strategies, retrieve holdings from a remote strategy database, and generate financial, news, and risk-oriented stock analysis for reference.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill connects to a remote strategy database using DB_PASSWORD.

Mitigation: Use a dedicated least-privilege database password that is not shared with production systems, and rotate it if exposed.

Risk: Proxy environment variables may contain credentials or alter data access behavior.

Mitigation: Avoid running the skill with credential-bearing proxy variables unless they are required and reviewed.

Risk: Financial and news analysis is generated from third-party data and should not be treated as verified investment advice.

Mitigation: Review cited source links and keep human approval in any investment decision workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gdyz/skills/quant-strategy-searcher)
- [ClawHub homepage metadata](https://clawhub.ai/GDYZ/quant-strategy-searcher)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown and structured text with JSON-shaped analysis sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include stock scores, confidence notes, data-source links, financial indicators, news sentiment summaries, strategy matches, and follow-up analysis responses.]

## Skill Version(s):

2.1.0 (source: server release metadata; artifact frontmatter says 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
