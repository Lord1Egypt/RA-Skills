## Description: <br>
Schedule meetings, check availability, and manage calendars across Google, Outlook, and CalDAV. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[billylui](https://clawhub.ai/user/billylui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an MCP-compatible agent resolve times, check calendar availability, and schedule meetings across Google Calendar, Outlook, and CalDAV providers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive OAuth calendar access for scheduling workflows. <br>
Mitigation: Install only when calendar access is acceptable, keep credentials protected at ~/.config/temporal-cortex/credentials.json, and confirm booking details before creating events. <br>
Risk: The npx installation path downloads a local MCP server package and platform binary. <br>
Mitigation: Verify the pinned npm package and release checksums before first use, or run the server in Docker when stronger supply-chain containment is needed. <br>
Risk: Platform Mode can contact Temporal Cortex services for cross-user scheduling. <br>
Mitigation: Keep Local Mode unless platform scheduling features are required. <br>


## Reference(s): <br>
- [Temporal Cortex Homepage](https://temporal-cortex.com) <br>
- [Temporal Cortex REST API Reference](https://temporal-cortex.com/docs/rest-api) <br>
- [Temporal Cortex Platform Docs](https://app.temporal-cortex.com) <br>
- [MCP Server Package](https://www.npmjs.com/package/@temporal-cortex/cortex-mcp) <br>
- [Security Model](references/SECURITY-MODEL.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with tables and inline code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Routes calendar tasks to datetime and scheduling MCP tools; calendar actions require OAuth credentials and user confirmation before booking or sending proposals.] <br>

## Skill Version(s): <br>
0.9.1 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
