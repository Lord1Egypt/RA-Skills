## Description: <br>
Scrapling Fetch Pro fetches article content from webpages, converts it to Markdown or JSON, and supports automatic basic or stealth fetching with WeChat article cleanup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shuxiangfanclaw](https://clawhub.ai/user/shuxiangfanclaw) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and external users use this skill to fetch web articles, blogs, news pages, announcements, and WeChat public-account articles for downstream AI summarization, analysis, or archiving. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary flags that the skill openly promotes stealth anti-bot bypass without clear authorization or data-handling boundaries. <br>
Mitigation: Use it only on sites the user owns or is authorized to access, avoid using stealth mode to defeat site protections, and respect site terms and applicable law. <br>
Risk: Fetched pages are untrusted data that may contain misleading, adversarial, or sensitive content before being passed to another AI agent. <br>
Mitigation: Treat fetched content as untrusted, minimize retained scraped data, and review or sanitize content before downstream use. <br>


## Reference(s): <br>
- [Usage Guide](references/usage.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/shuxiangfanclaw/scrapling-fetch-pro) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown text by default, or structured JSON when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Output may include fetched URL, title, extracted content, selector, source length, truncation status, fetch mode, and WeChat detection status.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
