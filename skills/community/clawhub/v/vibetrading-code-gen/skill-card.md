## Description:

Generate executable Hyperliquid trading strategy code from natural language prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuhaonan00](https://clawhub.ai/user/liuhaonan00)

### License/Terms of Use:


## Use Case:

Developers and trading automation users use this skill to turn natural-language strategy ideas into Python strategy files, configuration, usage guidance, and validation or backtesting commands for Hyperliquid workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated trading strategies can be run against live exchange credentials and may cause financial loss.

Mitigation: Manually audit generated code and API behavior, start with testnet or paper trading, and use restricted no-withdrawal API keys with small limits.

Risk: Generated or downloaded strategy files and validator or backtester inputs are executable Python.

Mitigation: Treat strategy files as untrusted code and run validation or backtesting only in a sandboxed environment.

Risk: The documented cleanup command permanently deletes local logs, sessions, and simulation results.

Mitigation: Review cleanup targets before running destructive shell commands and preserve any files needed for audit or troubleshooting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liuhaonan00/skills/vibetrading-code-gen)
- [Hyperliquid API endpoint](https://api.hyperliquid.xyz)
- [Hyperliquid testnet API endpoint](https://api.hyperliquid-testnet.xyz)

## Skill Output:

**Output Type(s):** [Code, Configuration, Markdown, Shell commands, Guidance]

**Output Format:** [Python files, JSON configuration, Markdown usage instructions, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated strategies may include validation reports, backtesting output, requirements, and risk warnings.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
