## Description: <br>
OpenClaw Web Chat Pro provides a Node.js web chat interface for AI conversations with model switching, streaming responses, persisted sessions, and conversation export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qqkzlm](https://clawhub.ai/user/qqkzlm) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and teams use this skill to deploy a web-based AI chat application with configurable models, streaming responses, history, export, and subscription-oriented feature tiers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Packaged password protection does not fully protect chat history, exports, websocket access, or AI usage. <br>
Mitigation: Add real server-side authentication and authorization to all API routes and websocket events before exposing the service beyond a trusted local environment. <br>
Risk: The packaged configuration includes a default password and permissive CORS behavior. <br>
Mitigation: Change the default password, restrict allowed origins, and avoid public hosting until access controls have been reviewed. <br>
Risk: Rendered Markdown and conversation export paths can expose user-provided chat content. <br>
Mitigation: Sanitize rendered Markdown and protect history and export endpoints with authenticated, session-scoped access checks. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/qqkzlm/webchat-pro) <br>
- [Publisher profile](https://clawhub.ai/user/qqkzlm) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>
- [Moltbook community](https://moltbook.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and configuration values; runtime chat responses are text or Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes web chat session data, model metadata, token and cost estimates, and JSON or Markdown conversation exports.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, skill.json, package.json, README.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
