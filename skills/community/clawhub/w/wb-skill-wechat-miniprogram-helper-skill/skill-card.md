## Description:

This skill helps users build, develop, debug, and publish WeChat Mini Programs, including project scaffolding, core Mini Program architecture, common error fixes, AppID setup, experience-member permissions, and release workflow guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haohao642](https://clawhub.ai/user/haohao642)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and builders use this skill to create runnable native WeChat Mini Program projects, apply Mini Program development patterns, debug common runtime and publishing issues, and prepare an app for preview, review, and release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scaffolder can overwrite fixed starter files when run against an existing project with --force.

Mitigation: Choose an empty target directory unless overwrite behavior is intentional; the scaffolder checks for conflicts and aborts in non-interactive mode without --force.

Risk: Local DevTools domain, TLS, or HTTPS checks may be bypassed during debugging.

Mitigation: Use the bypass only for local development and configure proper HTTPS request, upload, and download domains before publishing.

## Reference(s):

- [Architecture and Basics](references/architecture-and-basics.md)
- [Common Pitfalls](references/common-pitfalls.md)
- [Publishing](references/publishing.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code snippets, shell commands, and generated project files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate a local WeChat Mini Program starter project when the scaffolder is invoked.]

## Skill Version(s):

0.1.2 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
