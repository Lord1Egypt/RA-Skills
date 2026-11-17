## Description:

Audits locally installed AI skills against skillguard.vip's public security database and reports blocked, high-risk, medium, safe, unaudited, or errored results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangyixxxx](https://clawhub.ai/user/yangyixxxx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to check installed skill bundles before invoking them or after installation. It helps surface blocked and high-risk audit results with links to canonical audit pages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends locally installed skill directory names to skillguard.vip for lookup.

Mitigation: Use explicit checks when local skill names are sensitive, and understand this network lookup before installation.

Risk: Mutable main-branch install commands can change after review.

Mitigation: Prefer a reviewed ClawHub package or a pinned, verified commit for installation.

Risk: Private, unpublished, or same-named skills may be unaudited or mismatched because lookup is based on skill slug.

Mitigation: Treat unaudited or mismatched results as requiring manual review, and use the canonical audit page as the source of truth.

Risk: The public audit verdict may lag behind a republished skill version.

Mitigation: Check the audit page timestamp and rerun or request a fresh scan when the installed package may differ from the stored verdict.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yangyixxxx/skills/skillguard-check)
- [skillguard.vip homepage](https://skillguard.vip)
- [skillguard-check audit page](https://skillguard.vip/skills/clawhub/skillguard-check)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [JSON report with human-facing summary guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Exit code 1 indicates blocked or high-risk skills were found; no files are written.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
