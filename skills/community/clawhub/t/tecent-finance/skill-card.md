## Description:

Get stock prices, quotes, and compare stocks using Tencent Finance API. No API key required. Supports US stocks, China A-Shares, Hong Kong stocks. Optimized for use in mainland China.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pz325](https://clawhub.ai/user/pz325)

### License/Terms of Use:

MIT

## Use Case:

Developers and analysts use this skill to retrieve stock prices, detailed quotes, comparisons, and symbol searches through Tencent Finance for US, China A-share, Hong Kong, and major crypto symbols.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package contains documentation only, so the described CLI implementation may be absent or incomplete.

Mitigation: Verify the tfin implementation exists and works before relying on the skill for financial information.

Risk: Manual setup can involve installing Python packages or creating command symlinks.

Mitigation: Install dependencies in a virtual environment and avoid running pip or symlink commands with elevated privileges.

Risk: Financial quote data can be incomplete, delayed, or unavailable for unsupported symbols or markets.

Mitigation: Validate symbols and confirm material financial decisions against authoritative market data sources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pz325/skills/tecent-finance)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and tabular financial data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require local Python dependencies and network access to Tencent Finance API.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
