## Description:

Audit, debug, and clean up installed OpenClaw skills by detecting trigger conflicts, inline security red flags, stale versions, and likely skill matches for a prompt.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chris](https://clawhub.ai/user/chris)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use Skill Doctor to audit an installed OpenClaw skill collection, find overlapping triggers, review suspicious inline patterns, check release freshness, and debug which skill is likely to handle a prompt.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local scanner can follow symlinks or otherwise read outside the intended skill directory.

Mitigation: Run it only on trusted installed-skill directories, avoid untrusted directories that may contain symlinks, and pass an explicit --skills-dir path when auditing a known collection.

Risk: Security reports may include matched source lines that expose secrets or sensitive local content.

Mitigation: Review generated reports before sharing them, redact secrets or private paths, and treat findings as prompts for human review rather than proof of malicious behavior.

## Reference(s):

- [Skill Doctor on ClawHub](https://clawhub.ai/chris/skills/skill-doctor-audit)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally against installed skill directories; optional ClawHub CLI enables stale-version checks.]

## Skill Version(s):

1.0.0 (source: frontmatter, changelog, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
