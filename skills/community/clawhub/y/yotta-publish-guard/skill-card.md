## Description:

A general pre-publish release guard that checks skill contents, package contents, version alignment, name availability, and gated publishing commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yottameta](https://clawhub.ai/user/yottameta)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release teams use it to check skills before publishing to GitHub, npm, or ClawHub and to prepare a gated publish plan. Its reports support human review and do not make the release decision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Package checks described as dry-run or read-only may run package lifecycle scripts.

Mitigation: Review lifecycle scripts in the selected package before running pack; a dry-run is not an execution sandbox.

Risk: Command quoting defects can allow unintended commands, particularly with untrusted paths or metadata on Windows.

Mitigation: Correct and review command escaping before using untrusted paths or metadata, especially on Windows.

Risk: Network failures can leave package or repository name availability unconfirmed, and publish execution can affect public channels.

Mitigation: Manually verify names after network errors, and inspect the public repository, publishing organization, and selected channels before authorizing --exec.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/yottameta/skills/yotta-publish-guard)
- [Project homepage](https://github.com/YottaMeta/yotta-publish-guard)
- [Publish flow](references/publish-flow.md)
- [Check items](references/check-items.md)
- [Tutorial](references/tutorial.md)

## Skill Output:

**Output Type(s):** [Analysis, Text reports, Shell commands]

**Output Format:** [Markdown reports and shell command plans]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Publish plans default to dry-run; execution requires --exec.]

## Skill Version(s):

0.4.5 (source: frontmatter, package.json, CHANGELOG.md; released 2026-11-05)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
