## Description:

Secure email access via read-no-evil-mcp with prompt injection scanning for reading, sending, deleting, and moving emails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thekie](https://clawhub.ai/user/thekie)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and OpenClaw users use this skill to connect an agent to a read-no-evil-mcp server for mailbox listing, reading, sending, moving, and deletion with server-side prompt injection scanning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mailbox access can include send, delete, and move operations when those permissions are enabled.

Mitigation: Prefer read-only mailbox permissions and enable send, delete, or move only for accounts and folders that require those actions.

Risk: Docker and HTTP server setup can expose mailbox access too broadly if bound or routed incorrectly.

Mitigation: Use a trusted server, bind local deployments to localhost or firewall the port, and require HTTPS plus authentication for remote servers.

Risk: The .env file contains mailbox password material used by the server container.

Mitigation: Keep the .env file secret, avoid sharing it with the agent, and do not display full configuration contents during troubleshooting.

Risk: The setup script pulls a container image before passing it mailbox credentials.

Mitigation: Pin or independently verify the Docker image before providing credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thekie/skills/read-no-evil-mcp)
- [read-no-evil-mcp server](https://github.com/thekie/read-no-evil-mcp)
- [ProtectAI DeBERTa prompt injection model](https://huggingface.co/protectai/deberta-v3-base-prompt-injection-v2)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and plain-text CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands target a configured read-no-evil-mcp server; mailbox permissions are controlled by server configuration.]

## Skill Version(s):

0.3.1 (source: server release metadata and changelog, released 2026-02-17)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
