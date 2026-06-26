## Description: <br>
Guides agents through Universal Robots URSim setup, URScript motion and I/O commands, RTDE status reading, and related Python test or example workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qujingyang28](https://clawhub.ai/user/qujingyang28) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Robotics developers and automation engineers use this skill to configure URSim, send URScript commands, read RTDE status, and prepare cautious test workflows for Universal Robots systems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Runnable examples and tests can move a robot, apply force mode, or change I/O. <br>
Mitigation: Run workflows in URSim first, verify the target IP before execution, review scripts that send motion or I/O commands, keep the workcell clear, and keep emergency stop available. <br>
Risk: Artifact evidence says real robot operation has not been verified. <br>
Mitigation: Require qualified operator supervision, perform a site-specific risk assessment, use low initial speed and acceleration, and revalidate every command before use on physical hardware. <br>
Risk: System setup guidance may involve Docker relocation or firewall changes. <br>
Mitigation: Avoid those changes unless necessary, maintain backups, document rollback steps, and confirm the system impact before applying them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qujingyang28/ur-robot) <br>
- [Universal Robots official site](https://www.universal-robots.com/) <br>
- [Universal Robots programming resources](https://www.universal-robots.com/articles/ur/programming/) <br>
- [RTDE Python Client Library](https://github.com/UniversalRobots/RTDE_Python_Client_Library) <br>
- [Universal Robots downloads](https://www.universal-robots.com/download/) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill documentation](artifact/SKILL.md) <br>
- [URScript feature checklist](artifact/URSCRIPT_FEATURES.md) <br>
- [Artifact test report](artifact/TEST_REPORT.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes simulator-first workflows, URScript examples, RTDE usage notes, and safety-oriented configuration guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
