## Description:

Zettelkasten CN helps agents create, organize, search, link, update, delete, convert, and recover Markdown notes for a Chinese-language Zettelkasten workflow across fleeting, literature, permanent, project, and map note types.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wittfan](https://clawhub.ai/user/wittfan)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to maintain a local Markdown-based Zettelkasten knowledge base, including note creation, classification into nine life domains, linking, memory-date references, search, conversion, and undo support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The authoritative security summary reports that forged or misused undo history can move or overwrite files outside the intended notes folder.

Mitigation: Review before installing, use only in a constrained workspace, validate undo paths against the configured notes and trash directories, and avoid trusting serialized paths from operation_history.json.

Risk: The undo manager exposes an internal log command that can write arbitrary operation details into the undo history.

Mitigation: Restrict or remove the internal log command before broader use, or limit write access to the history file and run the skill with least-privilege filesystem permissions.

## Reference(s):

- [Advanced Zettelkasten Features](references/advanced.md)
- [Zettelkasten Command Configuration](references/config.json)
- [ClawHub Skill Page](https://clawhub.ai/wittfan/skills/zettelkasten-cn)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown note files, JSON command results, and terminal guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and modifies local files under the configured cards directory; default paths can be overridden with environment variables.]

## Skill Version(s):

1.0.0 (source: server release metadata and references/config.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
