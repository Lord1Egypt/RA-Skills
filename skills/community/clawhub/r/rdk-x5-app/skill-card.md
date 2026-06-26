## Description: <br>
Guides agents through running the RDK X5 /app preinstalled examples, including Python AI demos, 40-pin GPIO samples, C++ multimedia demos, and the bundled BPU model library. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[katherineedwards2475](https://clawhub.ai/user/katherineedwards2475) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill when working on an RDK X5 board to run preinstalled /app demos, test Python AI samples, compile C++ multimedia examples, exercise GPIO interfaces, or inspect bundled BPU models. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Camera, web display, and RTSP examples can expose sensitive video streams or credentials if used on an untrusted network. <br>
Mitigation: Use the web and RTSP demos only on trusted networks, treat stream URLs and camera output as sensitive, and stop services when finished. <br>
Risk: GPIO and hardware examples include sudo commands that can affect connected peripherals. <br>
Mitigation: Run sudo hardware examples only on the intended RDK X5 board after confirming wiring and peripheral behavior. <br>
Risk: Using a conda or virtualenv Python can fail because RDK X5 hardware libraries are installed in the system Python. <br>
Mitigation: Use the system Python path documented by the skill, such as /usr/bin/python3.10, for hardware-dependent demos. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash code blocks and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands assume an RDK X5 environment with python3 and board-specific preinstalled /app assets.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
