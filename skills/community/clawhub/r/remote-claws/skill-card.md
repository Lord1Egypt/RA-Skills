## Description: <br>
Full remote desktop control of a machine via Remote Claws MCP. Use when asked to: take a screenshot of the remote desktop; click, type, or drag with the mouse/keyboard on the remote machine; run commands or scripts; automate a Chromium browser on the remote machine; read or write files on the remote machine. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wentbackward](https://clawhub.ai/user/wentbackward) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agents use this skill to control a remote desktop through a Remote Claws MCP server for screenshots, UI interaction, browser automation, command execution, and file transfer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables broad remote control of another machine, including command execution, file operations, browser automation, and desktop interaction. <br>
Mitigation: Install it only for intentional remote-control use, run the MCP server under a low-privilege account, and require explicit confirmation for command execution, file deletion, file move, file write, and logged-in browser actions. <br>
Risk: Bearer token exposure or overly broad network access could allow unauthorized remote actions. <br>
Mitigation: Verify the remote-claws MCP server before enabling it, restrict the bearer token by IP address and host, and use per-tool permissions to expose only required tools. <br>
Risk: Persistent browser sessions can expose authenticated websites to unintended automation. <br>
Mitigation: Use separate browser profiles or temporary sessions for sensitive work and require confirmation before actions in logged-in browser sessions. <br>


## Reference(s): <br>
- [Remote Claws homepage](https://github.com/wentbackward/remote-claws) <br>
- [Remote Claws setup guide](https://github.com/wentbackward/remote-claws/blob/master/remote-claws-openclaw-setup-guide.md) <br>
- [Remote Claws security documentation](https://github.com/wentbackward/remote-claws#security) <br>
- [ClawHub skill page](https://clawhub.ai/wentbackward/remote-claws) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration, files] <br>
**Output Format:** [Markdown guidance with tool names, configuration references, and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Remote desktop screenshots are JPEG with a maximum size of 1280x960, file content is base64 encoded, desktop text input is ASCII-only, and browser sessions may persist cookies and local storage.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
