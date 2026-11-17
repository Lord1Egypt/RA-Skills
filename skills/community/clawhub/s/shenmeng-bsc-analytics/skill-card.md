## Description:

Provides BSC/BNB Chain ecosystem analysis for DeFi protocols, on-chain monitoring, project evaluation, yield opportunities, and risk alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shenmeng](https://clawhub.ai/user/shenmeng)

### License/Terms of Use:

MIT-0

## Use Case:

External analysts, developers, and crypto researchers use this skill to summarize BSC ecosystem metrics, compare protocols, evaluate projects with the BISCUIT rubric, and estimate yield scenarios. Treat investment-oriented outputs as decision support, not financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package includes a hardcoded SkillPay API key.

Mitigation: Rotate the key before release, remove secrets from the package, and load payment credentials from a runtime secret store or environment variable.

Risk: Payment verification can send a wallet address to an external SkillPay service without clear user-facing disclosure.

Mitigation: Disclose the data transfer before use and avoid providing a wallet address unless the user accepts that transfer.

Risk: Analytics outputs are static examples or heuristics unless live data sources and provenance are added.

Mitigation: Label outputs as estimates, verify figures against live trusted sources, and avoid treating generated yield or investment analysis as financial advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shenmeng/skills/shenmeng-bsc-analytics)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text reports with optional JSON files and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce static heuristic analytics and temporary JSON report files when scripts are run.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
