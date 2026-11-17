## Description:

Retail Investor Radar generates a plain-language A-share stock health report from a ticker, Chinese stock name, or pinyin abbreviation, using public market data and DeepSeek-assisted analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tkk0124](https://clawhub.ai/user/tkk0124)

### License/Terms of Use:

MIT-0

## Use Case:

External users and retail-investor analysts use this skill to enter an A-share ticker, Chinese name, or pinyin abbreviation and receive a plain-language report covering quote data, technical indicators, valuation, financial health, fund flow, recent news, and risk notes. The report is informational and should not be treated as investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the selected stock and fetched market or news context to DeepSeek.

Mitigation: Use it only when comfortable sharing that context with DeepSeek, and avoid entering confidential portfolio or trading information.

Risk: Generated reports may contain incorrect, stale, or misleading financial interpretation.

Mitigation: Treat outputs as informational, verify important claims against primary sources, and do not treat the report as investment advice.

Risk: Market-data dependencies and network access can fail or return partial data.

Mitigation: Check logs for fallback or missing-field warnings, and run in an isolated Python environment with pinned dependencies and proxy configuration when needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tkk0124/skills/retail-investor-radar)
- [DeepSeek Chat Completions API Endpoint](https://api.deepseek.com/v1/chat/completions)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown-like console text and saved text reports with setup commands and YAML configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DEEPSEEK_API_KEY; default report generation uses max_tokens 2000 and can save reports under ./reports.]

## Skill Version(s):

1.1.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
