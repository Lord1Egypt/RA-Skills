## Description:

Sandboxed ClawHub skill installation with automated security scanning for installing, auditing, and promoting skills through staging, scanning, promotion, or quarantine.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zurbrick](https://clawhub.ai/user/zurbrick)

### License/Terms of Use:


## Use Case:

Developers and security reviewers use this skill to install or audit ClawHub skills by staging them, running static security checks, and promoting clean results or quarantining flagged content for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer can automatically replace live skills and has path-handling flaws that could affect files outside the intended skill folders.

Mitigation: Use only in a disposable or backed-up OpenClaw workspace; avoid --force, --promote, and custom live or staging directories unless the exact staged contents have been manually verified.

Risk: Promotion can move staged skill content into the live skills directory after review.

Mitigation: Manually inspect staged files before promotion, keep backups of live skills, and prefer a fixed version that validates skill names, canonicalizes paths, records scan hashes, and asks before replacement.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zurbrick/skills/skill-sandbox)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash commands and terminal-oriented guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces security scan verdicts and promotion or quarantine guidance for staged ClawHub skills.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
