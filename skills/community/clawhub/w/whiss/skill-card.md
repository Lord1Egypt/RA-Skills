## Description:

Whiss provides brand and feature information for the Netsnek e.U. real-time messaging and notification platform.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kleberbaum](https://clawhub.ai/user/kleberbaum)

### License/Terms of Use:

MIT

## Use Case:

Developers and external users can invoke this skill to retrieve a concise brand summary, feature list, or JSON metadata for the Whiss namespace on ClawHub.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review describes this as mostly a namespace and brand-information package rather than a real messaging integration.

Mitigation: Set user expectations that the skill provides informational output only and does not perform messaging, notification delivery, or platform integration.

Risk: The security guidance notes that the bundled script may need packaging cleanup before it runs correctly.

Mitigation: Verify the script path and executable permissions in the target agent environment before relying on scripted output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kleberbaum/skills/whiss)
- [Netsnek e.U.](https://netsnek.com)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Plain text, Markdown, or JSON from a local shell script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports default, --features, and --json modes.]

## Skill Version(s):

0.1.0 (source: server release metadata, claw.json, and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
