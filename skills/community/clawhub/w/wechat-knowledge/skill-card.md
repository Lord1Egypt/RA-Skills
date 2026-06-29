## Description: <br>
一键知识库 - 微信内容管家 helps agents save supported WeChat, Douyin, Xiaohongshu, public-account, and local-file content into Tencent Docs knowledge spaces with an index entry. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hitjcl](https://clawhub.ai/user/hitjcl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users ask an agent to capture links or local files and add them to a Tencent Docs-backed knowledge base. The skill guides the agent through source recognition, local download or parsing, upload to Tencent Docs, and index-record creation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad save-style triggers can cause selected links or files to be downloaded locally and uploaded to Tencent or WeChat knowledge-base services unintentionally. <br>
Mitigation: Confirm the exact source items and destination before each upload, avoid ambiguous requests such as "save this," and review Tencent Docs authorization before use. <br>
Risk: Temporary local copies created during download or parsing can leave sensitive material on the local machine. <br>
Mitigation: Clean up temporary files after each run and avoid processing content that should not be transferred to the configured knowledge base. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hitjcl/wechat-knowledge) <br>
- [Tencent Docs](https://docs.qq.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and script invocation patterns] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May download selected content locally and upload it to Tencent Docs after user authorization.] <br>

## Skill Version(s): <br>
2.2.5 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
