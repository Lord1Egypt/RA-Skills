## Description: <br>
Skill Cortex helps an OpenClaw agent find, validate, install, use, release, and learn from temporary skills when installed skills cannot complete the current task. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ankwu001](https://clawhub.ai/user/ankwu001) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw agent users use this skill to add a temporary capability layer that searches for candidate skills, presents safety information for approval, installs approved skills, executes the requested task, and updates short-term routing memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can add and run skills from external sources for tasks the current agent cannot handle. <br>
Mitigation: Install only after reviewing each candidate's source, version, scan status, requested permissions, and side effects. <br>
Risk: Persistent routing memory can affect future skill selection and reflex behavior. <br>
Mitigation: Periodically inspect or reset ~/.openclaw/skill-cortex/cortex.json if routing or reflex behavior seems wrong. <br>
Risk: System dependency installation may broaden the environment's behavior or permissions. <br>
Mitigation: Require separate explicit approval before installing system dependencies. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ankwu001/skill-cortex-pub) <br>
- [OpenClaw project](https://github.com/openclaw) <br>
- [ClawHub](https://clawhub.ai) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline commands and JSON configuration references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose candidate skills, execution plans, side-effect warnings, and updates to short-term cortex memory.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
