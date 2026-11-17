## Description:

Helps users request technical indicator analysis, calculations, and visualization guidance based on a toolkit converted from popular TradingView Pine Script indicators.

This skill is ready for commercial/non-commercial use.

## Publisher:

[super-max21](https://clawhub.ai/user/super-max21)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this OpenClaw skill to ask for TradingView-derived technical analysis over market data and receive calculated indicator analysis or visualization-oriented guidance. Because execution is delegated to a remote Prana service, users should avoid sending proprietary trading strategies, sensitive account data, or secrets unless that service is trusted.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and user-provided trading context are sent to a remote Prana service.

Mitigation: Use the skill only with a trusted remote service and do not submit proprietary strategies, sensitive account data, or other confidential information.

Risk: The client handles API credentials and may fetch or write them to local configuration files.

Mitigation: Prefer pre-provisioned narrowly scoped credentials, protect environment and config files, set PRANA_SKILL_NO_AUTO_API_KEY to prevent automatic key fetching when appropriate, and set PRANA_SKILL_SKIP_WRITE_API_KEY to avoid plaintext credential writes.

Risk: Server security evidence marks this package suspicious because its visible technical-analysis helper behavior is implemented through a remote execution client.

Mitigation: Review the package before installation, scan it before deployment, and run it only in environments where remote prompt handling and credential use are acceptable.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON responses from the remote client and Markdown or plain-text guidance when returned by the remote skill]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include technical-analysis results, code snippets, setup commands, thread identifiers, or remote execution status depending on the Prana response.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
