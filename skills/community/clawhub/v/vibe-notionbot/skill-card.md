## Description: <br>
Interact with Notion workspaces using official API - manage pages, databases, blocks, users, and comments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[devxoul](https://clawhub.ai/user/devxoul) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and AI agents use this skill to inspect and manage Notion pages, databases, blocks, users, comments, and searches through the vibe-notionbot CLI and the official Notion API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A Notion integration token can grant broad workspace access if it is over-permissioned. <br>
Mitigation: Use a least-privilege Notion integration token and share only the specific pages or databases the agent needs. <br>
Risk: Archive/delete actions, content replacement, database schema changes, comments, file uploads, and batch operations can alter workspace content. <br>
Mitigation: Require confirmation before these operations and review batch JSON files before execution. <br>
Risk: The skill discusses a higher-privilege user-session CLI as an alternative to vibe-notionbot. <br>
Mitigation: Prefer vibe-notionbot with a Notion integration token unless the user explicitly authorizes acting through a logged-in desktop session. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/devxoul/vibe-notionbot) <br>
- [vibe-notion npm package](https://www.npmjs.com/package/vibe-notion) <br>
- [Notion integrations](https://www.notion.so/my-integrations) <br>
- [Feature requests](https://github.com/devxoul/vibe-notion/issues) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; CLI commands return JSON by default.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the vibe-notionbot binary and a NOTION_TOKEN integration token; batch operations can read JSON operation files.] <br>

## Skill Version(s): <br>
1.5.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
