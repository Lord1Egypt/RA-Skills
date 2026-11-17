## Description:

Runs a local, read-only eight-dimension health check for a WorkBuddy environment, covering disk health, backup freshness, automation status, hardcoded credential indicators, backup package integrity, configuration, memory sync, and cross-machine backup carrier readiness.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT

## Use Case:

Developers and WorkBuddy operators use this skill to run a local environment health check before maintenance, backup, recovery, or cross-machine synchronization. It produces a prioritized remediation list so users can review CRIT, WARN, and advisory findings before taking action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports may contain local backup path information.

Mitigation: Review reports before sharing them outside the local environment and remove sensitive paths when necessary.

Risk: Release integrity evidence is not fully consistent because the security evidence says the recorded SKILL.md hash does not match the inspected file.

Mitigation: Verify the package hashes against the installed artifact before trusting attestation claims or redistributing the release.

Risk: The authoritative security verdict is suspicious because privacy and integrity claims do not fully match the shipped artifacts.

Mitigation: Review before installing, and treat security claims as release evidence that needs confirmation in the target environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaoxinghua09-cell/skills/workbuddy-health-check)
- [Publisher profile](https://clawhub.ai/user/zhaoxinghua09-cell)
- [Attestation](artifact/ATTESTATION.md)
- [Security test results](artifact/tests/security_results.json)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown report and JSON summary, with optional shell command usage shown in the skill documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are written locally under the configured output directory and retain the most recent health-check outputs.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
