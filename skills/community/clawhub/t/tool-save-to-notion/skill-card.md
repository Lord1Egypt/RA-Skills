## Description: <br>
Save tool links to Notion Toolbox by extracting tool name, type, tags, description, and optional cover image from a user-provided URL and saving them as a structured Notion database entry. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[redisread](https://clawhub.ai/user/redisread) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to save GitHub repositories, product pages, AI tools, browser extensions, online services, and software package links into a Notion Toolbox database with consistent metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends user-provided URLs and extracted metadata to a Notion database. <br>
Mitigation: Use a Notion integration token scoped only to the intended database and confirm the database ID before use. <br>
Risk: Private, internal, localhost, credential-bearing, or confidential URLs could expose sensitive information when fetched or stored. <br>
Mitigation: Use the skill only for public or intentionally shared tool links, and avoid confidential URLs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/redisread/tool-save-to-notion) <br>
- [Notion integrations](https://www.notion.so/my-integrations) <br>
- [Notion Pages API endpoint](https://api.notion.com/v1/pages) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown guidance with inline bash commands and JSON API payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured NOTION_API_KEY and access to the target Notion database.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
