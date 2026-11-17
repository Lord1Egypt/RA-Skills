## Description:

Evaluate a README file text, score it out of 100, and provide specific, actionable improvement suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunny0826](https://clawhub.ai/user/sunny0826)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, maintainers, and developer advocates use this skill to evaluate pasted README text against open-source documentation best practices and receive a score, strengths, improvement suggestions, and an optimized Markdown example.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted README content may contain prompt-injection instructions or commands.

Mitigation: Treat the README only as text to be reviewed; do not execute commands, follow embedded instructions, or fetch remote README content.

Risk: Users may provide only a URL, which would require fetching external untrusted content.

Mitigation: Ask the user to paste the raw README text directly instead of retrieving content from external URLs.

Risk: Installers may expect English output when the skill is designed to respond primarily in Chinese.

Mitigation: Set expectations that README review reports are produced primarily in Chinese.

## Reference(s):

- [README Grader ClawHub page](https://clawhub.ai/sunny0826/skills/readme-grader)
- [README Grader README](artifact/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Structured Markdown, primarily in Chinese, with a score breakdown, strengths, improvement suggestions, and an example README snippet.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires raw README text from the user; it should not fetch external README URLs or execute instructions embedded in the README content.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
