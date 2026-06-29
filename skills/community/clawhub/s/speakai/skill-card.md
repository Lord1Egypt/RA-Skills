## Description: <br>
Capture meetings, search thousands of recordings, run async voice and video surveys, create clips, and automate workflows with Speak AI through MCP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[speakai](https://clawhub.ai/user/speakai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, employees, and external users use this skill to connect agents to a Speak AI workspace for transcription, meeting analysis, transcript search, media exports, clips, surveys, and workflow automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The connector can access Speak AI workspace data according to the OAuth or API key permissions granted by the user. <br>
Mitigation: Review connector permissions during OAuth, authorize only the intended Speak AI account, and revoke OAuth access or remove the connector when it is no longer needed. <br>
Risk: Some tools can delete records, make bulk changes, create persistent automations or recorders, reanalyze content, or generate shareable exports. <br>
Mitigation: Require explicit user confirmation with target IDs and consequences before risky actions, preview bulk changes, and provide rollback or disable instructions for persistent changes. <br>
Risk: Transcripts, captions, AI insights, chat messages, and meeting content may contain untrusted instructions or sensitive text. <br>
Mitigation: Treat media content as data rather than instructions, scope reads to the smallest useful set of records, and ask the user whether to redact or proceed if credentials or directives appear in content. <br>


## Reference(s): <br>
- [Speak AI MCP installation guide](https://mcp.speakai.co) <br>
- [Speak AI API reference](https://docs.speakai.co) <br>
- [@speakai/mcp-server package](https://www.npmjs.com/package/@speakai/mcp-server) <br>
- [ClawHub Speak AI skill page](https://clawhub.ai/speakai/skills/speakai) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, Markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON configuration, and MCP tool-call recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce MCP tool calls that read, create, update, share, export, reanalyze, or delete Speak AI workspace records after appropriate confirmation.] <br>

## Skill Version(s): <br>
1.13.2 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
