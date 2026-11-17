## Description:

Stocktorch helps analyze China A-share stocks and broad market conditions using technical, financial, capital-flow, peer-comparison, and news signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fslong520](https://clawhub.ai/user/fslong520)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Stocktorch for stock-research assistance on China A-share equities and real-time market conditions. It can produce module-specific analysis or a combined report that integrates technical, financial, capital-flow, peer-comparison, and news context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stock-research outputs may be mistaken for financial advice.

Mitigation: Treat outputs as research assistance only and verify investment decisions against authoritative market data or qualified financial advice.

Risk: The skill may search the web and save generated analysis reports locally.

Mitigation: Run it only where browser-based research and local report writes are expected, and review data sources and timestamps before relying on results.

Risk: The packaged artifact contains instructions but appears to lack the referenced analysis scripts and documentation.

Mitigation: Confirm the required runtime files are present before attempting workflows such as run_skill.py.

## Reference(s):

- [Stocktorch ClawHub skill page](https://clawhub.ai/fslong520/skills/stocktorch)
- [fslong520 ClawHub publisher profile](https://clawhub.ai/user/fslong520)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown research reports with shell command examples and optional JSON output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may be saved locally under a reports directory when the referenced runtime files are available.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence; artifact frontmatter reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
