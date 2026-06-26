## Description: <br>
Parses WeChat public-account articles, extracts title, author, publication time, body text, and image links, and can optionally save extracted article data to files or a Feishu Bitable. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[reknottycat](https://clawhub.ai/user/reknottycat) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to extract readable content and metadata from WeChat article URLs for review, summarization, archival, or optional Feishu Bitable collection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional Feishu saver can automatically change the target table schema. <br>
Mitigation: Review the saver script before use and run it against a dedicated low-privilege Feishu app and test table first. <br>
Risk: The optional Feishu saver can delete blank rows from the configured table. <br>
Mitigation: Back up important table data and disable or manually approve blank-row deletion before using it on production tables. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/reknottycat/wechat-article-parser-local) <br>
- [Feishu Open Platform](https://open.feishu.cn) <br>
- [Feishu Bitable create record API](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/bitable-v1/app-table-record/create) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, files, API calls, shell commands, configuration] <br>
**Output Format:** [Console text and optional JSON files; Feishu saver writes records through the Feishu Bitable API.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Article output may include title, author, publish time, extracted body text, word count, image count, image URLs, source URL, and parse timestamp.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
