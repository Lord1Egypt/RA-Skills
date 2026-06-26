## Description: <br>
Real-time companion monitor for OpenClaw agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luccast](https://clawhub.ai/user/luccast) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use Crabwalk to install and run a real-time monitor for OpenClaw agents, including activity views, workspace browsing, and gateway-token aware connectivity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The monitor can expose agent activity, workspace files, and local OpenClaw gateway token access through a web server. <br>
Mitigation: Bind the service to localhost or a protected interface, share URLs only with trusted viewers, and review host, port, and token settings before starting it. <br>
Risk: Installation and update commands download release artifacts, edit PATH, and may install optional packages with system package managers. <br>
Mitigation: Review commands before execution, ask user permission before updates, and avoid sudo package installation unless the user approves it. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/luccast/public) <br>
- [Crabwalk Homepage](https://crabwalk.app) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash code blocks and CLI instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes installation, verification, start, update, and troubleshooting guidance.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
