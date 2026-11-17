## Description:

Zynq Linux Hardware Debug helps agents provide debugging guidance for Xilinx Zynq-7000 and Zynq UltraScale+ Linux systems, including I2C, I2S, UART, GPIO, FPGA access, device tree examples, kernel module commands, cross-compilation, and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnwoosz](https://clawhub.ai/user/johnwoosz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and hardware engineers use this skill to ask an agent for Zynq Linux peripheral debugging workflows, example shell commands, device tree snippets, kernel-module build commands, user-space access examples, and troubleshooting checks for PetaLinux, Debian, or custom Linux deployments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can suggest hardware writes, FPGA loads, kernel module changes, and devmem/devmem2 commands that may affect a real board.

Mitigation: Require explicit operator approval before executing any write, FPGA load, kernel module change, or direct memory access command, and confirm the board, register map, bus numbers, and peripheral effects first.

Risk: Example bus numbers, addresses, GPIO lines, and register values may not match the target hardware.

Mitigation: Treat commands as templates and verify target-specific values against the board design, device tree, and hardware documentation before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/johnwoosz/skills/zynq-linux-dev)
- [ClawHub Publisher Profile](https://clawhub.ai/user/johnwoosz)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash, C, and device tree code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include hardware access commands that should be reviewed before execution on real boards.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
