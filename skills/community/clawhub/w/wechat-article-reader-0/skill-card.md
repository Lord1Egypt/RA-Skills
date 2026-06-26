## Description: <br>
Reads WeChat public account article links, extracts article metadata, and returns a concise summary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shianaixuexi-cell](https://clawhub.ai/user/shianaixuexi-cell) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to process supported WeChat public account article URLs, extract title, author, account, publication date, and summarize the article content for messaging or agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound network requests to article URLs provided by the user. <br>
Mitigation: Use it only with public WeChat article links and avoid private, access-controlled, or sensitive URLs. <br>
Risk: The release relies on externally maintained Python dependencies with version ranges rather than pinned reviewed versions. <br>
Mitigation: Review and pin dependencies in the deployment environment before production use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/shianaixuexi-cell/wechat-article-reader-0) <br>
- [Artifact README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON] <br>
**Output Format:** [Plain text message with structured JSON status and article data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include extracted title, author, account, publication time, URL, content, and generated summary when parsing succeeds.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md frontmatter, and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
