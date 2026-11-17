## Description:

Write a coding standards document for a project using the coding styles from the file(s) and/or folder(s) passed as arguments in the prompt, without modifying analyzed source files unless edits are explicitly requested and confirmed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jhauga](https://clawhub.ai/user/jhauga)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to analyze explicitly provided project files or narrowly scoped folders and produce a coding standards document, README section, or prompt output that reflects the project's existing style.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad folder analysis could unintentionally include secrets, generated outputs, dependency folders, or unrelated private files.

Mitigation: Analyze only explicit file paths or narrowly scoped folders and keep the default exclusions for secret, private, dependency, build, and environment files.

Risk: Generated coding standards or inconsistency summaries may be incomplete or misleading if the provided files are not representative.

Mitigation: Review the generated standards against the project before adopting them, and provide additional representative files when needed.

Risk: README, test-file, or source-file edits can change project behavior or documentation unexpectedly.

Mitigation: Use read-only prompt output when appropriate, and require explicit approval plus diff review before accepting any file edits.

Risk: Optional public style-guide fetching may make network requests during standards generation.

Mitigation: Set fetchStyleURL=false in restricted environments or when external reference fetching is not needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jhauga/skills/write-coding-standards-from-file)
- [Publisher profile](https://clawhub.ai/user/jhauga)
- [Skill source evidence](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown or plain text, with optional project file updates when explicitly requested and confirmed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a coding standards file, add README content, summarize inconsistencies, or propose reviewed diffs depending on configuration.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
