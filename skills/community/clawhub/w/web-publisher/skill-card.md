## Description: <br>
Accepts article URLs or local documents, extracts content, optionally rewrites it, and publishes or saves drafts to WeChat Official Accounts while also supporting document-to-Markdown conversion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sipingme](https://clawhub.ai/user/sipingme) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content operators use this skill to turn web articles and local files into WeChat drafts or publications, with optional AI rewriting and Markdown-only conversion when publication is not desired. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A reusable publishing API key may be exposed in chat or logs on a persist-failed login-status path. <br>
Mitigation: If this condition occurs, treat the key as exposed and rotate or revoke it before continuing. <br>
Risk: Documents, URLs, and rewritten content are sent to tools.siping.me and may also flow through rewrite providers. <br>
Mitigation: Use the skill only with content approved for that data flow, and avoid confidential or regulated material unless that transfer has been reviewed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sipingme/web-publisher) <br>
- [Publisher Profile](https://clawhub.ai/user/sipingme) <br>
- [tools.siping.me](https://tools.siping.me) <br>
- [Microsoft MarkItDown](https://github.com/microsoft/markitdown) <br>
- [news-to-markdown companion skill](https://github.com/sipingme/news-to-markdown-skill) <br>
- [browser-web-search companion skill](https://github.com/sipingme/browser-web-search-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Markdown, API calls, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce WeChat draft media IDs, publish IDs, login or configuration URLs, Markdown conversion output, and status summaries.] <br>

## Skill Version(s): <br>
0.9.18 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
