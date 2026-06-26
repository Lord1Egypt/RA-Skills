## Description: <br>
Install, configure, and operate the TokenRanger OpenClaw plugin for local Ollama context compression and TokenRanger sidecar troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[synchronic1](https://clawhub.ai/user/synchronic1) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw operators use TokenRanger to install, configure, upgrade, uninstall, and troubleshoot a local context-compression plugin that reduces cloud LLM input tokens through Ollama-backed summarization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A local background service may process conversation history for compression. <br>
Mitigation: Install only in trusted local environments and avoid sensitive or regulated chats unless the environment is approved. <br>
Risk: The setup flow registers a persistent sidecar service. <br>
Mitigation: Verify the service state after setup and remove the documented systemd or launchd service files when uninstalling. <br>
Risk: When Ollama or the sidecar is unavailable, TokenRanger can fall through to uncompressed cloud LLM calls. <br>
Mitigation: Check TokenRanger status and sidecar logs before relying on compression or local processing behavior. <br>


## Reference(s): <br>
- [TokenRanger ClawHub listing](https://clawhub.ai/synchronic1/tokenranger) <br>
- [TokenRanger plugin repository](https://github.com/peterjohannmedina/openclaw-plugin-tokenranger) <br>
- [openclaw-plugin-tokenranger npm package](https://www.npmjs.com/package/openclaw-plugin-tokenranger) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local service status checks, OpenClaw plugin commands, Ollama setup guidance, and uninstall cleanup steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: artifact frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
