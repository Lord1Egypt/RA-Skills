## Description: <br>
General bilingual ROS1 Noetic skill for ROS questions and ROS project operations across robot dogs, mobile robots, manipulators, perception pipelines, simulation, and OpenClaw integrations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lljj123](https://clawhub.ai/user/lljj123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and robotics engineers use this skill to answer ROS1 Noetic questions, inspect catkin workspaces, build and launch ROS projects, debug active ROS graphs, and plan ROS1 integrations. It supports bilingual guidance and operational workflows for mobile robots, manipulators, simulation, data pipelines, and OpenClaw rosbridge deployments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can launch and stop ROS programs, which may affect running systems or connected robots. <br>
Mitigation: Require explicit user confirmation before launches, stops, rosbag recording, rosbridge exposure, sudo or install commands, and any real-world motion. <br>
Risk: Runtime scripts source local setup and state files, and weak scoping could make untrusted state paths risky on shared machines. <br>
Mitigation: Review the scripts before use, keep runtime state files in a trusted private directory, and avoid passing arbitrary state-file paths. <br>
Risk: Motion-control workflows can send commands to ROS topics when the graph exposes suitable interfaces. <br>
Mitigation: Use simulation-first testing, verify command and telemetry topic types, enforce timeouts, and send explicit stop or neutral commands at the end of motion workflows. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lljj123/ros1-noetic-general) <br>
- [Official ROS1/Noetic Sources](references/official-docs.md) <br>
- [ROS1 Noetic Project Profiles](references/project-profiles.md) <br>
- [ROS1 Noetic Full Scope](references/ros1-full-scope.md) <br>
- [ROS1 Engineering Patterns](references/ros1-engineering-patterns.md) <br>
- [OpenClaw ROS1 Adapter Blueprint](references/ros1-openclaw-adapter.md) <br>
- [ROS1 Knowledge Base Sources](references/ros1-knowledge-base-sources.md) <br>
- [ROS Noetic Documentation](http://docs.ros.org/en/noetic/) <br>
- [ROS Package Index](https://index.ros.org/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include ROS command output interpretation, reproducible command sequences, and safety or confirmation gates for stateful robot operations.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
