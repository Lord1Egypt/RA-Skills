## Description:

This skill claims to analyze blockchain sandwich operations, but the packaged shell tool behaves as a local note and configuration manager.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers can use this skill to inspect or run the packaged local storage commands while accounting for the mismatch with the stated blockchain-analysis purpose.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release is mislabeled: it claims blockchain sandwich analysis, while the packaged behavior is local note and configuration management.

Mitigation: Review the purpose before installation and do not rely on it for protocol security analysis until the documentation and behavior are aligned.

Risk: The tool persists user-entered data under ~/.sandwich by default and can export local files.

Mitigation: Avoid sensitive inputs, set SANDWICH_DIR to a reviewed location, and review exported files before sharing.

Risk: The remove command deletes stored records by line number.

Mitigation: Verify the target line or back up the data file before removal.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ckchzh/skills/sandwich)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Files]

**Output Format:** [Plain text command output with JSONL or CSV export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and reads local data under SANDWICH_DIR, defaulting to ~/.sandwich.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
