## Description:

Scans installed OpenClaw skills for malicious patterns including prompt injection, credential theft, data exfiltration, obfuscated payloads, and backdoors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[itsclawdbro](https://clawhub.ai/user/itsclawdbro)

### License/Terms of Use:


## Use Case:

Developers and security reviewers use Skill Defender to scan individual or installed OpenClaw skills for deterministic malicious-pattern findings before installation, after updates, or during periodic audits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary reports broad bypass and coverage gaps that could make unsafe skills look clean.

Mitigation: Treat clean results as advisory and require independent review before using the scan result for approval decisions.

Risk: Skipped directories, symlinks, allowlists, or excluded patterns may reduce scan coverage.

Mitigation: Review scan scope and suppression choices, especially for clean aggregate verdicts.

Risk: The release security verdict is suspicious even though no discrete risk findings were reported.

Mitigation: Install only when the user accepts the advisory posture and understands it is not a definitive security gate.

## Reference(s):

- [Threat Patterns Reference](references/threat-patterns.md)
- [ClawHub Skill Page](https://clawhub.ai/itsclawdbro/skills/skill-defender)

## Skill Output:

**Output Type(s):** [analysis, json, shell commands, guidance]

**Output Format:** [Human-readable text or JSON scan reports with verdicts, findings, counts, and timestamps.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses deterministic pattern matching and may suppress known false positives through allowlists or exclusions.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
