## Description:

Scrapes Reddit stock forums, fetches market data, and uses DeepSeek to produce short-term stock-pick analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[altusrossouw](https://clawhub.ai/user/altusrossouw)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to summarize Reddit stock sentiment, combine it with Yahoo Finance market data, and generate AI-assisted stock-pick analysis for the next week. The output is entertainment or research input and should not be treated as financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The web app can expose an unauthenticated analysis endpoint that may spend the user's DeepSeek API credits.

Mitigation: Deploy behind authentication, rate limits, and monitoring; avoid public exposure unless these controls are in place.

Risk: The skill sends Reddit and market-analysis context to DeepSeek and fetches data from Yahoo Finance.

Mitigation: Install only when this data sharing is acceptable and avoid including private or regulated information in analysis prompts.

Risk: The web UI may render untrusted AI or market data unsafely.

Mitigation: Sanitize rendered HTML and review UI handling before exposing web mode to other users.

Risk: Generated stock picks can be inaccurate or misleading.

Mitigation: Treat outputs as entertainment or research input only, retain the financial disclaimer, and require human review before any investment decision.

Risk: Dependencies are specified with lower bounds rather than pinned versions.

Mitigation: Pin and review dependencies in production deployments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/altusrossouw/skills/reddit-stonks)
- [Project homepage from ClawHub metadata](https://github.com/AltusRossouw/reddit-stonks)
- [DeepSeek API endpoint used by the skill](https://api.deepseek.com/v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown analysis with stock tables, ranked picks, risk notes, confidence score, and optional European ticker equivalents]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CLI and web modes require DEEPSEEK_API_KEY; web mode streams results over server-sent events.]

## Skill Version(s):

1.1.1 (source: server release evidence; artifact frontmatter says 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
