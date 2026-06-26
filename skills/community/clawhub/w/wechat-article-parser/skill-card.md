## Description: <br>
解析微信公众号文章，提取标题、作者、正文内容、图片等信息。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harven-droid](https://clawhub.ai/user/harven-droid) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to parse WeChat public-account article links, extract article metadata and body text, and optionally save results to JSON, text files, or a configured Feishu Bitable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Feishu save helper can create or modify Bitable fields and delete rows it considers empty. <br>
Mitigation: Review the helper before use, connect it to a dedicated backed-up or disposable table, and disable empty-row cleanup unless row deletion is intended. <br>
Risk: The Feishu integration uses app credentials and table identifiers from environment variables. <br>
Mitigation: Use a dedicated Feishu app with the minimum required Bitable permissions and rotate credentials if they are exposed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/harven-droid/wechat-article-parser) <br>
- [Publisher Profile](https://clawhub.ai/user/harven-droid) <br>
- [Feishu Open Platform](https://open.feishu.cn) <br>
- [Feishu Bitable Record Create API](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/bitable-v1/app-table-record/create) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Console text, JSON files, Markdown guidance, and Feishu Bitable records when configured] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can include article title, author, publish time, body text, word count, image URLs, source URL, and parse timestamp.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
