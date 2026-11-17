## Description:

Builds verifiable evidence that a ClawHub release is published, approved, and installable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bonniegeng-max](https://clawhub.ai/user/bonniegeng-max)

### License/Terms of Use:

MIT-0

## Use Case:

Skill publishers and developers use this skill to check whether a pushed release reached ClawHub, passed moderation, and can be installed, then document the evidence and any gaps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Checking the wrong skill or version can produce a misleading release conclusion.

Mitigation: Confirm the target slug and version before checking repository, registry, and installation evidence.

Risk: An optional installation check may increase public install or download metrics.

Mitigation: Install in an isolated directory and record the time, slug, version, reason, and affected metrics interval.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bonniegeng-max/skills/release-proof-builder)
- [Project homepage](https://github.com/bonniegeng-max/openclaw-publisher)
- [Evidence levels](references/evidence_levels.md)
- [Verification commands](references/verification_commands.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Shell commands]

**Output Format:** [Markdown evidence report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes an E0–E4 evidence level, verified and missing evidence, conflicting signals, and next steps.]

## Skill Version(s):

1.0.5 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
