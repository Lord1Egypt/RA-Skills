## Description:

xhsmander helps agents automate Xiaohongshu login, image-text post publishing, search, and account interactions through a Docker-hosted xiaohongshu-mcp service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[279458179](https://clawhub.ai/user/279458179)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to run a Docker-backed Xiaohongshu automation workflow for QR login, publishing image-text notes, searching feeds, and performing account interactions from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live account-control tools can publish, comment, like, and favorite from a real Xiaohongshu account.

Mitigation: Require explicit user confirmation before account-changing actions and restrict use to the intended account.

Risk: The Docker service uses an unpinned xiaohongshu-mcp image and exposes the MCP service on port 18060.

Mitigation: Pin and audit the Docker image before installation and bind the MCP port to 127.0.0.1.

Risk: Cookies, QR codes, and JSON result files may persist in local data and script output paths.

Mitigation: Protect the ./data directory and delete cookies, QR images, and generated result files when they are no longer needed.

## Reference(s):

- [xiaohongshu-mcp API Reference](artifact/references/mcp_api.md)
- [ClawHub skill page](https://clawhub.ai/279458179/skills/xhsmander)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, Python code, JSON API payloads, and generated local files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate QR code images and JSON result files; account-changing actions can publish posts or interact with live Xiaohongshu content.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
