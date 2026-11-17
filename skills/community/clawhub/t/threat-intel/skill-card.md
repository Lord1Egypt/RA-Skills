## Description:

Arabic-first OSINT and threat intelligence skill for monitoring Arabic-language threat actor channels on Telegram, generating bilingual threat reports, searching dark web indexes via Tor, and enumerating subdomains via Certificate Transparency logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abdullah944](https://clawhub.ai/user/abdullah944)

### License/Terms of Use:

MIT-0

## Use Case:

External analysts, SOC teams, OSINT investigators, journalists, researchers, and enterprise security teams use this skill to monitor Arabic-language threat activity, produce bilingual threat briefs, search Tor-accessible dark web indexes, and discover subdomains from public CT logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends user queries and targets to Telegram, crt.sh, and Tor-accessible onion search services.

Mitigation: Use it only in environments where outbound OSINT and Tor lookups are approved, avoid sensitive search terms, and document the external services contacted.

Risk: Returned Telegram and onion content may be incomplete, misleading, or malicious.

Mitigation: Treat all remote content as untrusted evidence and review findings before sharing or taking action.

Risk: The skill requests broad execution and write authority relative to its described OSINT behavior.

Mitigation: Narrow tool permissions before deployment and remove unused write authority where it is not required.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/abdullah944/skills/threat-intel)
- [Publisher Profile](https://clawhub.ai/user/abdullah944)
- [Telegram Public Channel Web View](https://t.me/s/{channel})
- [crt.sh Certificate Transparency Search](https://crt.sh/?q=%25.{domain}&output=json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Console text and Markdown-style threat intelligence summaries, with structured snippets for Telegram posts, Tor search results, and CT log findings.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports channel, report, darkweb, and scan commands with language and region options.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter and changelog list 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
