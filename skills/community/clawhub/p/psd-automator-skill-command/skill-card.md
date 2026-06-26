## Description: <br>
Dispatch PSD automation tasks through skill command entry while reusing the same /psd orchestrator. Requires psd-automator core. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dhrxy](https://clawhub.ai/user/dhrxy) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to invoke PSD automation from a skill command while preserving the existing /psd orchestration behavior. It supports dispatching PSD edits from either a task JSON path or natural-language requirements, including Chinese-language requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PSD automation can modify source design files and write exported assets. <br>
Mitigation: Use --dry-run first, restrict task and index paths, and run on copies or version-controlled assets when changes matter. <br>
Risk: The skill depends on the separate psd-automator core for actual automation behavior. <br>
Mitigation: Install and use this command only when the required psd-automator core is trusted and reviewed for the intended environment. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown with command examples and task-dispatch guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Invokes PSD automation through the psd_automator_skill_command tool and may write modified PSD exports.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
