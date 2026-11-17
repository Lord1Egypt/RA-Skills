## Description:

Scans a skill directory for security issues and best practices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liverock](https://clawhub.ai/user/liverock)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill reviewers use this skill to scan Python skill directories for security issues, misconfigurations, and best-practice concerns before review or deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner is heuristic and may overstate scan completeness.

Mitigation: Use its report as a review aid, not as a definitive security gate.

Risk: Markdown reports can be influenced by scanned filenames or code strings.

Mitigation: Treat generated reports as untrusted evidence and review them before sharing or acting on them.

Risk: The scanner reads directories selected by the caller.

Mitigation: Run it only on skill directories or paths that were intentionally chosen for review.

## Reference(s):

- [Security Sentinel Ultimate on ClawHub](https://clawhub.ai/liverock/skills/security-sentinel-ultimate)
- [liverock publisher profile](https://clawhub.ai/user/liverock)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown report with severity summaries and findings tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports findings grouped by file and category with critical, warning, and OK severity labels.]

## Skill Version(s):

0.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
