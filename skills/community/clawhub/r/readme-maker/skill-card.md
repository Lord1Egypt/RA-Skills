## Description:

Readme Maker helps agents design, validate, generate, format, and review GitHub profile READMEs and project documentation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and documentation maintainers use this skill to draft, lint, validate, format, compare, preview, and report on README content from a command-line workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided README text and project notes can be stored in plaintext logs under ~/.local/share/readme-maker/.

Mitigation: Do not pass secrets, tokens, private project notes, unreleased details, or sensitive README drafts to the skill.

Risk: Search and export commands can expose previously logged README content.

Mitigation: Review exported files before sharing them and periodically delete local readme-maker logs when they are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bytesagain-lab/skills/readme-maker)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with optional shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command inputs, history, search results, and exports may be persisted as local plaintext files by the bundled CLI.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
