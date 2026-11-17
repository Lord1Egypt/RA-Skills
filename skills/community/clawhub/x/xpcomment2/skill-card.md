## Description:

Manages JPEG XPComment metadata by generating exiftool commands to read, add, overwrite, or remove Windows photo comments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[happyturbo](https://clawhub.ai/user/happyturbo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to manage XPComment metadata on local JPEG/image files with exiftool, including single-file, wildcard, and recursive folder operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe shell execution from untrusted file paths or comment text.

Mitigation: Use only trusted local images and avoid copying untrusted paths or comment text directly into shell commands.

Risk: Metadata add, remove, wildcard, or recursive operations can overwrite or delete XPComment values across one or many files.

Mitigation: Make backups and require explicit confirmation before overwrite, delete, wildcard, or recursive runs.

Risk: The suggested sudo install command changes the system package set.

Mitigation: Run the sudo install command only when intentionally installing the exiftool system package.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/happyturbo/skills/xpcomment2)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include exiftool commands and completion summaries for read, add, overwrite, remove, wildcard, and recursive XPComment operations.]

## Skill Version(s):

1.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
