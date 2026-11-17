## Description:

Create a timestamped backup copy of a file in the same directory when the user wants to save a copy before making changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jinwangmok](https://clawhub.ai/user/jinwangmok)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create a timestamped backup of a local file before editing or replacing it.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: In shared or untrusted directories, predictable timestamped backup names may overwrite an existing backup or interact poorly with symlinks.

Mitigation: Write backups only to trusted directories and verify the backup path before relying on it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jinwangmok/skills/simple-file-backup)
- [MANUAL.md](artifact/MANUAL.md)

## Skill Output:

**Output Type(s):** [shell commands, text, files]

**Output Format:** [Shell command execution with plain-text status or error output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a timestamped backup file using cp and date; no output is expected from the SKILL.md command on success, while run.sh prints the created backup path.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
