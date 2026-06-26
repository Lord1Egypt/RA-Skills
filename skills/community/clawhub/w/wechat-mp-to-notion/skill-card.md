## Description: <br>
Fetches public WeChat MP articles from mp.weixin.qq.com links and saves them into Notion as structured pages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[opoojkk](https://clawhub.ai/user/opoojkk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to archive public WeChat account articles into Notion, creating a structured page or database entry with article metadata, readable text blocks, and images where possible. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A Notion token with broad workspace access could allow more access than needed when saving articles. <br>
Mitigation: Use a dedicated Notion integration token limited to the target page or database. <br>
Risk: The skill writes content from a user-provided WeChat article into a user-specified Notion parent. <br>
Mitigation: Verify the article URL and Notion parent ID before running, and pass only articles intended for archival. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/opoojkk/wechat-mp-to-notion) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with bash command examples; the script returns JSON with article metadata and the created Notion page identifiers.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Notion integration token and a target page or database shared with that integration.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
