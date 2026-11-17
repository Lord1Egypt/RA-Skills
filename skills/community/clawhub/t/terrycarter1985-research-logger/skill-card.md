## Description:

Research a topic via web search, auto-match a GIF with gifgrep, and log structured notes to Bear using a customizable template.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, developers, and productivity-focused users use this skill to gather web search results for a topic, attach a related GIF, and create a structured Bear note from a customizable template.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Template, fetched web content, and local path handling may expose users to unsafe note content or unintended file access.

Mitigation: Escape template replacements, validate fetched URLs, and constrain template paths before routine use.

Risk: Fallback note storage and Bear note creation behavior may not reliably preserve user intent when note creation fails.

Mitigation: Use private temporary storage and fix the Bear fallback control flow before relying on the fallback output.

Risk: The grizzly dependency is installed from a moving latest version.

Mitigation: Pin the grizzly module version and review dependency changes before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/terrycarter1985-research-logger)
- [grizzly install module](https://github.com/tylerwince/grizzly)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown note content with source links and GIF media references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a Bear note through grizzly or write fallback Markdown content to local temporary storage.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
