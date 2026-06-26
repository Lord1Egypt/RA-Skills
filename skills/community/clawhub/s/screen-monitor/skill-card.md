## Description: <br>
Dual-mode screen sharing and analysis. Model-agnostic (Gemini/Claude/Qwen3-VL). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[emasoudy](https://clawhub.ai/user/emasoudy) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and technical users use this skill to share a browser-selected screen or capture a desktop screenshot so an agent with vision support can analyze visible UI state and answer questions about it. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Screen content may include sensitive data and may be captured or written locally under /tmp. <br>
Mitigation: Share a single non-sensitive window when possible, avoid passwords, customer data, private messages, admin consoles, and regulated information, and stop sharing when finished. <br>
Risk: The skill exposes local screen-sharing functionality intended for analysis, which can be inappropriate on untrusted networks. <br>
Mitigation: Review before installing and use only on trusted networks. <br>


## Reference(s): <br>
- [Screen Monitor ClawHub page](https://clawhub.ai/emasoudy/screen-monitor) <br>
- [Publisher profile](https://clawhub.ai/user/emasoudy) <br>
- [README](README.md) <br>
- [Backend endpoint](references/backend-endpoint.js) <br>
- [Screen analysis helper](references/screen-analyze.sh) <br>
- [Share URL helper](references/get-share-url.sh) <br>
- [Environment check helper](references/env-check.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text analysis with shell command usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a vision-capable model and may use a browser screen-share frame or local screenshot file.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and manifest.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
