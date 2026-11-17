## Description:

SSQ Predictor analyzes local historical Double Color Ball lottery CSV data and generates zone-balanced number recommendations using hot/cold number, omission-value, and distribution heuristics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ligo-gao](https://clawhub.ai/user/ligo-gao)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to analyze SSQ lottery history from a local CSV and generate multiple entertainment-oriented number recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake lottery-number recommendations for reliable financial advice or improved odds.

Mitigation: Present predictions as entertainment only and avoid using the output as the basis for financial decisions.

Risk: Predictions depend on the local historical-results CSV supplied by the user.

Mitigation: Review the CSV source and format before running the scripts, and treat malformed or stale data as reducing output usefulness.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ligo-gao/skills/ssq-predictor)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands, Python snippets, and printed prediction results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads a local historical-results CSV and prints generated red-ball and blue-ball predictions with zone and size distributions.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
