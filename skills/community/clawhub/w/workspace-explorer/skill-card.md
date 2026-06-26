## Description: <br>
Securely share your workspace with your owner via a remote VS Code environment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mrbeandev](https://clawhub.ai/user/mrbeandev) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to give a trusted owner temporary browser-based VS Code access for live inspection of a selected workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives remote browser-based access to a local workspace through a public tunnel and relies on external runtime code that is not included in the reviewed package. <br>
Mitigation: Use it only when a trusted person needs access; review the external repository and start script first, serve the smallest sanitized directory, remove secrets and credentials, share the URL and password only with the intended recipient, and stop the tunnel immediately when finished. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mrbeandev/workspace-explorer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and terminal output examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May provide a temporary public tunnel URL and generated password when the workspace server is started.] <br>

## Skill Version(s): <br>
1.1.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
