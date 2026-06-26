## Description: <br>
Manage temporary files in workspace temp directory. All non-essential files must go to temp/, keeping workspace root clean. Auto-detects workspace from openclaw.json config. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lichenyang-zk](https://clawhub.ai/user/lichenyang-zk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to keep downloaded, copied, generated, and intermediate files inside a per-session workspace temp directory instead of cluttering the workspace root. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Temporary copies may contain sensitive data such as passwords, API keys, or secrets. <br>
Mitigation: Avoid processing secrets unless necessary, and clean the per-session temp directory after use. <br>
Risk: The skill depends on reading OpenClaw workspace configuration and session information to choose the temp directory. <br>
Mitigation: Install only when that local read access is acceptable and verify the configured workspace before use. <br>
Risk: The promise not to modify pre-existing workspace files is guidance rather than technical enforcement. <br>
Mitigation: Review file operations before execution and keep writes restricted to the resolved per-session temp directory. <br>


## Reference(s): <br>
- [Workspace Temp on ClawHub](https://clawhub.ai/lichenyang-zk/workspace-temp) <br>
- [Publisher profile](https://clawhub.ai/user/lichenyang-zk) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, shell commands] <br>
**Output Format:** [Markdown guidance with procedural steps and code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs focus on temp directory resolution, file handling rules, cleanup guidance, and permission-aware error handling.] <br>

## Skill Version(s): <br>
1.1.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
