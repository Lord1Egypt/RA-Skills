## Description:

Security-first skill vetting for AI agents that checks red flags, permission scope, suspicious patterns, and provides risk assessment and safety recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ttttstc](https://clawhub.ai/user/ttttstc)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill before installing external skills to review code patterns, dependency advisory signals, permissions, and installation risk.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security review says the skill-safety results may be untrustworthy until TLS verification and incomplete scan handling are fixed.

Mitigation: Treat scan results as advisory, review the code before approving a skill, and fix TLS verification and incomplete-result reporting before relying on it for install decisions.

Risk: The release guidance warns against direct-download execution from a mutable branch.

Mitigation: Install from pinned releases or checksum-verified artifacts instead of executing raw files from a moving branch.

Risk: The server security verdict is suspicious.

Mitigation: Run the skill in a constrained environment and avoid exposing credentials or broad filesystem access during evaluation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ttttstc/skills/skill-safety-verifier)
- [GitHub Advisory API](https://api.github.com/advisories)
- [OpenClaw Security Docs](https://docs.openclaw.ai/security)
- [OpenClaw Skill Writing Guide](https://docs.openclaw.ai/skills/write)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown risk summaries, terminal risk radar output, and optional JSON analysis.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include network, vulnerability, permission, and total risk scores with warnings and recommendations.]

## Skill Version(s):

0.1.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
