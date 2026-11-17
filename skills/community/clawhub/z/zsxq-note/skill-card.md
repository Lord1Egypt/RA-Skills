## Description:

Manages public ZSXQ notes through zsxq-cli, including creating, listing, viewing, editing, and deleting notes that are accessible to anyone with the link.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zsxq](https://clawhub.ai/user/zsxq)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to manage public ZSXQ notes from a logged-in zsxq-cli account, including creating shareable notes, reviewing note history, inspecting details, updating content, and deleting notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Created or edited notes are public and can be accessed by anyone with the link.

Mitigation: Review note text and attachments before create or edit, and avoid adding private or sensitive information.

Risk: Deleting a note is described as irreversible.

Mitigation: Confirm the target note_id and current note content before running a delete operation.

Risk: The skill operates through the user's logged-in zsxq-cli account.

Mitigation: Install and use it only when the agent is intended to manage public ZSXQ notes for that account.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zsxq/skills/zsxq-note)
- [note +create](references/zsxq-note-create.md)
- [note +list](references/zsxq-note-list.md)
- [note +detail](references/zsxq-note-detail.md)
- [note +edit](references/zsxq-note-edit.md)
- [note +delete](references/zsxq-note-delete.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires zsxq-cli and a logged-in account; note operations can create public content or delete content irreversibly.]

## Skill Version(s):

1.3.1 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
