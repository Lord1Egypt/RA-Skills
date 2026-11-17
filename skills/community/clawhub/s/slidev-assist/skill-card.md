## Description:

Generates Slidev presentation Markdown and supporting commands from topics, documents, data, web pages, copy, or existing PPTX material.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sfewsuper](https://clawhub.ai/user/sfewsuper)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, developers, and presentation authors use this skill to turn source material into Slidev-based presentations, then preview or export the result. It is most useful when an agent is allowed to read local inputs, produce slides.md, and suggest npm/npx commands for Slidev workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic npm/npx execution can fetch changing package versions.

Mitigation: Pin Slidev and Playwright versions in a project lockfile before running generated install, preview, or export commands.

Risk: The skill can process local documents, spreadsheets, PPTX files, and web content.

Mitigation: Use it only in workspaces where those files are appropriate for the agent to read, and avoid sensitive documents unless that access is intended.

Risk: Remote Slidev preview can expose the local presentation server beyond the local machine.

Mitigation: Avoid enabling --remote unless the user understands and accepts the network exposure.

Risk: Global package installation changes the host environment.

Mitigation: Prefer local project installation over global installs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sfewsuper/skills/slidev-assist)
- [Slidev Documentation](https://sli.dev)
- [Slidev GitHub Repository](https://github.com/slidevjs/slidev)
- [Slidev Assist Quick Reference](references/quickref.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, Slidev frontmatter, inline code blocks, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces presentation source and workflow guidance for previewing or exporting with Slidev; does not itself guarantee package pinning or network isolation.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
