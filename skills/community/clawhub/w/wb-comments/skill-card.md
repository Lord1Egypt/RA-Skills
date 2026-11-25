## Description:

Collects public Weibo post comments in user-approved steps, supports selective reply expansion, and exports collected comments as CSV.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mystery77777777](https://clawhub.ai/user/mystery77777777)

### License/Terms of Use:

MIT-0

## Use Case:

External users use the skill to inspect comment counts, collect public Weibo comments page by page, selectively expand replies, and export results. The agent reports the estimated volume first and asks before each billable collection step.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates the skill suspicious, citing insecure connection settings and collection capabilities beyond its stated Weibo-only purpose.

Mitigation: Review these reported concerns before installation. The documentation says the default HTTP service sends tokens in plaintext; use a trusted HTTPS endpoint where available and avoid disabling certificate checks.

Risk: Security analysis is incomplete: only 2 of 6 components were fully inspected and tool-misuse analysis was degraded.

Mitigation: Treat the scan as incomplete and review the skill files and configuration behavior before installation.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/mystery77777777/skills/wb-comments)

## Skill Output:

**Output Type(s):** [JSON, CSV files, shell commands, user guidance]

**Output Format:** [JSON command responses and CSV exports (UTF-8 with BOM)]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Comment results include main comments and, when requested, replies; collection proceeds in user-approved steps.]

## Skill Version(s):

1.0.0 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
