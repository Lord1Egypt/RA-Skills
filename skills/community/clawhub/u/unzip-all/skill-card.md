## Description:

Recursively extracts nested ZIP, 7z, and RAR archives from a file or folder, with handling for Chinese filenames.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tang-dafa](https://clawhub.ai/user/tang-dafa)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users use this skill to ask an agent to recursively unpack a single archive or all archives in a folder, including nested ZIP, 7z, and RAR files. It is especially useful when archives contain Chinese filenames that need GBK decoding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill performs broad recursive archive extraction and file writes.

Mitigation: Use it only on trusted archives and inspect the destination folder before running it on important data.

Risk: Source archives are automatically deleted after successful extraction.

Mitigation: Keep backups or run the skill on copies when the original archives must be preserved.

Risk: Crafted archives may overwrite files outside the intended target folder or exhaust disk or memory.

Mitigation: Avoid untrusted archives, use a contained working directory, and monitor available disk space during extraction.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tang-dafa/skills/unzip-all)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with command examples and extraction status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces extracted files on disk and reports failed or remaining archives.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
