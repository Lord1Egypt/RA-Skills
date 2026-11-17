## Description:

Publishes Markdown articles to WeChat Official Accounts by converting Markdown to WeChat-friendly HTML, uploading cover images, creating drafts, and providing API or manual publishing guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shimonxin](https://clawhub.ai/user/shimonxin)

### License/Terms of Use:

MIT-0

## Use Case:

Content operators and developers use this skill to turn Markdown with YAML frontmatter into WeChat Official Account drafts or publications while checking account limits, cover image requirements, and common API errors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use WeChat credentials to create, publish, list, and delete account drafts.

Mitigation: Review commands before execution, test with non-sensitive drafts first, and confirm the target media_id before deleting or publishing.

Risk: Stored WeChat configuration and token files can expose account access if permissions are loose.

Mitigation: Store ~/.config/wx-mp securely, restrict token-file permissions, and rotate credentials if account access is uncertain.

Risk: The rebuild script contains hardcoded media IDs and local article paths.

Mitigation: Avoid running the rebuild script unless the paths and media IDs have been reviewed for the intended account.

Risk: Dependency provenance may be affected by the lockfile using a non-HTTPS registry mirror.

Mitigation: Prefer a consistent HTTPS registry and refresh dependencies before production use.

## Reference(s):

- [WeChat publishing best practices](references/best-practices.md)
- [ClawHub skill page](https://clawhub.ai/shimonxin/skills/wx-mp-publish)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated WeChat-ready HTML handled by scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create, publish, list, or delete WeChat drafts when run with account credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata and scripts/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
