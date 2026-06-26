## Description: <br>
Execute ROS 2 Control read-only introspection commands (list, view) in a sandboxed environment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bigrobinson](https://clawhub.ai/user/bigrobinson) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and robotics engineers use this skill to inspect ROS 2 Control controller managers, hardware components, interfaces, and controller chains without loading, switching, or modifying controllers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The wrapper sources a local ROS 2 setup path, so an untrusted ROS environment could influence command execution. <br>
Mitigation: Install only in trusted ROS 2 environments and review the generated config.json on unusual systems. <br>
Risk: Profile and --params-file inputs can alter ROS arguments passed to the introspection command. <br>
Mitigation: Use only trusted profile and parameter files, and treat the wrapper as a read-oriented guard rather than a complete security sandbox. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/bigrobinson/ros2-control-introspection) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/bigrobinson) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces read-only ROS 2 Control command invocations through the safe wrapper script.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
