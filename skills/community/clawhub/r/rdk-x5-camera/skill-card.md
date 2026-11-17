## Description:

Configures and starts MIPI CSI, USB, and depth cameras on RDK X5, then guides live browser preview, image capture, and connection troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[katherineedwards2475](https://clawhub.ai/user/katherineedwards2475)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and robotics engineers use this skill to bring up camera hardware on RDK X5, preview live image streams in a browser, capture images, tune ISP settings, and troubleshoot common camera connection issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes root-level package installation and ISP tuning commands.

Mitigation: Review and separate build, package installation, and sudo tuning steps before execution; approve privileged commands only in a trusted RDK X5 camera environment.

Risk: The skill includes broad process-kill commands for stopping camera services.

Mitigation: Prefer shutting down specific ROS 2 nodes or known camera, websocket, and codec processes instead of running broad pkill patterns.

Risk: Wildcard package installation can install more packages than intended.

Mitigation: Replace wildcard package names with exact package names where possible before installing dependencies.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/katherineedwards2475/skills/rdk-x5-camera)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and troubleshooting tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires RDK X5 camera hardware, ROS 2 tooling, and user review before running privileged setup or tuning commands.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
