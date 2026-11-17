## Description:

Professional US stock analysis with financial data, news, social sentiment, and multi-model AI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aisadocs](https://clawhub.ai/user/aisadocs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and external users use this skill to gather US equity data, monitor portfolios, screen stocks, and generate informational stock analysis reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stock tickers, watchlists, research queries, and analysis context may be sent to AIsa and model providers.

Mitigation: Use the skill only with information you are comfortable sharing with those services, and avoid submitting sensitive or non-public portfolio context.

Risk: Generated reports may contain incorrect, incomplete, or time-sensitive financial analysis.

Mitigation: Review reports before relying on them and consult licensed financial professionals before making investment decisions.

Risk: Saved reports are written as local JSON files when an output path is provided.

Mitigation: Choose output filenames and directories carefully to avoid overwriting files or exposing reports in shared locations.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/aisadocs/skills/us-stock-analyst)
- [AIsa API reference](https://aisa.mintlify.app/api-reference/introduction)
- [AIsa complete documentation](https://aisa.mintlify.app/llms.txt)
- [AIsa website](https://aisa.one)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell and Python examples, plus JSON analysis reports when saved to a file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AISA_API_KEY and may write local JSON report files when an output path is provided]

## Skill Version(s):

1.0.1 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
