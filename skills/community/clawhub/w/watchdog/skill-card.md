## Description: <br>
Monitors websites, APIs, and cron jobs through Watch.dog, with tools to create, inspect, pause, resume, and delete monitors and watchdogs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joseshiru](https://clawhub.ai/user/joseshiru) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and site reliability teams use this skill to connect an agent to a Watch.dog account, review uptime or heartbeat status, and manage monitors, watchdogs, and public status pages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can store a Watch.dog API key locally and use it to access the user's monitoring account. <br>
Mitigation: Use a revocable or scoped API key when available, protect the generated .env file, and install the skill only when account management is intended. <br>
Risk: Authorized actions can create, pause, resume, delete, or publish monitoring resources. <br>
Mitigation: Carefully confirm delete, pause, resume, create, and public status-page update requests before tool execution. <br>
Risk: An incorrect WATCHDOG_API_URL could send credentials or account requests to the wrong endpoint. <br>
Mitigation: Verify WATCHDOG_API_URL before entering credentials or testing the connection. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/joseshiru/watchdog) <br>
- [Watch.dog](https://watch.dog) <br>
- [Watch.dog MCP endpoint](https://api.watch.dog/api/mcp_server.php) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, configuration, guidance] <br>
**Output Format:** [Markdown-oriented text responses with tool-returned status data, URLs, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Watch.dog API key and API URL; destructive and account-changing actions should be confirmed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence, SKILL.md frontmatter, and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
