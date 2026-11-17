## Description:

Analyzes A-share sector heatmaps to identify leading, rising, and potential reversal sectors using DaxiAPI sector data and CS indicator guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ksky521](https://clawhub.ai/user/ksky521)

### License/Terms of Use:

MIT-0

## Use Case:

External users and market analysts use this skill to generate structured A-share sector heatmap reports, including market posture, sector strength, heat diffusion, concept-sector hotspots, and non-personalized risk notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The token configuration check can expose a stored DaxiAPI token in shared terminals or logs.

Mitigation: Use a status-only authentication check when available, or run the intended data command and handle authentication errors without printing the token value.

Risk: Generated sector views may be mistaken for personalized investment advice.

Mitigation: Present the output as market commentary, keep the disclaimer, and require users to make their own suitability and risk decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ksky521/skills/xiapi-heatmap-analysis)
- [DaxiAPI](https://daxiapi.com)
- [CLI command reference](artifact/references/cli-commands.md)
- [CS indicator guide](artifact/references/cs-indicator.md)
- [Heatmap field descriptions](artifact/references/field-descriptions.md)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance, analysis]

**Output Format:** [Markdown report with inline shell commands and structured analysis sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses DaxiAPI heatmap, concept-sector, and top-stock data; output should remain market commentary and not personalized investment advice.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
