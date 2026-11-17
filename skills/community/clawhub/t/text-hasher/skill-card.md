## Description:

Compute SHA-256 or MD5 hashes of text strings. Useful for quick integrity checks, deduplication, and content fingerprinting without leaving the terminal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical users use this skill to generate SHA-256 or MD5 fingerprints for pasted text, stdin streams, or named files when checking integrity, deduplicating content, or comparing text values.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may guide an agent to hash a named file, which requires the agent to read that file.

Mitigation: Use it only on files the user intends the agent to access, and review proposed commands before execution.

Risk: MD5 is unsuitable for adversarial integrity or security-sensitive collision resistance.

Mitigation: Prefer SHA-256 for security-relevant checks and use MD5 only for non-security fingerprinting or legacy comparison needs.

## Reference(s):

- [ClawHub skill page: text-hasher](https://clawhub.ai/terrycarter1985/skills/text-hasher)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and plain-text hash output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local command guidance for SHA-256 or MD5 hashing; no network use or credential handling is indicated by the security evidence.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
