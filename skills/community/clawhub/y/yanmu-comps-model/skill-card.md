## Description:

A comparable-company valuation skill for equity research that compares valuation, profitability, growth, and financial-health metrics, then produces valuation commentary and charts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caoling7878-arch](https://clawhub.ai/user/caoling7878-arch)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to run comparable-company valuation analysis for supported A-share, Hong Kong, and U.S. equities. It helps compare PE, PB, PS, EV/EBITDA, ROE, margins, and growth metrics and generate text or JSON outputs plus chart files for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial comparison outputs could be mistaken for investment advice.

Mitigation: Treat the generated analysis as reference material only and review it with appropriate financial judgment before use.

Risk: The script contacts Sina Finance for live quote data whenever it runs.

Mitigation: Run it in an environment where outbound network access is expected and acceptable.

Risk: Python dependencies are installed from the environment package source.

Mitigation: Install in a dedicated virtual environment and review or pin dependency versions before installing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/caoling7878-arch/skills/yanmu-comps-model)
- [Sina Finance](https://finance.sina.com.cn)

## Skill Output:

**Output Type(s):** [text, json, files, shell commands, guidance]

**Output Format:** [Plain text report or JSON, with local PNG chart files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a target ticker, comma-separated comparable tickers, market, output directory, and output format.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
