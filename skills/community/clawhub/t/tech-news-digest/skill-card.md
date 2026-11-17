## Description:

Generate tech news digests with unified source model, quality scoring, and multi-format output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinstein](https://clawhub.ai/user/dinstein)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical teams use this skill to collect, score, deduplicate, summarize, archive, and deliver recurring technology news digests across RSS, Twitter/X, GitHub, Reddit, and web search sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled shell workflows can repeatedly run the digest pipeline and deliver results outside the workspace.

Mitigation: Review every scheduled job, workspace path, channel ID, email address, and delivery destination before enabling automation.

Risk: The skill can use API tokens and credential fallbacks for Twitter/X, web search, and GitHub.

Mitigation: Use least-privilege tokens in a dedicated workspace and avoid GH_APP_KEY_FILE or gh CLI fallback unless those paths are required.

Risk: Configurable source URLs and enrichment fetch external content that may be untrusted.

Mitigation: Use trusted source configurations, disable enrichment for untrusted feeds, and do not import third-party source configs until private-network URL blocking and safer command construction are added.

## Reference(s):

- [Tech News Digest Source Repository](https://github.com/draco-agent/tech-news-digest)
- [Digest Prompt Template](references/digest-prompt.md)
- [Discord Output Template](references/templates/discord.md)
- [Email Output Template](references/templates/email.md)
- [PDF Output Template](references/templates/pdf.md)
- [ClawHub Skill Page](https://clawhub.ai/dinstein/skills/tech-news-digest)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, HTML email, PDF-oriented markdown, JSON pipeline data, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces quality-scored digest content, source-count metadata, archive files, optional email HTML, and optional PDF attachments.]

## Skill Version(s):

3.16.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
