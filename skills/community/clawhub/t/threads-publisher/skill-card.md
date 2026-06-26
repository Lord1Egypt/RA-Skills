## Description: <br>
Publish posts and threads to Threads (by Meta), including text posts, photo or video posts, carousels, multi-post threads, and replies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snoopyrain](https://clawhub.ai/user/snoopyrain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to publish, schedule, and reply to Threads content through Boring after connecting a Threads account. It guides the agent in choosing the right Boring MCP tool, splitting long content into threads, preparing media, and reporting publish results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Boring MCP Connector URL grants persistent third-party publishing authority for connected Threads accounts. <br>
Mitigation: Treat the connector URL like a password, connect only intended accounts, confirm exact content and schedules before publishing, and revoke or regenerate the token if it is exposed or no longer needed. <br>
Risk: The security review notes inconsistent data-flow disclosure for a workflow that sends publishing and analytics requests through Boring. <br>
Mitigation: Review Boring's data handling before use and avoid submitting content, media, or account access unless that service is trusted for the intended account. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/snoopyrain/threads-publisher) <br>
- [Boring MCP setup documentation](https://boring-doc.aiagent-me.com/getting-started/mcp.html) <br>
- [Boring API documentation](https://boring-doc.aiagent-me.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Text, Configuration] <br>
**Output Format:** [Markdown guidance with MCP tool call examples and publishing status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Boring MCP Connector URL that contains an embedded authentication token.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
