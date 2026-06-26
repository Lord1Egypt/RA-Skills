## Description: <br>
Publish AI-powered web pages with end-to-end encryption on yourbro.ai. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mehanig](https://clawhub.ai/user/mehanig) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to create, configure, and publish encrypted web page directories through a local yourbro-agent and the yourbro.ai relay. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on a local yourbro-agent binary and a YOURBRO_TOKEN credential. <br>
Mitigation: Install only when you trust yourbro.ai and keep the token scoped and protected in the agent environment. <br>
Risk: Page visibility settings can make content public or share it with specific accounts. <br>
Mitigation: Review page.json before sharing links and avoid setting sensitive pages to public. <br>
Risk: Deletion commands under /data/yourbro/pages/ can permanently remove local page content. <br>
Mitigation: Confirm the target slug and keep backups before running delete commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mehanig/yourbro) <br>
- [yourbro.ai homepage](https://yourbro.ai) <br>
- [yourbro-agent macOS Apple Silicon download](https://yourbro.ai/releases/latest/yourbro-agent-darwin-arm64) <br>
- [yourbro-agent macOS Intel download](https://yourbro.ai/releases/latest/yourbro-agent-darwin-amd64) <br>
- [yourbro-agent Linux x86_64 download](https://yourbro.ai/releases/latest/yourbro-agent-linux-amd64) <br>
- [yourbro-agent Linux ARM64 download](https://yourbro.ai/releases/latest/yourbro-agent-linux-arm64) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON configuration, and HTML/CSS/JavaScript file content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local page files under /data/yourbro/pages/ and page metadata such as page.json.] <br>

## Skill Version(s): <br>
0.0.11 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
