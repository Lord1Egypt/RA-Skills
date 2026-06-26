## Description: <br>
Execute ROS 2 commands (run, launch, call) in a sandboxed, allowlisted environment with support for parameter profiles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bigrobinson](https://clawhub.ai/user/bigrobinson) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and robotics engineers use this skill to let an agent run selected ROS 2 nodes, launches, service calls, and action goals through an allowlisted wrapper in a trusted ROS workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad authority to run ROS 2 commands that may affect robot behavior or actuators. <br>
Mitigation: Use it only in trusted ROS workspaces, keep package allowlists narrow, and require human approval before commands that could move hardware or affect actuators. <br>
Risk: The skill depends on local configuration and parameter files whose contents influence ROS command execution. <br>
Mitigation: Keep config.json and packages.json writable only by trusted users, prefer named parameter profiles, and review any arbitrary parameter file before use. <br>
Risk: The security evidence says the skill is purpose-aligned but overstates or inconsistently describes its safety limits. <br>
Mitigation: Review the wrapper behavior and security limits before installing or enabling the skill on a real ROS system. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local ROS 2 setup, generated config files, package allowlists, and optional YAML parameter profiles.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
