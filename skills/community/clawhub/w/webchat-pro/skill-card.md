## Description:

OpenClaw Web Chat Pro provides a browser-based AI chat application with model switching, streaming responses, conversation persistence, export, and dark mode.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qqkzlm](https://clawhub.ai/user/qqkzlm)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to run a local or self-hosted AI chat interface with selectable models, streamed responses, saved conversations, and exportable chat history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private chats and AI execution may be exposed if the web chat is deployed on a network with only the provided authentication controls.

Mitigation: Use only for local testing or place it behind strong network controls until real server-side authentication and session authorization are added.

Risk: Default or plaintext password handling can leave deployments accessible to unintended users.

Mitigation: Remove default passwords, require secure password setup, and store credentials with appropriate hashing before using sensitive chats.

Risk: Rendered Markdown and deployment hooks may create additional review obligations before production use.

Mitigation: Sanitize rendered Markdown and review or remove postinstall and systemd deployment steps before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/qqkzlm/skills/webchat-pro)
- [Publisher Profile](https://clawhub.ai/user/qqkzlm)
- [OpenClaw Documentation](https://docs.openclaw.ai)
- [Moltbook Community](https://moltbook.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Browser chat responses with Markdown rendering and JSON or Markdown conversation exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Streams responses and can persist per-session conversation history.]

## Skill Version(s):

1.0.0 (source: server release metadata, artifact skill.json, artifact package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
