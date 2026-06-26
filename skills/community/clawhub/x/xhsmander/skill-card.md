## Description: <br>
xhsmander helps an agent use a Docker-hosted xiaohongshu-mcp service to log in to Xiaohongshu, publish image-and-text posts, search content, and perform account interactions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[279458179](https://clawhub.ai/user/279458179) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to automate Xiaohongshu publishing workflows through local helper scripts and a Docker-hosted MCP endpoint. It is suited for preparing login QR codes, checking session status, publishing posts, searching feeds, and performing explicitly approved interactions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Docker service can retain session cookies and act on a live Xiaohongshu account after login. <br>
Mitigation: Install only when the Docker image is trusted, run it on a trusted machine, stop the container after use, and delete stored cookies in ./data when the session is no longer needed. <br>
Risk: Publishing, liking, favoriting, or commenting can affect a real social account with limited built-in scoping. <br>
Mitigation: Require the agent to show the exact post or interaction and get explicit approval before any account-changing action. <br>
Risk: The local MCP service is exposed on port 18060. <br>
Mitigation: Keep port 18060 local and protected, and do not expose it to untrusted networks. <br>


## Reference(s): <br>
- [xhsmander ClawHub listing](https://clawhub.ai/279458179/xhsmander) <br>
- [xiaohongshu-mcp API reference](references/mcp_api.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code, API Calls, Files] <br>
**Output Format:** [Markdown guidance with shell commands, Python script usage, JSON-RPC payloads, and generated local files such as QR code and result JSON files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local Docker service on port 18060 and uses container paths for image publishing.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
