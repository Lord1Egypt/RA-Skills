## Description:

Research a topic via web search, auto-match a GIF, and log structured notes to Bear.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to gather web research, match a related GIF, and produce a Bear-ready Markdown research note from a reusable template.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted topic text can execute local code in fallback mode.

Mitigation: Review and fix topic input handling before using the skill with untrusted or sensitive research topics.

Risk: The note is written to a predictable temporary path.

Mitigation: Change the output path to a unique private temporary file before relying on the generated note for Bear workflows.

## Reference(s):

- [Research note template](references/research_template.md)
- [Research Logger on ClawHub](https://clawhub.ai/terrycarter1985/skills/research-logger-tc)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown note content with a shell command workflow]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a Bear-ready research note to a local Markdown file and prints it to stdout.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
