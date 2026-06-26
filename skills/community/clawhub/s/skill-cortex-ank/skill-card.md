## Description: <br>
Skill Cortex helps OpenClaw agents find, install, use, learn from, and discard short-term skills from ClawHub or GitHub when installed skills cannot handle a task. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ankwu001](https://clawhub.ai/user/ankwu001) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill when the current installed skill set cannot complete a task and the agent needs to locate, install, execute, learn from, and then remove a short-term capability. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can let an agent find, install, execute, remember, and remove other skills at runtime. <br>
Mitigation: Use it only when that level of runtime skill management is acceptable, and require explicit approval for installation and execution. <br>
Risk: Reflex behavior can reduce the normal execution-plan confirmation flow for frequently successful read-only tasks. <br>
Mitigation: Keep reflex behavior disabled or require explicit approval for every install and execution unless the candidate is reviewed and version-locked. <br>
Risk: GitHub candidates may be unreviewed sources when ClawHub results are insufficient. <br>
Mitigation: Inspect unreviewed GitHub candidates before installation or restrict use to reviewed ClawHub skills. <br>
Risk: The local cortex memory file records routing history and lessons about prior skill use. <br>
Mitigation: Periodically review or delete the local cortex memory file and avoid storing concrete personal, project, location, or file identifiers. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/ankwu001/skill-cortex-ank) <br>
- [README](artifact/README.md) <br>
- [Design document](artifact/DESIGN.md) <br>
- [OpenClaw](https://github.com/openclaw) <br>
- [ClawHub](https://clawhub.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes candidate summaries, execution plans, side-effect warnings, failure reports, and local cortex memory updates.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter states 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
