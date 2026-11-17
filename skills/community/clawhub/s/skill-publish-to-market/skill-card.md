## Description:

Publishes SKILL.md packages to ClawHub, Anthropic Skills, ECC Community, and skills.sh by guiding credential checks, quality validation, platform adaptation, API calls, pull request creation, conflict handling, and status reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to publish SKILL.md-compatible skills across marketplace platforms. It supports quality checks, credential verification, platform-specific payload preparation, pull requests, retries, partial-failure handling, and status checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for powerful GitHub and ClawHub credentials and automates external uploads and repository changes.

Mitigation: Use narrow, short-lived tokens, prefer fine-grained GitHub tokens when possible, mask tokens in output, and revoke credentials after publishing.

Risk: The security evidence flags weak scoping and unsafe command-template handling for shell and JSON publishing templates.

Mitigation: Review the exact files, target platforms, generated curl payloads, and skill package trust level before execution; avoid publishing untrusted packages until escaping is fixed.

Risk: Automated pull requests and retries can create duplicate or unintended marketplace submissions when a platform returns partial or indeterminate results.

Mitigation: Check existing pull requests and live ClawHub versions before retrying failed GitHub-backed platforms or version-conflict paths.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dingtom336-gif/skills/skill-publish-to-market)
- [README](artifact/README.md)
- [API Request Templates](artifact/references/templates.md)
- [Publishing Playbooks](artifact/references/playbooks.md)
- [Error Recovery Paths](artifact/references/fallbacks.md)
- [Execution Log Schema](artifact/references/runbook.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, JSON, Guidance]

**Output Format:** [Markdown status tables with inline shell commands and optional JSON execution logs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include PR URLs, ClawHub slug/version identifiers, quality-gate results, retry guidance, and partial-success status.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
