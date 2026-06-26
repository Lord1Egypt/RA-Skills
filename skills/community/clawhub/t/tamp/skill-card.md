## Description: <br>
Set up Tamp token compression proxy for OpenClaw to reduce Anthropic API input token costs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sliday](https://clawhub.ai/user/sliday) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to install and configure the Tamp local proxy for OpenClaw so Anthropic requests can be compressed before reaching the upstream API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Anthropic prompts, tool outputs, and API headers pass through a local compression proxy. <br>
Mitigation: Install only after reviewing or trusting the Tamp npm package, and use a direct Anthropic provider as a fallback when appropriate. <br>
Risk: Exposing port 7778 beyond localhost could make model traffic reachable by other hosts. <br>
Mitigation: Keep Tamp bound to localhost and do not publish or proxy port 7778 externally. <br>
Risk: Persistent service mode or logging can create ongoing local behavior or retain operational details. <br>
Mitigation: Enable the systemd service or TAMP_LOG only when that persistence or logging is intended. <br>


## Reference(s): <br>
- [Tamp ClawHub Page](https://clawhub.ai/sliday/tamp) <br>
- [Tamp Source](https://github.com/sliday/tamp) <br>
- [Tamp Documentation](https://tamp.dev) <br>
- [Tamp White Paper](https://tamp.dev/whitepaper.pdf) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash, systemd, and JSON5 configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
