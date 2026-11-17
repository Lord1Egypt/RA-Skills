## Description:

Interprets pasted statistical results, including SPSS output, and generates academic-style Chinese writeups for tests such as t-tests, ANOVA, chi-square, correlation, regression, mediation/moderation, and reliability analyses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeoyee](https://clawhub.ai/user/jeoyee)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, students, and analysts use this skill to turn statistical test output into Chinese academic prose suitable for a paper results section. It is oriented toward common psychology, statistics, and data analysis workflows, including pasted SPSS-style output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pasted research results are transmitted to Moonshot/Kimi for processing, which can expose confidential, regulated, unpublished, or participant-level data.

Mitigation: Use only data approved for external processing, disclose the remote transmission before use, and redact or aggregate sensitive inputs.

Risk: The artifact contains a bundled API key.

Mitigation: Remove and rotate the bundled key, then require users to provide credentials through a managed secret or environment variable.

Risk: Generated statistical interpretations may be incomplete or inaccurate for publication use.

Mitigation: Have a qualified reviewer compare the generated prose against the original statistical output before using it in academic writing.

Risk: Generated interpretations are autosaved locally as timestamped text files.

Mitigation: Disclose local storage behavior and remove or protect saved files when outputs include sensitive study details.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jeoyee/skills/statistics-skill)
- [Publisher profile](https://clawhub.ai/user/jeoyee)
- [Moonshot API endpoint](https://api.moonshot.cn/v1)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files, Guidance]

**Output Format:** [Chinese prose text with R source-command usage guidance and locally saved .txt interpretation files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Calls Moonshot/Kimi for interpretation and autosaves generated results to timestamped text files.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
