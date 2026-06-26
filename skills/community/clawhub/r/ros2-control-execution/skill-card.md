## Description: <br>
Execute ROS 2 Control state-changing commands (load, switch, unload) in a sandboxed environment. Supports parameter profiles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bigrobinson](https://clawhub.ai/user/bigrobinson) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and robotics engineers use this skill to run approved ROS 2 Control state-changing operations such as loading, switching, unloading, and setting controller or hardware component state through a wrapper-driven workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change ROS 2 controller and hardware state in a real robot, lab system, or production ROS environment. <br>
Mitigation: Review each action before execution and require human approval or local guardrails for hardware-affecting commands. <br>
Risk: The security evidence reports a real command-injection weakness and broad runtime authority in the wrapper boundary. <br>
Mitigation: Use only a trusted ROS installation and trusted config/config.json, and avoid untrusted profiles or params files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bigrobinson/ros2-control-execution) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Invocations route through a local Python wrapper and may update ROS 2 controller or hardware state.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
