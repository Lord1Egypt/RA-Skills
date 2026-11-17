## Description:

Automatically fills Word table-based application forms by mapping report content into corresponding form sections while preserving the original document structure and applying uniform formatting to inserted text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fanqing203](https://clawhub.ai/user/fanqing203)

### License/Terms of Use:

MIT-0

## Use Case:

External users and document automation practitioners use this skill to fill structured Word application forms, especially medical, research, and project declaration forms, from prepared report content. It is intended for local Windows workflows that can run Python and Word automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Opening user-supplied Word documents through local Office automation can expose users to unsafe or unexpected document behavior.

Mitigation: Process only trusted documents, avoid unknown .doc and macro-enabled files, and review the generated output before using it.

Risk: Automated form filling may overwrite or distort important application content if the form structure or row mapping is wrong.

Mitigation: Keep backups of original documents, write to a distinct output path, and manually inspect filled forms for content and formatting accuracy.

Risk: The runtime dependency on pywin32 and local Word automation can vary across Windows and Office environments.

Mitigation: Pin and test pywin32 in the target environment before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fanqing203/skills/sanxin)
- [fanqing203 publisher profile](https://clawhub.ai/user/fanqing203)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with Python code and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or update local Word document files when the Python automation script is executed by the user.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
