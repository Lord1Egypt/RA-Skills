## Description:

Scan trending stocks and crypto movers with live AISA market signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bibaofeng](https://clawhub.ai/user/bibaofeng)

### License/Terms of Use:

Apache-2.0

## Use Case:

External users and developers use this skill to generate timely market-momentum reports for stocks and cryptocurrencies, including top movers, volume activity, news-driven names, and watchlist ideas. The output is informational only and is not financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send AISA_API_KEY to an undocumented custom endpoint if AISA_BASE_URL is changed.

Mitigation: Run it only with a narrowly scoped AISA_API_KEY and prevent untrusted launchers, shell profiles, wrappers, or project files from setting AISA_BASE_URL.

Risk: Runtime dependencies are not pinned.

Mitigation: Prefer a release that pins dependencies, or install and run it in a controlled environment with reviewed dependency versions.

Risk: Market reports and watchlist ideas may be incorrect or unsuitable for trading decisions.

Mitigation: Treat the output as informational, verify market data independently, and do not use it as financial advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bibaofeng/skills/stock-hot)
- [AISA API endpoint](https://api.aisa.one/v1)

## Skill Output:

**Output Type(s):** [text, markdown, json]

**Output Format:** [Markdown market report with optional compact JSON summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on live market data access and the selected focus: both, stocks, or crypto.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
