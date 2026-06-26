## Description: <br>
OpenClaw plugin development assistant that produces runnable plugin skeletons, install commands, and debugging steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[boleyn](https://clawhub.ai/user/boleyn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to decide whether an OpenClaw extension should be a Skill or Plugin, then generate a minimal plugin scaffold with install, debug, publish, rollback, and troubleshooting guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated install, publish, or rollback commands may affect local projects, registry accounts, credentials, or published releases. <br>
Mitigation: Confirm the target project, registry or account, credentials, and expected side effects before execution; prefer dry runs or backups where available. <br>
Risk: Generated plugin scaffolds or troubleshooting guidance may be incomplete or unsuitable for a specific OpenClaw project. <br>
Mitigation: Review generated files and commands before deployment, then test locally before publishing. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with code blocks and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes plugin skeleton file contents, install/debug/publish/rollback commands, and risk troubleshooting notes.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
