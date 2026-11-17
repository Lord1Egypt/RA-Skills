## Description:

The Yoder Skill Auditor scans OpenClaw and ClawHub skills for security issues, trust-score signals, update regressions, and benchmark results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yoder-bawt](https://clawhub.ai/user/yoder-bawt)

### License/Terms of Use:

MIT

## Use Case:

Developers and security reviewers use this skill to audit OpenClaw and ClawHub skills before installation, compare versions for regressions, generate trust scores, and produce scan reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The inspected published artifact includes runnable malicious test scripts and scanner weaknesses.

Mitigation: Do not install the artifact as-is; ask the publisher to exclude tests or ship only inert fixture data and to fix the scanner issues identified by clawscan.

Risk: The artifact contains intentionally malicious test fixtures that are only meant for detection testing.

Mitigation: Evaluate only in a sandbox without credentials, sudo access, or outbound network access, and do not execute fixture files outside the test harness.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yoder-bawt/skills/yoder-skill-auditor)
- [Publisher Profile](https://clawhub.ai/user/yoder-bawt)
- [CHANGELOG.md](artifact/CHANGELOG.md)
- [TEST-FIXTURES-WARNING.md](artifact/TEST-FIXTURES-WARNING.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Terminal text, JSON scan output, Markdown reports, and command-oriented guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Audit commands return pass, review, fail, or error exit codes; trust scoring reports a 0-100 score with grade labels.]

## Skill Version(s):

3.1.0 (source: server release metadata, artifact/SKILL.md frontmatter, artifact/skill.json, artifact/CHANGELOG.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
