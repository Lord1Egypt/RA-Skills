## Description:

Sync WeRead shelf state, reading progress, visible book content, and note-ready Markdown into a local workspace using the user's logged-in Chrome session.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mingchaoxu](https://clawhub.ai/user/mingchaoxu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and personal knowledge workers use this skill to sync WeRead shelf and book page data into local JSON and Obsidian-ready Markdown for note taking, review, and downstream agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access a logged-in Chrome debugging session and read visible WeRead page content.

Mitigation: Use it only on a machine you control, keep Chrome remote debugging disabled except during sync, and pass only intended WeRead URLs.

Risk: The skill can write or overwrite Obsidian notes through obsidian-cli.

Mitigation: Review generated Markdown before publishing and use a test vault or backup until overwrite behavior is acceptable for the workflow.

Risk: Captured reading data and reflections may contain private personal content.

Mitigation: Treat generated files as private, review output before sharing, and sync one book at a time unless broader capture is intentional.

## Reference(s):

- [Data Contract](references/data-contract.md)
- [Security Policy](SECURITY.md)
- [ClawHub Skill Page](https://clawhub.ai/mingchaoxu/skills/weread-assitant)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands, plus generated local JSON and Markdown files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated artifacts may include WeRead shelf snapshots, per-book JSON captures, reflection sidecar JSON, Obsidian-ready Markdown notes, and Obsidian vault notes written through obsidian-cli.]

## Skill Version(s):

1.0.1 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
