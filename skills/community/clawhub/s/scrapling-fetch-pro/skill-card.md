## Description:

Scrapling Fetch Pro helps agents fetch web page content, extract article bodies, clean common noise, and return Markdown or JSON, including support for WeChat public-account articles and stealth fetching modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shuxiangfanclaw](https://clawhub.ai/user/shuxiangfanclaw)

### License/Terms of Use:

MIT

## Use Case:

Developers and external agent users use this skill to retrieve article-like content from blogs, news pages, announcements, WeChat public-account articles, and pages that may require browser-based fetching. It is intended to provide scraped content to an agent as Markdown or structured JSON for downstream reading, summarization, or analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill accepts arbitrary URLs and can fetch content from broad web targets.

Mitigation: Run it only in controlled environments and avoid networks that can reach private services, internal hosts, or cloud metadata endpoints.

Risk: The skill includes stealth behavior for anti-bot or protected pages.

Mitigation: Use stealth mode only for sites where the operator is authorized to fetch content and where the site's terms and applicable rules permit automated access.

Risk: Scraped page content can be untrusted or misleading when passed to an agent.

Mitigation: Treat fetched content as untrusted input, keep it separate from instructions, and review downstream agent outputs before acting on them.

## Reference(s):

- [Usage Guide](artifact/references/usage.md)
- [ClawHub Skill Page](https://clawhub.ai/shuxiangfanclaw/skills/scrapling-fetch-pro)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown text by default, or JSON when requested with the command-line flag]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The script accepts a URL, optional maximum character count, fetch mode selection, JSON output mode, and debug output mode; text output may be truncated at the requested character limit.]

## Skill Version(s):

1.2.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
