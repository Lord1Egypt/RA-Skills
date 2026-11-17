## Description:

STM32 AI Assistant is an MCP server that helps AI coding assistants query STM32 register definitions, inspect peripherals and pins, check HAL code, and generate STM32 HAL initialization code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yeyeeyeeee](https://clawhub.ai/user/yeyeeyeeee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and embedded engineers use this skill to ask an agent for STM32 register lookups, peripheral summaries, pin mappings, HAL template generation, and basic HAL code checks while working on STM32 firmware.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP server has an under-disclosed path traversal bug that can read files outside its bundled templates under constrained names.

Mitigation: Review the MCP server code before installation or wait for a release that restricts chip and peripheral names to an allowlist.

Risk: Generated STM32 templates may be unsafe or incorrect for a specific board, clock tree, memory map, or safety requirement.

Mitigation: Treat generated FLASH, CAN, relay, buzzer, watchdog, power, interrupt, and other hardware-affecting examples as starting points and validate them before flashing hardware.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yeyeeyeeee/skills/stm32-ai-assistant)
- [README](README.md)
- [SKILL.md](SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with JSON MCP configuration snippets and C HAL code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated code and checks should be reviewed against the target board schematic, clock tree, memory map, and safety requirements before flashing hardware.]

## Skill Version(s):

5.0.0 (source: server release evidence; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
