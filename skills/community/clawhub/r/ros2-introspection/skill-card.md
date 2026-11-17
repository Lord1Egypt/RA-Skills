## Description:

Execute core ROS 2 introspection commands to query the ROS graph, including topics, nodes, services, actions, and parameters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bigrobinson](https://clawhub.ai/user/bigrobinson)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and robotics engineers use this skill to inspect a ROS 2 graph and gather read-only information about topics, nodes, services, actions, parameters, interfaces, and graph visualization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The safety claims are overstated because strict read-only behavior depends on trusting the local ROS environment and generated configuration.

Mitigation: Install only in trusted ROS environments and avoid deployments that require strict read-only behavior or strong sandboxing until the setup path and command arguments are constrained.

Risk: The configured ROS setup path can be executed unsafely if it is not safely quoted or allowlisted.

Mitigation: Verify or allowlist the generated setup path before use, and review the configuration file created during setup.

Risk: The skill can read live ROS topic and parameter data and can launch rqt_graph.

Mitigation: Use it only on ROS graphs where inspection of topic, parameter, and graph metadata is permitted, and review outputs for sensitive operational data before sharing.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and command output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces read-only ROS 2 introspection guidance and command invocations through the bundled wrapper.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
