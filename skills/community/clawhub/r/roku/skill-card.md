## Description: <br>
Control Roku devices via CLI for discovery, remote control, app launching, search, and HTTP bridge mode for real-time control. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gumadeiras](https://clawhub.ai/user/gumadeiras) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to discover same-network Roku devices, issue remote-control commands, launch apps, search content, and configure CLI or HTTP bridge control. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Telegram and local pipe control paths can issue Roku commands without clear access controls. <br>
Mitigation: Use a strong unique bridge token, keep the bridge bound to localhost or a trusted network, and run Telegram or pipe listeners only when remote control is intentional and user access is restricted. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/gumadeiras/roku) <br>
- [Source repository](https://github.com/gumadeiras/roku-cli) <br>
- [python-roku dependency](https://github.com/jcarbaugh/python-roku) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown with inline shell commands and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can include CLI commands, HTTP request examples, and bridge configuration values.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
