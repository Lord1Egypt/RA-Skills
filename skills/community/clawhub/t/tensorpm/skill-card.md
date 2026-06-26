## Description: <br>
AI-powered project management - a Notion and Jira alternative with local-first architecture. Manage projects, track action items, and coordinate teams via MCP tools or A2A agent communication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Neo552](https://clawhub.ai/user/Neo552) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, agents, and project teams use this skill to connect an AI assistant to the TensorPM desktop app for project creation, action item tracking, workspace switching, and project-agent conversations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: TensorPM's local API can read and change project data without authentication while the app is running. <br>
Mitigation: Run TensorPM only on trusted machines, enable A2A_HTTP_AUTH_TOKEN before starting TensorPM when using A2A, and avoid placing sensitive secrets in projects, imported files, or conversations. <br>
Risk: The skill depends on the TensorPM desktop app and its download channels. <br>
Mitigation: Install only when you trust the TensorPM app and its published download sources. <br>


## Reference(s): <br>
- [TensorPM homepage](https://tensorpm.com) <br>
- [ClawHub skill listing](https://clawhub.ai/Neo552/tensorpm) <br>
- [TensorPM release notes](https://github.com/Neo552/TensorPM-Releases/releases/latest) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text, JSON] <br>
**Output Format:** [Markdown guidance with shell commands, configuration steps, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the TensorPM desktop app for MCP tools and A2A communication.] <br>

## Skill Version(s): <br>
1.1.12 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
