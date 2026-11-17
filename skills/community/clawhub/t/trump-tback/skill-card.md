## Description:

Trump Tback analyzes Trump-related post text and engagement data with a T-Back sentiment framework to classify promotional, threat-oriented, or neutral market-sentiment signals.

This skill is for research and development only.

## Publisher:

[kai157isme-lgtm](https://clawhub.ai/user/kai157isme-lgtm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to analyze Trump-related social posts, engagement data, daily aggregates, and cross-platform signals for research or entertainment-oriented market-sentiment review. Its scores and warnings should not be treated as investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may overinterpret T-Back scores, market-sensitivity labels, or hedge-style warnings as investment advice.

Mitigation: Present outputs as research or entertainment signals only and require independent review before any financial decision.

Risk: Optional market-data functions may contact yfinance when called.

Mitigation: Run the local text analysis functions without market-data calls when network access is not approved or external data access is not desired.

Risk: The skill is Chinese-first and narrowly focused on Trump-related market sentiment.

Mitigation: Review the language, framing, and domain fit before deploying it to users or workflows outside that intended context.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kai157isme-lgtm/skills/trump-tback)
- [Skill homepage](https://github.com/trump-mood-dashboard)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with Python code snippets and JSON-like analysis dictionaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces sentiment scores, T-Back levels, keyword groups, viral momentum summaries, daily aggregates, and cross-platform resonance alerts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
