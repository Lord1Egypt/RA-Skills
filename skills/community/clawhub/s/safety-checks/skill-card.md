## Description:

Verify before you trust: model pinning, fallbacks, and runtime safety validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leegitw](https://clawhub.ai/user/leegitw)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to run pre-flight and heartbeat safety checks for model version drift, fallback configuration, stale cache data, and cross-session state contamination.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional dependency install commands may add related skills whose versions and trust posture should be reviewed before use.

Mitigation: Review why context-verifier, failure-memory, and constraint-engine are needed, and prefer pinned or trusted versions if OpenClaw supports them.

Risk: Safety checks read local configuration and cache metadata and write local safety logs.

Mitigation: Confirm the configured paths match the documented .openclaw, .claude, and output/safety locations before running clear or remediation commands.

## Reference(s):

- [Safety Checks on ClawHub](https://clawhub.ai/leegitw/skills/safety-checks)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown command guidance and plain-text check reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local check results under output/safety/ and uses local safety-check configuration files.]

## Skill Version(s):

1.5.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
