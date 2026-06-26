## Description: <br>
Install and configure the OpenClaw Vertex AI Memory Bank plugin for persistent, cross-agent memory across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Shubhamsaboo](https://clawhub.ai/user/Shubhamsaboo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to set up Google Vertex AI-backed long-term memory, configure openclaw.json, and manage memory search, capture, sync, and deletion commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent automatic cloud memory may store sensitive conversations or workspace files. <br>
Mitigation: Use a dedicated least-privilege GCP project, disable autoCapture or autoSyncFiles for sensitive work, or set a TTL before use. <br>
Risk: The setup script installs unpinned remote code from a GitHub repository. <br>
Mitigation: Review and pin the source before running the setup script in a production or sensitive environment. <br>
Risk: The setup flow can create Google Cloud resources that may incur costs. <br>
Mitigation: Use an intended GCP project, review billing controls, and confirm the region and project ID before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Shubhamsaboo/vertexai-memory-bank) <br>
- [Source repository from skill metadata](https://github.com/Shubhamsaboo/openclaw-vertexai-memorybank) <br>
- [Google Cloud SDK installation](https://cloud.google.com/sdk/docs/install) <br>
- [Node.js](https://nodejs.org/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash, curl, and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose commands that create Google Cloud resources, install npm packages, and modify OpenClaw configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
