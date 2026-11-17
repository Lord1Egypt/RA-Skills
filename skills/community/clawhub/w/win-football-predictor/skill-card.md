## Description:

Win Football Predictor helps agents generate football lottery outcome analysis using Pi-Rating, odds-derived probabilities, ensemble heuristics, upset detection, and league-specific adjustments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangjinfc](https://clawhub.ai/user/yangjinfc)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to draft football match prediction reports, compare model probabilities with market odds, and flag possible upset outcomes. Its outputs should be treated as entertainment or decision-support analysis, not as betting advice or validated forecasting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release advertises historical training and accuracy claims that are not supported by the bundled code or data.

Mitigation: Treat predictions and backtest numbers as unverified heuristic outputs until the publisher provides real historical data, model artifacts, provenance, and reproducible evaluation methodology.

Risk: Users may mistake football prediction outputs for betting advice.

Mitigation: Present outputs as entertainment or decision-support analysis, include the skill's stated caution that it is not betting advice, and require human review before any wagering-related use.

Risk: The bundled script can create output files when prediction or backtest commands are run.

Mitigation: Run the script in a controlled workspace and review generated JSON or reports before sharing or using them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yangjinfc/skills/win-football-predictor)
- [Feature engineering reference](references/features.md)
- [Backtest analysis reference](references/backtest.md)
- [500.com football lottery data](https://datachain.500.com/sfc/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with JSON prediction artifacts and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write prediction and backtest JSON files when the bundled script is executed.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
