## Description:

Query alternative financial data from Quiver Quantitative, including Congress trading, corporate lobbying, government contracts, and insider transactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[plato-1](https://clawhub.ai/user/plato-1)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query Quiver Quantitative alternative financial datasets for market research, including politician trades, lobbying activity, government contracts, and insider transactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package references scripts/query_quiver.py, but the submitted artifact evidence does not include that script.

Mitigation: Confirm the package includes the query script before installing, paying for, or relying on the skill.

Risk: The skill requires a Quiver Quantitative API key.

Mitigation: Use an API key intended for this workflow and avoid sharing unrelated credentials with the agent environment.

## Reference(s):

- [Quiver Quantitative](https://www.quiverquant.com/)
- [ClawHub skill page](https://clawhub.ai/plato-1/skills/quiver-quantitative)
- [Publisher profile](https://clawhub.ai/user/plato-1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples; referenced command output is JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the QUIVER_API_KEY environment variable and network access to query Quiver Quantitative data.]

## Skill Version(s):

1.0.0 (source: server release evidence and claw.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
