## Description: <br>
Basic web page fetching utility that supports anti-bot bypass, automatic main-content extraction, and HTML-to-Markdown conversion for blogs, news, announcements, and other static pages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shuxiangfanclaw](https://clawhub.ai/user/shuxiangfanclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to fetch web pages, extract likely article content, and convert the result to Markdown or JSON for downstream reading, summarization, or analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can fetch third-party websites, including with stealth mode, which can create compliance risk if used on sites where scraping is not authorized. <br>
Mitigation: Use the skill only on sites where access and scraping are authorized and comply with applicable terms, laws, and internal policies. <br>
Risk: Fetched page text is untrusted input and may contain misleading instructions, prompt-injection content, or inaccurate information. <br>
Mitigation: Treat fetched content as untrusted before asking an agent to summarize it, execute follow-up actions, or rely on extracted claims. <br>
Risk: Optional stealth fetching depends on browser automation and anti-bot behavior that may be unsuitable for some production environments. <br>
Mitigation: Prefer basic mode where possible, install and review dependencies before use, and restrict stealth mode to approved workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shuxiangfanclaw/scrapling-fetch-basic) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown text by default, with optional JSON output containing URL, title, content, selector, length, truncation status, and mode.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Content is truncated to the requested maximum character count; default maximum is 30000 characters.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
