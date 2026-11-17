## Description:

Create, manage, and operate a Zettelkasten slip-box note system using the zk.py CLI script.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goog](https://clawhub.ai/user/goog)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create and maintain a local Markdown Zettelkasten vault, including fleeting, literature, permanent, and Map of Content notes. It supports note creation, linking, orphan detection, search, graph inspection, promotion, and vault statistics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled CLI can run unintended shell commands through editor settings.

Mitigation: Review before installation, use --no-edit until editor launch is fixed, and only use a trusted EDITOR value.

Risk: The CLI creates and scans a local Markdown vault.

Mitigation: Use a trusted ZK_VAULT path and review any proposed shell profile changes before applying them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/goog/skills/znote)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command snippets and generated Python or Markdown files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local vault files and may open an editor unless note commands are run with --no-edit.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
