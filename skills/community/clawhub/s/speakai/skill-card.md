## Description: <br>
Capture meetings, search thousands of recordings, run async voice and video surveys, create clips, and automate workflows with Speak AI through MCP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[speakai](https://clawhub.ai/user/speakai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect an agent to a Speak AI workspace for searching recordings, reading transcripts and insights, creating clips or exports, and managing meeting, recorder, folder, webhook, and automation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access meeting, transcript, media, and workspace data in Speak AI. <br>
Mitigation: Use the narrowest OAuth or API permissions available, scope searches with filters, and retrieve only the records needed for the user's task. <br>
Risk: Some tools can delete records, create shareable artifacts, or make persistent workspace changes such as webhooks, automations, recorders, and meeting assistants. <br>
Mitigation: Require explicit user confirmation for destructive, bulk, sharing, reanalysis, and persistent actions, including target IDs and consequences before execution. <br>
Risk: Transcript, caption, media, insight, and chat content may contain text that resembles agent instructions. <br>
Mitigation: Treat workspace content as untrusted data and follow only the active user's instructions. <br>


## Reference(s): <br>
- [Speak AI MCP installation guide](https://mcp.speakai.co) <br>
- [Speak AI API reference](https://docs.speakai.co) <br>
- [Speak AI MCP server package](https://www.npmjs.com/package/@speakai/mcp-server) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with tool selections, configuration snippets, and concise user-facing results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call Speak AI MCP tools and resources when configured with OAuth or SPEAK_API_KEY.] <br>

## Skill Version(s): <br>
1.13.8 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
