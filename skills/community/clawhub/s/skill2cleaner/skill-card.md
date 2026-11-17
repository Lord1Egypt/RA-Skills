## Description:

Scans workspace skills to check whether authorization, configuration, and environment variables are complete, and can disable or uninstall invalid skills when requested.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edde-101](https://clawhub.ai/user/edde-101)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to inspect installed skills for missing API keys, disabled configuration, or missing skill files, then produce a health report or clean invalid skills after review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can disable or forcibly uninstall installed skills without its own validity check or confirmation gate.

Mitigation: Use report-only mode by default, verify exact skill names before cleanup, and require explicit confirmation before running disable or uninstall actions.

Risk: Cleanup actions may affect valid skills if an unverified name is supplied.

Mitigation: Validate requested skill names exactly and reject valid skills during cleanup.

Risk: The dependency declaration allows broad PyYAML versions.

Mitigation: Pin PyYAML before broad deployment.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text diagnostic reports and command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Report mode lists valid and invalid skills with reasons; clean mode can disable or uninstall named skills.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
