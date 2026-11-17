## Description:

A Chinese-language research methods advisor that recommends statistical tests, alternatives, assumptions, sample-size planning guidance, psychometric analysis methods, and Python function examples from a user's study design inputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhan599](https://clawhub.ai/user/zhan599)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, students, and analysts use this skill to choose appropriate quantitative research methods before or during study planning and data analysis. It is most useful for psychology and social-science workflows that need test-selection guidance, assumption checks, nonparametric alternatives, and Python implementation pointers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can suggest an unsuitable statistical method if the study design, variable type, sampling structure, or assumptions are entered incorrectly.

Mitigation: Treat recommendations as planning guidance and have the final method choice reviewed against the actual study design and diagnostic checks.

Risk: Sample-size and power outputs are approximate planning estimates rather than formal study-power calculations.

Mitigation: Use dedicated tools such as G*Power, statsmodels, or pingouin for final sample-size and power analysis before committing to a study plan.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhan599/skills/research-method-advisor)
- [Publisher profile](https://clawhub.ai/user/zhan599)
- [SKILL.md](artifact/SKILL.md)
- [README.md](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Chinese-language recommendations with Python examples, structured dictionaries, and optional command-line prompts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No external dependencies are declared; output depends on user-supplied research purpose, variable types, group counts, design, and assumption status.]

## Skill Version(s):

1.0.0 (source: server release evidence and target metadata; artifact manifest lists 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
