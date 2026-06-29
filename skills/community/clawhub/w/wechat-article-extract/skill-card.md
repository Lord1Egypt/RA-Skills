## Description: <br>
Extract public WeChat Official Account articles from mp.weixin.qq.com links or saved HTML into clean Markdown or structured JSON, including title, account name, publish time, article text, tables, image markers, and image URLs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joannaxing](https://clawhub.ai/user/joannaxing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to extract public WeChat Official Account articles into portable Markdown or structured JSON for reading, archiving, summarization, or downstream import workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches public WeChat pages and can write extracted output or downloaded images to local paths. <br>
Mitigation: Review the source URL and output destination before running, and use image downloading only for trusted articles and directories. <br>
Risk: Extracted article content may be subject to third-party copyright or reuse restrictions. <br>
Mitigation: Summarize or transform content when sharing externally, and do not republish full articles unless the user has the rights to do so. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/joannaxing/wechat-article-extract) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, files] <br>
**Output Format:** [Markdown or JSON article extraction output, with optional downloaded image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Markdown includes article metadata, text, table conversions, image markers, and image URLs; JSON includes structured article metadata, content fields, image entries, image URLs, and optional downloaded image paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
