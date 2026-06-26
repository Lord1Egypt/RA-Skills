## Description: <br>
Guides developers through debugging I2C, I2S, UART, GPIO, FPGA access, device tree configuration, kernel modules, user-space tools, cross-compilation, and common hardware issues on Xilinx Zynq Linux systems. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[johnwoosz](https://clawhub.ai/user/johnwoosz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and hardware engineers use this skill to generate or review Zynq Linux debugging commands, device tree snippets, kernel module build commands, and troubleshooting guidance for board bring-up and peripheral debugging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can suggest commands that write registers, GPIO values, FPGA bitstreams, I2C registers, or kernel module state on live hardware. <br>
Mitigation: Verify every address, register, GPIO number, bitstream, bus, and module action against board documentation, and prefer read-only checks before write operations. <br>
Risk: Incorrect low-level hardware commands can disrupt development boards or production systems. <br>
Mitigation: Use the guidance on non-production or recoverable systems first, and review commands with an engineer familiar with the target Zynq board. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/johnwoosz/zynq-linux-dev) <br>
- [Publisher profile](https://clawhub.ai/user/johnwoosz) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash, C, and device tree code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include hardware-mutating commands that require board-specific verification before use.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
