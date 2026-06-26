## Description: <br>
Execute core ROS 2 introspection commands to query the ROS graph (topics, nodes, services, actions, parameters). STRICTLY read-only. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bigrobinson](https://clawhub.ai/user/bigrobinson) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and robotics engineers use this skill to inspect ROS 2 topics, nodes, services, actions, parameters, and interfaces without running nodes, calling services, or sending action goals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Topic echo and parameter dump output may expose sensitive robot or system data. <br>
Mitigation: Install only in a ROS environment you control and review introspection output before sharing, storing, or acting on it. <br>
Risk: The rqt_graph command can launch a GUI process. <br>
Mitigation: Avoid rqt_graph when a GUI process is not desired or not allowed in the execution environment. <br>
Risk: Setup depends on the detected ROS setup path and writes it into config/config.json. <br>
Mitigation: Review config/config.json after setup and rerun setup after changing ROS distributions or environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bigrobinson/ros2-introspection) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration guidance] <br>
**Output Format:** [Markdown with inline shell commands and ROS 2 command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only ROS 2 introspection results; topic echo and parameter dump output may contain sensitive robot or system data.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
