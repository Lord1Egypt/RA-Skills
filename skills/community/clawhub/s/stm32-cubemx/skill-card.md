## Description:

STM32CubeMX CLI operations for configuring pins, peripherals, DMA, interrupts, and generating code for STM32 projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aidankong](https://clawhub.ai/user/aidankong)

### License/Terms of Use:


## Use Case:

Developers and embedded engineers use this skill to update STM32CubeMX .ioc configuration, configure common peripherals, set up DMA and interrupts, generate project code, and verify CMake/GCC builds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A build cleanup example uses rm -rf build/Debug and could remove unintended files if run from the wrong project directory.

Mitigation: Confirm PROJECT_DIR and generated paths before execution, guard cleanup commands, or use a safer clean/build workflow.

## Reference(s):

- [USART + DMA Complete Configuration](references/USART_DMA.md)
- [IOC File Structure Reference](references/IOC_structure.md)
- [UM1718 STM32CubeMX User Manual](https://www.st.com/resource/en/user_manual/um1718-stm32cubemx-description-stmicroelectronics.pdf)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell commands and INI/C configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are guidance and proposed commands or configuration snippets for the user to review before applying.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
