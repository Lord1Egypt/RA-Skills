## Description: <br>
Generate XMind mind map files (.xmind) from Markdown outlines or plain text descriptions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Geoion](https://clawhub.ai/user/Geoion) <br>

### License/Terms of Use: <br>
ISC <br>


## Use Case: <br>
Developers and agents use this skill to convert Markdown outlines or structured text into local .xmind files for mind maps and planning artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Input and output paths can point outside the intended workspace. <br>
Mitigation: Keep input and output paths inside the workspace and review the resolved output path before opening or sharing the file. <br>
Risk: Installing dependencies fetches the declared xmind package and transitive npm packages. <br>
Mitigation: Install dependencies in the skill directory using the provided package lock and apply normal dependency review for the environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Geoion/xmind-generator) <br>
- [xmind npm package](https://registry.npmjs.org/xmind/-/xmind-2.2.33.tgz) <br>


## Skill Output: <br>
**Output Type(s):** [files, shell commands, configuration] <br>
**Output Format:** [.xmind file plus concise terminal status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js, npm install, and the xmind package; output defaults to output.xmind unless a path is provided.] <br>

## Skill Version(s): <br>
1.0.3 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
