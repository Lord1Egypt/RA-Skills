## Description:

Give this agent a real, routable IPv6 (/128) identity on the Whisper network, with safe egress and externally-verifiable identity through DNSSEC and RDAP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kakooch](https://clawhub.ai/user/kakooch)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to assign an agent a stable, attributable IPv6 egress identity on the Whisper network or to verify a Whisper agent identity without an account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs users to run an internet installer in a shell before using the Whisper CLI.

Mitigation: Review the installer before use, prefer a versioned signed release with checksum or signature verification, and run it without administrative privileges.

Risk: Identity creation and egress use a credentialed network identity, and connected traffic may be attributed to that identity.

Mitigation: Use a narrowly scoped Whisper API key where available, avoid hard-coding credentials, and confirm that operators understand the attribution model before enabling egress.

## Reference(s):

- [Whisper homepage](https://whisper.online)
- [Whisper documentation](https://whisper.online/docs)
- [ClawHub skill page](https://clawhub.ai/kakooch/skills/whisper-identity)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Verification commands are keyless; identity creation and egress setup require a Whisper API key.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
