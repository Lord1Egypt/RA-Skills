## Description: <br>
Searches and reads WeChat public-account articles by keyword or mp.weixin.qq.com URL, returning article metadata and extracted text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[onlyloveher](https://clawhub.ai/user/onlyloveher) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to find public WeChat articles, extract article text and metadata, and summarize or analyze content from supplied WeChat article links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms or supplied WeChat article URLs may be sent to external search or fetch services. <br>
Mitigation: Use the skill only for intended public WeChat article lookups and avoid submitting sensitive queries or private URLs. <br>
Risk: Broad activation wording may invoke the skill for ambiguous WeChat-related requests. <br>
Mitigation: Narrow triggers or review invocation context before deployment when unintended external requests are a concern. <br>
Risk: High-frequency article fetching may trigger anti-bot controls or unreliable reads. <br>
Mitigation: Avoid high request volume and prefer explicit user confirmation before repeated searches or fetches. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/onlyloveher/wechat-tool-v2) <br>
- [Publisher profile](https://clawhub.ai/user/onlyloveher) <br>
- [Repository link declared by artifact](https://github.com/johan-oilman/wechat-articles) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Text or Markdown summaries, with optional command-line output and Python dictionary structures for article metadata and paragraphs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results may include title, URL, source, date, and snippet; article reads may include title, author, paragraphs, and read mode.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
