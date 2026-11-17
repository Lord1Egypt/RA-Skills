## Description:

Guarantee instruction compliance with root cause analysis, flow verification, and automated validators that make future failures impossible.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill when an instruction failure must not recur. It guides severity assessment, root cause analysis, instruction flow verification, and creation of local validator scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates persistent local enforcement state and may propose executable validators that affect future agent behavior.

Mitigation: Use manual or ask-first setup modes, and review every proposed AGENTS.md, HEARTBEAT.md, hook, and validator change before approval.

Risk: Validator examples may be fragile if used as security-critical controls without hardening.

Mitigation: Harden and test validator scripts before relying on them for security-sensitive protection.

## Reference(s):

- [Self Discipline ClawHub page](https://clawhub.ai/ivangdavila/skills/self-discipline)
- [Self Discipline homepage](https://clawic.com/skills/self-discipline)
- [Setup](setup.md)
- [Memory Template](memory-template.md)
- [Severity Assessment](severity.md)
- [Root Cause Analysis](root-cause.md)
- [Flow Verification](flow-verification.md)
- [Validator Patterns](validators.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local files under ~/self-discipline/ and validator scripts after user approval.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
