## Description: <br>
Repeatedly output a string (or 'y' by default) for automated scripts, batch confirmation, and pipeline input generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to generate repeated text for pipeline input or scripted confirmation workflows. It should be used only where downstream prompts and command effects have been reviewed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unattended confirmation can approve deletion, package management, account changes, legal consent, privileged actions, or other irreversible commands. <br>
Mitigation: Review the exact downstream command, prompt text, and consequences before piping generated responses into any sensitive operation. <br>
Risk: The documentation claims options such as --count, --sleep, --hex, --json, and --no-newline that the provided script does not implement. <br>
Mitigation: Do not rely on those options unless the implementation is fixed and retested; use external controls such as reviewed wrappers or timeouts when bounded output is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dinghaibin/yes-tool) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text stream with command examples and usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The provided script repeats one string until the process stops; documented flags such as --count, --sleep, --hex, --json, and --no-newline are not implemented in the artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
