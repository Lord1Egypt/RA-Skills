## Description: <br>
Monitors websites, APIs, and cron jobs using Watch.dog so an agent can check uptime, create monitors, manage watchdogs, and configure public status pages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Robinson0594](https://clawhub.ai/user/Robinson0594) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, site reliability engineers, and service operators use this skill to monitor websites, APIs, servers, and scheduled jobs through Watch.dog. It supports checking status, creating active monitors and passive watchdogs, managing monitor state, and configuring public tracker pages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores a Watch.dog API key locally and sends requests to Watch.dog using that key. <br>
Mitigation: Use a restricted API key when available, protect the local .env file, and rotate the key if it may have been exposed. <br>
Risk: The skill can modify account resources, including pausing, resuming, creating, or deleting monitors and watchdogs. <br>
Mitigation: Review requested resource names, IDs, and URLs before execution, and require explicit confirmation before destructive actions. <br>
Risk: The provided security summary flags weak user-consent boundaries around credential testing and destructive account actions. <br>
Mitigation: Install only after review, expect the skill to contact Watch.dog after credentials are configured, and manually confirm any account-changing operation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Robinson0594/seeweb-uptime) <br>
- [Watch.dog](https://watch.dog) <br>
- [Watch.dog MCP API endpoint](https://api.watch.dog/api/mcp_server.php) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, configuration guidance] <br>
**Output Format:** [Markdown and text responses from MCP tool calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include status tables, uptime summaries, monitor IDs, tracker page URLs, and watchdog endpoint URLs.] <br>

## Skill Version(s): <br>
1.0.5 (source: SKILL.md frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
