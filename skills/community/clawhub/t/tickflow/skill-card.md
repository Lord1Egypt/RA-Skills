## Description:

Uses the TickFlow Python SDK to retrieve real-time quotes and K-line data for A-share, Hong Kong, U.S. equity, and futures markets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tickflow-dev](https://clawhub.ai/user/tickflow-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, data analysts, and quantitative researchers use this skill to set up TickFlow SDK workflows and generate examples for retrieving market quotes, historical and intraday K-line data, instrument metadata, and financial data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup guidance includes install steps that should be reviewed before execution.

Mitigation: Install uv through a trusted package manager or verified release before running TickFlow examples.

Risk: API key setup guidance may encourage storing TICKFLOW_API_KEY in shell startup files.

Mitigation: Store TICKFLOW_API_KEY in a password manager, OS keychain, or local uncommitted environment file.

Risk: Dependency installation can change over time if package versions are not pinned.

Mitigation: Pin and lock Python dependencies for repeatable agent environments.

## Reference(s):

- [TickFlow homepage](https://tickflow.org)
- [ClawHub TickFlow skill page](https://clawhub.ai/tickflow-dev/skills/tickflow)
- [uv installer for macOS/Linux](https://astral.sh/uv/install.sh)
- [uv installer for Windows PowerShell](https://astral.sh/uv/install.ps1)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require python3, uv, and TICKFLOW_API_KEY for full real-time data workflows.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
