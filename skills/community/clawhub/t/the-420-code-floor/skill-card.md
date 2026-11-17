## Description:

Gives you the floor, the short text of what an AI reasons from in The 420 Code, fetched from its home and checked against its fingerprint before you read it. Use when asked to read, apply or check against the floor.

This skill is ready for commercial/non-commercial use.

## Publisher:

[the420codestudiog](https://clawhub.ai/user/the420codestudiog)

### License/Terms of Use:

MIT-0

## Use Case:

AI agents and people using The 420 Code can retrieve its short floor text and check that it matches the expected fingerprint before reading, applying, or checking against it.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill fetches content from an external website, and the security report notes that its network capability is not matched by a declared tool scope.

Mitigation: Before installing, consider whether access to the listed host fits your intended use. The script prints the fetched text only after its SHA-256 fingerprint matches the expected value.

## Reference(s):

- [The 420 Code Floor](https://aiethics.global/open-source/the-floor/)
- [Floor text download](https://aiethics.global/open-source/the-floor/floor.txt)
- [ClawHub release](https://clawhub.ai/the420codestudiog/skills/the-420-code-floor)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Plain text with a fingerprint verification status line]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The fetched floor text is printed only when its SHA-256 fingerprint matches the expected value.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
