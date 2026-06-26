## Description: <br>
STM32 AI Assistant is an MCP server that helps coding agents look up STM32 register definitions, pin mappings, quick references, and generate or review HAL initialization code for peripherals such as GPIO, USART, SPI, I2C, ADC, TIM, and EXTI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yeyeeyeeee](https://clawhub.ai/user/yeyeeyeeee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Embedded developers and engineers use this skill to ask an agent for STM32 peripheral facts, pin options, quick-reference guidance, HAL code templates, and checks for common HAL code mistakes. It is intended for agent-assisted firmware development, not as a substitute for board-level validation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated FLASH code can erase device memory or write to the wrong location if copied without review. <br>
Mitigation: Verify the target sector and address, linker layout, calibration data, backups, and erase/program return values before compiling or flashing. <br>
Risk: Generated STM32 HAL code and pin mappings may not match the exact chip, board wiring, clock tree, or project configuration. <br>
Mitigation: Review generated code against the target datasheet, schematic, HAL configuration, and hardware test plan before use. <br>


## Reference(s): <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact Skill Definition](artifact/SKILL.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/yeyeeyeeee/stm32-ai-assistant) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/yeyeeyeeee) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance] <br>
**Output Format:** [MCP text responses containing JSON-formatted lookup results, Markdown/plain-text guidance, and C/HAL code snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should be reviewed against the target STM32 part, board schematic, linker layout, and HAL project configuration before use.] <br>

## Skill Version(s): <br>
5.0.0 (source: ClawHub release evidence; artifact frontmatter and MCP server report 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
