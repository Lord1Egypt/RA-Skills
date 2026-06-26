## Description: <br>
Save WeChat public account articles to a Notion database, including title, cover image, body content, keywords, a review comment, and a star rating. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Gevtolev](https://clawhub.ai/user/Gevtolev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and knowledge workers use this skill to archive WeChat public account articles into a Notion database while preserving article structure and adding searchable review metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes real changes to Notion using a Notion API key. <br>
Mitigation: Use a dedicated Notion integration shared only with the intended database or parent page, and confirm the destination database before running the save step. <br>
Risk: The Notion API key can be exposed if pasted into chat or stored carelessly. <br>
Mitigation: Keep NOTION_API_KEY out of chat and shell history where possible, and provide it through the agent or OpenClaw configuration mechanism. <br>
Risk: Fetched article text plus generated tags, ratings, and comments are persisted in Notion. <br>
Mitigation: Review the source article and generated metadata before saving sensitive or regulated content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Gevtolev/wechat-to-notion) <br>
- [Notion integrations](https://notion.so/my-integrations) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON intermediate article data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires NOTION_API_KEY plus python3 and curl; fetches only mp.weixin.qq.com article URLs and writes content blocks to Notion.] <br>

## Skill Version(s): <br>
1.2.5 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
