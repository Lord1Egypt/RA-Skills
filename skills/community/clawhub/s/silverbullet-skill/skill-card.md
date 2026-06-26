## Description: <br>
MCP server for SilverBullet note-taking app - read, write, search, and manage markdown pages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ramonitor](https://clawhub.ai/user/ramonitor) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and external users connect an MCP-compatible agent to a configured SilverBullet note space so the agent can list, read, write, search, append, delete, and inspect markdown pages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read notes from the configured SilverBullet space. <br>
Mitigation: Install it only for agents that should have access to that space, and keep SILVERBULLET_URL pointed at the intended server. <br>
Risk: Write, append, and delete tools can change or remove real notes. <br>
Mitigation: Require user confirmation before invoking write_page, append_to_page, or delete_page. <br>
Risk: An unintended base_url override could direct requests to the wrong SilverBullet server. <br>
Mitigation: Do not allow untrusted content to choose base_url; prefer a fixed, reviewed SILVERBULLET_URL configuration. <br>


## Reference(s): <br>
- [SilverBullet documentation](https://silverbullet.md) <br>
- [SilverBullet HTTP API](https://silverbullet.md/HTTP%20API) <br>
- [ClawHub skill page](https://clawhub.ai/ramonitor/silverbullet-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Text, Markdown page content, JSON tool responses, and Markdown with inline shell or configuration blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Tool behavior depends on the configured SilverBullet server URL and the selected MCP transport.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, pyproject.toml, and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
