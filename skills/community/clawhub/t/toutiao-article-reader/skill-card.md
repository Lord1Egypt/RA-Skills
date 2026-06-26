## Description: <br>
Uses browser automation to open article links from Toutiao, WeChat public accounts, Zhihu, Xueqiu, and similar sites, extract article metadata and body text, clean the content, and produce summaries or exports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brainpower168](https://clawhub.ai/user/brainpower168) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Readers, researchers, and content-analysis agents use this skill to fetch public article URLs, extract title, author, date, source URL, and cleaned body text, then generate a short summary or export the result. It is intended for article reading and summarization workflows, not for handling confidential or restricted pages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill opens user-supplied article links in an automated browser. <br>
Mitigation: Confirm the target URL before use and run it only for pages the user intends the agent to access. <br>
Risk: Extracted article text can be cached locally in the skill folder and later shown or exported. <br>
Mitigation: Avoid private, confidential, paywalled, internal, or sensitive pages unless local caching is acceptable, and clear the cache after sensitive processing. <br>
Risk: Generated summaries and export files may contain copied article content. <br>
Mitigation: Review exported Markdown, TXT, JSON, or HTML files before sharing and handle them according to the sensitivity of the source article. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/brainpower168/toutiao-article-reader) <br>
- [Server-resolved publisher profile](https://clawhub.ai/user/brainpower168) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, html, shell commands, guidance] <br>
**Output Format:** [Console text or JSON, with optional Markdown, TXT, JSON, or HTML export files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include title, author, publish time, source URL, cleaned content, word count, reading time, summary, key points, and value assessment; caches extracted article data locally for 24 hours by default.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
