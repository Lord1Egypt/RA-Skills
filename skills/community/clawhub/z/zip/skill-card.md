## Description:

Compress, extract, list, and encrypt ZIP archives in batch.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and operators use this skill to generate shell commands for creating, extracting, listing, updating, testing, searching, comparing, and password-protecting ZIP archives.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Archive names, file names, or patterns supplied from untrusted sources can be interpreted as unsafe zip or unzip options.

Mitigation: Use the skill only in controlled directories with trusted archive and file names, and review generated commands before execution.

Risk: Password-protected archive commands can expose passwords through process listings, logs, or transcripts.

Mitigation: Avoid using the password command for real secrets; prefer safer secret-handling workflows outside this wrapper.

Risk: Extracting archives can overwrite files or place unexpected content in the target directory.

Mitigation: Extract only trusted archives into a dedicated directory and inspect contents before using them.

## Reference(s):

- [Zip skill page](https://clawhub.ai/xueyetianya/skills/zip)
- [BytesAgain homepage](https://bytesagain.com)
- [Publisher profile](https://clawhub.ai/user/xueyetianya)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash command examples and concise operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe archive paths, file arguments, output directories, patterns, and password-protected archive workflows.]

## Skill Version(s):

3.0.1 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
