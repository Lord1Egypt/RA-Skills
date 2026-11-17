## Description:

Convert any URL to clean, readable Markdown for article saving, web content extraction, reading-list conversion, and optional article summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linbeiganlinniang](https://clawhub.ai/user/linbeiganlinniang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and agents use this skill to turn web articles and reading lists into clean Markdown for offline reading, LLM context, archiving, and knowledge-base workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill fetches user-provided web URLs and may write Markdown files locally.

Mitigation: Confirm the URLs to fetch and the destination paths before running batch or output commands.

Risk: The installation command uses an unpinned web2md package dependency.

Mitigation: Install only from a trusted package source, preferably in a virtual environment, and consider pinning a reviewed version.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linbeiganlinniang/skills/web2md-pro)
- [Web2md website](https://web2md.dev)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with bash command examples and generated Markdown files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May fetch user-provided URLs and write Markdown output files; optional summaries depend on the installed web2md package and available AI support.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
