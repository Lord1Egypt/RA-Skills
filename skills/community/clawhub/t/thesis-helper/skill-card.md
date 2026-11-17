## Description:

Thesis Helper provides thesis-outline, literature-review, abstract-writing, citation-formatting, style-checking, and defense-preparation guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain3](https://clawhub.ai/user/bytesagain3)

### License/Terms of Use:

MIT-0

## Use Case:

Students, researchers, and academic writers use this skill to generate thesis structures, literature-review frameworks, abstract templates, citation-format examples, formatting checklists, and defense-preparation prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release includes an under-disclosed local data/history logging script.

Mitigation: Review the local logging behavior before installation, set THESIS_HELPER_DIR to an approved directory, or avoid data-management commands when logging is not desired.

Risk: The defense-preparation command has a shell-input weakness around duration calculations.

Mitigation: Use only trusted numeric duration values, or validate/replace the bc-based calculation before exposing the command to untrusted input.

## Reference(s):

- [Thesis Helper Tips](artifact/tips.md)
- [BytesAgain homepage](https://bytesagain.com)
- [Thesis Helper on ClawHub](https://clawhub.ai/bytesagain3/skills/thesis-helper)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown and plain text with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No API keys are required; bundled shell scripts may write local data and history logs when invoked.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
