## Description: <br>
抖音/B站视频收藏入库：接收视频链接，自动抓取信息、生成总结、分类，并写入飞书多维表格。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[keson1521](https://clawhub.ai/user/keson1521) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, creators, and knowledge workers use this skill to collect Douyin or Bilibili video links, summarize and categorize the content, and store structured records in Feishu Bitable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill grants broader local command authority than the video-to-Feishu workflow requires. <br>
Mitigation: Review before installing, use trusted sources for dokobot and lark-cli, and remove unused permissions such as node and rm when the agent supports narrowing allowed tools. <br>
Risk: The workflow writes persistent records to Feishu without a clearly defined review step. <br>
Mitigation: Use a dedicated or least-privilege Feishu Base and verify table sharing settings before storing private or access-controlled video links. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/keson1521/video-collector) <br>
- [Publisher profile](https://clawhub.ai/user/keson1521) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON record structure] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a Feishu Bitable record proposal and confirmation text after writing the video entry.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
