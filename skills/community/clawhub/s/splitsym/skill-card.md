## Description:

Extract comments and split symbols from source files so users can inspect inline comments, docstrings, and block comments for code understanding or documentation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[turinfohlen](https://clawhub.ai/user/turinfohlen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to extract comments, docstrings, and block comments from source files when reviewing code, understanding legacy modules, or preparing documentation summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local source files and prints extracted comment content, which may expose sensitive comments if used on private files.

Mitigation: Run it only on files intended for inspection and review extracted output before sharing it.

Risk: Custom symbols.json configurations define regex patterns that control what file content is extracted and printed.

Mitigation: Use trusted configuration files and review custom regex rules before running them on source files.

## Reference(s):

- [splitsym ClawHub release page](https://clawhub.ai/turinfohlen/skills/splitsym)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and text extraction output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Extracted comment output preserves source line numbers and indentation; block comments are marked with a PAIR: prefix.]

## Skill Version(s):

1.0.0 (source: release evidence and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
