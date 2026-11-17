## Description:

Package directory structures into a single plain text file, or restore directory structures from text files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[turinfohlen](https://clawhub.ai/user/turinfohlen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agent users use this skill to serialize project directories into portable plain text archives and restore those archives in another environment or conversation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A crafted archive can write files or create symlinks outside the chosen output folder during unpacking.

Mitigation: Use only trusted archives, unpack into a disposable empty directory, and avoid elevated privileges until path traversal and symlink containment checks are added.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/turinfohlen/skills/text-directory-archiver)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with protocol examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or consume plain text archive files containing JSON metadata, text blocks, Base64 blocks, directory entries, and symlink declarations.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
