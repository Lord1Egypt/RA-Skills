## Description: <br>
Access to RDK X5 /app folder resources including GPIO, multimedia, AI samples. Invoke when user wants to run embedded demos or control hardware on RDK X5. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Zh1fen](https://clawhub.ai/user/Zh1fen) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to locate and run RDK X5 board resources for GPIO, I2C/SPI, UART, camera, multimedia, AI inference, and ISP tuning workflows under /app. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: GPIO, bus, camera, media pipeline, and ISP commands can affect attached RDK X5 hardware or peripherals. <br>
Mitigation: Before execution, confirm the board model, pin numbering, voltage and current limits, connected peripherals, and whether the command may move, power, display, capture, or retune hardware. <br>
Risk: Python samples may fail or behave incorrectly if run from a conda environment without the board-provided libraries. <br>
Mitigation: Use the documented system Python interpreter, /usr/bin/python3.10, for RDK X5 Python samples that depend on D-Robotics libraries. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Zh1fen/rdkx5-app-resources) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands target RDK X5 /app resources and should be reviewed before execution on hardware.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
