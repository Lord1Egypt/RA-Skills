## Description:

你的私人 AI 投顾。提供 A 股个股深度多维分析、持仓管理。

This skill is ready for commercial/non-commercial use.

## Publisher:

[daasai](https://clawhub.ai/user/daasai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to request A-share stock analysis reports and manage a local stock portfolio through command-line actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installer guidance includes a curl-to-shell command for uv.

Mitigation: Use a trusted uv installation path and independently verify installer sources before running them.

Risk: Stock symbols and the configured API key are sent to the selected Stock Advisor Pro API backend.

Mitigation: Configure only a trusted HTTPS or loopback API endpoint and treat API responses as external service output.

Risk: Portfolio holdings are stored as plaintext local financial data.

Mitigation: Protect local access to the skill directory and avoid storing sensitive portfolio records on shared systems.

Risk: The artifact bundles a sample portfolio record.

Mitigation: Clear data/portfolio.json before real use.

Risk: Runtime dependencies are installed dynamically by uv script metadata.

Mitigation: Pin and review dependencies before deployment.

## Reference(s):

- [Stock Advisor Pro ClawHub skill page](https://clawhub.ai/daasai/skills/stock-advisor)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports and command-line text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stock scan output depends on a configured Stock Advisor Pro API endpoint; portfolio data is stored as local JSON.]

## Skill Version(s):

1.0.0 (source: server release metadata, artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
