## Description:

Extract readable text, markdown, HTML, JSON, or XML content from web pages using the trafilatura CLI tool with optional metadata and output formatting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goog](https://clawhub.ai/user/goog)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and content workflows use this skill to extract readable page content from a URL and return it as markdown, plain text, HTML, JSON, or XML.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill fetches user-provided URLs over the network, which can expose private, internal, or sensitive URLs if supplied.

Mitigation: Use a controlled environment and avoid providing internal, private, or sensitive URLs unless network retrieval is intended.

Risk: The skill depends on the locally installed trafilatura package, so behavior can vary by package version.

Mitigation: Install in a virtual environment where possible, and pin and review the trafilatura package version before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/goog/skills/tra-extract-text)

## Skill Output:

**Output Type(s):** [Text, Markdown, HTML, JSON, XML, Shell commands, Guidance]

**Output Format:** [Markdown guidance with trafilatura CLI commands and extracted content in markdown, plain text, HTML, JSON, or XML.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write extracted content to a file and include page metadata when requested.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
