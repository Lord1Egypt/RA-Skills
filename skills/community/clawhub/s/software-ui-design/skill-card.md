## Description:

Software UI Design helps agents parse UI design files, generate annotations and asset exports, check design specifications, compare designs, and produce design-system documentation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaochunz030-spec](https://clawhub.ai/user/xiaochunz030-spec)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, design engineers, and product teams use this skill to inspect Figma, Sketch, or Adobe XD designs, extract UI properties, create handoff artifacts, validate design-system rules, and draft implementation snippets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Figma parser accepts a Personal Access Token as a command-line argument, which can expose the token through shell history or process logs.

Mitigation: Use a least-privilege Figma token and prefer environment-based or interactive secret entry if adapting the script.

Risk: Reports and asset outputs may be written to user-selected paths.

Mitigation: Confirm output paths before running scripts that write reports or exported assets.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/xiaochunz030-spec/skills/software-ui-design)
- [Figma API endpoint](https://api.figma.com/v1)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown, JSON reports, generated code snippets, shell commands, and asset export guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate local reports or asset files when scripts are run with user-provided design inputs.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
