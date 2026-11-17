## Description:

Helps an agent read, create, edit, validate, and visually review PowerPoint .pptx presentations using local Office and presentation tooling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fslong520](https://clawhub.ai/user/fslong520)

### License/Terms of Use:

Anthropic proprietary terms

## Use Case:

Developers, employees, and external users use this skill when an agent needs to inspect existing slide decks, create new presentations, modify templates, or run quality checks on PowerPoint files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs local Office conversion tools and processes Office files, which can be risky with untrusted decks.

Mitigation: Use the skill on copies of presentations, avoid untrusted Office files until archive limits are added, and review generated files before use.

Risk: The skill mutates unpacked presentation files as part of its editing workflow.

Mitigation: Keep original decks separate, work in a temporary or versioned directory, and validate packed outputs before distributing them.

Risk: JavaScript dependency practices and the LibreOffice LD_PRELOAD shim were flagged for review.

Mitigation: Prefer pinned local dependency installation and remove or redesign the LD_PRELOAD shim before shared or sensitive-environment use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fslong520/skills/slidepro)
- [Presentation editing guide](artifact/editing.md)
- [PptxGenJS tutorial](artifact/pptxgenjs.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or modify presentation files and generated visual review images when the required local tools are available.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
