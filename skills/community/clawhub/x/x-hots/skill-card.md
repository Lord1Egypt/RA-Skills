## Description:

Fetch trending topics from X (Twitter), match them to user interests, and summarize their background, opinions, and controversies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiangsier-xyz](https://clawhub.ai/user/jiangsier-xyz)

### License/Terms of Use:

MIT-0

## Use Case:

People tracking news and social conversations use this skill to identify X trends in their areas of interest and review the background, differing opinions, and controversies behind them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reading X trends requires access to an already logged-in browser session.

Mitigation: Enable the skill only if access to that X session is acceptable; restore login before fetching rather than reporting logged-out results.

Risk: Optional API fallback may miss popular posts and only searches English-language results.

Mitigation: Provide an API token only when fallback is wanted, label fallback results as partial, and do not present them as a complete view of hot topics.

## Reference(s):

- [X (Twitter) Hot Topics on ClawHub](https://clawhub.ai/jiangsier-xyz/skills/x-hots)

## Skill Output:

**Output Type(s):** [Markdown, Text analysis]

**Output Format:** [Markdown topic summaries organized by interest area]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Topics are ranked by engagement; API fallback results are identified as partial.]

## Skill Version(s):

2.0.1 (source: skill frontmatter and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
