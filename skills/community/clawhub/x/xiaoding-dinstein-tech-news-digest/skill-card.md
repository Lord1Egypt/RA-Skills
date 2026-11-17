## Description:

Generates tech news digests by collecting RSS, Twitter/X, GitHub releases and trending repositories, Reddit, and web search sources into quality-scored, deduplicated Discord, email, Markdown, or PDF outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asterisk622](https://clawhub.ai/user/asterisk622)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and teams use this skill to configure and schedule daily or weekly technology news digests from predefined and workspace-specific sources. It supports source collection, scoring, deduplication, archiving, and delivery-oriented report generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad URL fetching can contact configured RSS, web search, GitHub, Reddit, and Twitter/X endpoints, including URLs supplied through workspace configuration.

Mitigation: Use only trusted source configuration files and run the skill in an environment with appropriate outbound network controls, especially near private networks or cloud metadata services.

Risk: Optional API credentials for GitHub, Twitter/X, Tavily, and Brave may be used by collection scripts.

Mitigation: Provide narrowly scoped credentials, avoid broad GitHub tokens, and rotate keys according to the owning service's policy.

Risk: Full-text enrichment fetches article pages beyond the initial source metadata.

Mitigation: Disable enrichment unless richer article summaries are needed.

Risk: Scheduled delivery can send digests to Discord channels or email recipients.

Mitigation: Confirm channel IDs, email recipients, and schedule settings before enabling recurring delivery.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/asterisk622/skills/xiaoding-dinstein-tech-news-digest)
- [Digest prompt template](references/digest-prompt.md)
- [Configuration schema](config/schema.json)
- [Discord output template](references/templates/discord.md)
- [Email output template](references/templates/email.md)
- [PDF output template](references/templates/pdf.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON pipeline data, shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can generate Discord-ready Markdown, email HTML, archived Markdown reports, and optional PDF attachments.]

## Skill Version(s):

3.15.0 (source: server release metadata, SKILL.md frontmatter, and changelog released 2026-03-15)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
