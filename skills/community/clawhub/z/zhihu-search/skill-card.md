## Description:

Zhihu Search helps an agent fetch Zhihu search results, question answers, column articles, comments, and hot-list items using a user-provided Zhihu session cookie.

This skill is ready for commercial/non-commercial use.

## Publisher:

[excalibursssooo](https://clawhub.ai/user/excalibursssooo)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill for read-only Zhihu topic research, trend review, answer summarization, column article collection, and comment inspection. It is intended for workflows that need concise Markdown or JSON outputs from Zhihu content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles a live Zhihu session cookie, which can expose account access if stored or shared improperly.

Mitigation: Use a dedicated low-risk account, keep cookie and state files outside shared or committed directories, use owner-only file permissions, and verify sensitive data is not added to git.

Risk: Security evidence flags unsafe persistence and process-control behavior around keepalive and cron usage.

Mitigation: Do not run install-cron or keepalive automation until the cron quoting and process-kill behavior are fixed and reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/excalibursssooo/skills/zhihu-search)
- [Artifact README](artifact/README.md)
- [Artifact changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries, JSON files, and command-line output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports compact summaries, explicit Markdown file output, local JSON caches, and environment-variable path overrides.]

## Skill Version(s):

1.1.0 (source: frontmatter, changelog, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
