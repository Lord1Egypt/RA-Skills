## Description:

Multi-role AI stock research team that analyzes A-share and U.S. stocks with technical, fundamental, macro, sentiment, bull-bear debate, trading strategy, risk review, and a director verdict with a composite score.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[charonling](https://clawhub.ai/user/charonling)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to request A-share or U.S. stock analysis, quick stock summaries, or side-by-side comparisons. It drafts structured research reports with data collection, analyst viewpoints, trading posture, risk review, and a final composite score.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup script installs Python packages and persistently registers a local stock-analyzer MCP server in supported AI clients.

Mitigation: Review setup.sh before running it, install only in trusted environments, and remove the server with uninstall.sh when it is no longer needed.

Risk: publish.sh can initialize a repository and push the full skill contents to a public GitHub repository if run intentionally.

Mitigation: Do not run publish.sh unless public publication is intended, and review repository contents before using it.

Risk: Generated stock reports may include market scores, price targets, stop-loss levels, and trading suggestions that can be mistaken for investment advice.

Mitigation: Treat reports as informational only and verify market data and recommendations with qualified financial review before acting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/charonling/skills/stock-research-team)
- [Python requirements](references/requirements.txt)
- [HTML report template](assets/report-template.html)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report with structured analyst sections, scores, trading posture, risk factors, and disclaimer text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include stock scores, price targets, stop-loss levels, and generated timestamps.]

## Skill Version(s):

1.0.0 (source: frontmatter, changelog, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
