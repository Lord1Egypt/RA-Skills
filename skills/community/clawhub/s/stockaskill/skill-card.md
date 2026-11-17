## Description:

Multi-market intelligent stock selection for A-share, Hong Kong, US stocks, and ETFs, including stock analysis, market scanning, portfolio construction, factor screening, strategy signals, fund screening, backtesting, and investment diagnosis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[axjing](https://clawhub.ai/user/axjing)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run market-data-backed equity and fund research workflows, including single-security analysis, scans, portfolio construction, strategy backtests, and investment diagnostics. The skill supports A-share, Hong Kong, US stock, and ETF/LOF research using AKShare-based data flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may fetch market data from external providers and produce financial research outputs that can be mistaken for trading advice.

Mitigation: Use outputs as research support only, verify market data and filings independently, and avoid treating BUY/SELL/HOLD signals as direct trade instructions.

Risk: The skill may install or upgrade mutable Python market-data packages and run broad local Python or Bash workflows.

Mitigation: Run it in a disposable virtual environment, review commands before execution, and prefer pinned dependency versions.

Risk: The referenced runtime scripts are not included in the submitted artifact for review.

Mitigation: Review or supply the missing scripts before allowing execution in a sensitive workspace.

Risk: The skill may create local SQLite cache and report files.

Mitigation: Run it in a non-sensitive workspace and inspect generated files before sharing or retaining them.

## Reference(s):

- [Server-resolved source repository](https://github.com/axjing/stockaskill)
- [ClawHub skill page](https://clawhub.ai/axjing/skills/stockaskill)
- [AKShare official documentation](https://akshare.akfamily.xyz)
- [AKShare GitHub repository](https://github.com/akfamily/akshare)
- [AKShare PyPI package](https://pypi.org/project/akshare)
- [Factor system](references/factors.md)
- [Strategy system](references/strategies.md)
- [Python API quick reference](references/python-api.md)
- [Risk and research boundary](references/risk-and-compliance.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown, JSON, terminal text, and shell command suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local cache and report files under the skill workspace.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
