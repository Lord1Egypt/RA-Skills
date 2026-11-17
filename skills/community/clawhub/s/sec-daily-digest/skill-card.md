## Description:

Generates a cybersecurity daily or weekly digest from CyberSecurityRSS OPML feeds and Twitter/X security accounts, with provider selection, recent-window filtering, archive deduplication, vulnerability merging, source health monitoring, and Markdown output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zer0yu](https://clawhub.ai/user/zer0yu)

### License/Terms of Use:


## Use Case:

Cybersecurity researchers and security teams use this skill to collect recent security and AI-related items, rank and deduplicate them, merge vulnerability events, and produce a bilingual Markdown digest for daily or weekly review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Network fetching can be directed at internal or private-network URLs.

Mitigation: Review configured RSS sources before use and add outbound URL validation in corporate, cloud, or private-network environments.

Risk: AI provider and email features can send collected content outside the local machine.

Mitigation: Use approved AI providers and recipients, prefer dry-run for sensitive material, and avoid --enrich or --email unless the data is suitable for external processing or delivery.

## Reference(s):

- [Sec Daily Digest skill page](https://clawhub.ai/zer0yu/skills/sec-daily-digest)
- [Digest prompt templates](references/digest-prompt.md)
- [gogcli email delivery dependency](https://github.com/steipete/gogcli)
- [twitterapi.io API provider](https://twitterapi.io)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown digest with optional shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write digest files, update local state, and optionally send email when configured.]

## Skill Version(s):

0.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
