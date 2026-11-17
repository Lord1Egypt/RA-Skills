## Description:

Supports Universal Robots simulation and control with URSim setup guidance, URScript command examples, RTDE data communication, and Python scripts for joint, Cartesian, IO, and force-mode workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qujingyang28](https://clawhub.ai/user/qujingyang28)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and robotics engineers use this skill to set up URSim, generate or run URScript and RTDE examples, and test Universal Robots motion and IO workflows before considering supervised real-robot use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scripts can send live robot movement, IO, and force commands.

Mitigation: Use URSim or an isolated supervised robot cell, run independent safety checks, and keep an emergency-stop-ready operator present before any hardware test.

Risk: The package was tested in URSim and not validated on real robots.

Mitigation: Re-validate every command at low speed on the target robot model and controller before operational use.

Risk: URSim and RTDE workflows expose local control ports and depend on Docker images and Python packages.

Mitigation: Bind Docker ports to localhost where possible, keep the firewall enabled, and pin Docker images and dependencies.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qujingyang28/skills/ur-robot)
- [Universal Robots official site](https://www.universal-robots.com/)
- [URScript programming documentation](https://www.universal-robots.com/articles/ur/programming/)
- [UR RTDE Python client library](https://github.com/UniversalRobots/RTDE_Python_Client_Library)
- [URSim downloads](https://www.universal-robots.com/download/)
- [RTDE guide](https://www.universal-robots.com/articles/ur/real-time-data-exchange-rtde-guide/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes URSim setup steps, URScript/RTDE examples, and robot-control scripts that may require simulator or hardware access.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact documentation remains v1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
