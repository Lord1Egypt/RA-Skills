## Description:

Inserts text, paragraphs, or Excel/CSV tables at the cursor position in the currently open Microsoft Word document.

This skill is ready for commercial/non-commercial use.

## Publisher:

[183347986](https://clawhub.ai/user/183347986)

### License/Terms of Use:

MIT-0

## Use Case:

Report-writing users and office automation agents use this skill to place computed values, prose, or tabular data directly into an open Word document without manual copy and paste.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill modifies the currently active Word document in place.

Mitigation: Place the cursor in the intended document before running the skill and review the changed document when accuracy matters.

Risk: Nearby document text may appear in command output or agent logs.

Mitigation: Avoid using the skill on confidential documents unless that logging behavior is acceptable.

Risk: Dependency behavior can change if runtime packages are not reviewed or pinned.

Mitigation: Use reviewed, pinned versions of pywin32 and openpyxl in the managed Python environment.

## Reference(s):

- [Environment Gotchas](references/gotchas.md)
- [ClawHub skill page](https://clawhub.ai/183347986/skills/word-cursor-insert)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and short execution-result text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Windows, Microsoft Word, pywin32, and openpyxl for Excel files.]

## Skill Version(s):

1.0.2 (source: manifest.yaml and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
