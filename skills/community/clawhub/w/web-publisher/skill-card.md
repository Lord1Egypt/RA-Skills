## Description:

Converts web articles and local documents into Markdown or WeChat public-account drafts and posts, with optional AI rewriting through siping.me services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sipingme](https://clawhub.ai/user/sipingme)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content operators use this skill to convert web pages or local documents into WeChat-ready drafts, published posts, or standalone Markdown. Developers and agents can also use it to handle login, account configuration, job status, and document conversion workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles WeChat publishing authority and account credentials through siping.me services.

Mitigation: Install only when the user trusts siping.me with article content, publishing authority, and AppID/AppSecret handling; use logout and confirm service-side API-key revocation when access should end.

Risk: Configuration links and service endpoints could expose sensitive setup data if they are not the expected HTTPS siping.me links.

Mitigation: Verify onboarding and configuration URLs use HTTPS on the expected siping.me domains before entering credentials or continuing setup.

Risk: Direct publish actions can make content public through the connected WeChat account.

Mitigation: Use draft mode by default and reserve publish mode for explicit user requests; review generated or converted content before publication.

Risk: The optional news-to-markdown fallback runs separate local code outside this skill's audit scope.

Mitigation: Treat the fallback as separately trusted software; use the pinned documented version with installation scripts disabled, preserve a lockfile, or provide already extracted content instead.

Risk: Local document publishing uploads user-supplied files to remote conversion and publishing services.

Mitigation: Upload only files the user explicitly provides or authorizes; keep the documented 50 MiB cap and reject files that change during bounded reads.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sipingme/skills/web-publisher)
- [Publisher profile](https://clawhub.ai/user/sipingme)
- [Markdown themes reference](references/markdown-themes.md)
- [Microsoft MarkItDown](https://github.com/microsoft/markitdown)
- [news-to-markdown fallback skill](https://github.com/sipingme/news-to-markdown-skill)
- [browser-web-search companion skill](https://github.com/sipingme/browser-web-search-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, shell command invocations, JSON status and result summaries, and optional Markdown files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Publishing commands return job, media, or publish identifiers; conversion can write Markdown to a user-specified output path.]

## Skill Version(s):

0.10.2 (source: frontmatter and server evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
