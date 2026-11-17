## Description:

Use before making a private repository public, before the first push of a new public repo, or when the user asks "is this safe to publish", "check for leaks", or wants a pre-publication scan. Also use after discovering identifying content already leaked into a public repo's history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[escoffier-labs](https://clawhub.ai/user/escoffier-labs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to assess whether a repository is ready to publish by checking its working tree, commit history, repository hygiene, and remote state. It produces a ship-or-fix-first assessment with evidence and remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The cleanup guidance proposes disruptive history rewrites, remote updates, and repository deletion, while removal from all copies cannot be guaranteed.

Mitigation: Use the reporting workflow first; require approval before remote changes or deletion; protect backups containing leaked data; rotate exposed credentials promptly; and do not treat a fresh clone as proof that forks, caches, or other copies are clean.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/escoffier-labs/skills/publish-readiness)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with a pass/fail checklist and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Evidence-based ship-or-fix-first verdict with remediation steps]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
