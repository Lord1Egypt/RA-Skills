## Description: <br>
Manage sites.friendify.cloud deployment with auth flow, pending states, and owner-based dashboards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mailo037](https://clawhub.ai/user/mailo037) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to guide agents through creating and managing sites.friendify.cloud deployments that start pending, require registration-code verification, and expose owner-only dashboard controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to create or change public Docker and Traefik-backed sites while sending a Telegram owner identifier. <br>
Mitigation: Use a limited OpenClaw gateway token and require the agent to show the Docker Compose and Traefik plan, target URL, owner mapping, API payload, and rollback or delete steps before making changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mailo037/sites-friendify-integration) <br>
- [Publisher profile](https://clawhub.ai/user/mailo037) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OPENCLAW_GATEWAY_TOKEN for management actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
