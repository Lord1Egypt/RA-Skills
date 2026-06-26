## Description: <br>
STM32CubeMX CLI operations for configuring pins, peripherals, DMA, interrupts, and generating code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Aidankong](https://clawhub.ai/user/Aidankong) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and embedded engineers use this skill to update STM32CubeMX IOC configuration, generate STM32 project code, and verify CMake/GCC builds for STM32 firmware projects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Clean-build commands can delete build artifacts if PROJECT_DIR points to the wrong project folder. <br>
Mitigation: Verify PROJECT_DIR, IOC_FILE, SCRIPT_FILE, and CUBEMX before running shell snippets, and keep the project in version control or backed up. <br>
Risk: STM32CubeMX code generation can overwrite generated project files. <br>
Mitigation: Review proposed IOC changes before generation and inspect the resulting diff before using generated code. <br>


## Reference(s): <br>
- [USART + DMA Complete Configuration](references/USART_DMA.md) <br>
- [IOC File Structure Reference](references/IOC_structure.md) <br>
- [UM1718 STM32CubeMX User Manual](https://www.st.com/resource/en/user_manual/um1718-stm32cubemx-description-stmicroelectronics.pdf) <br>
- [ClawHub Skill Page](https://clawhub.ai/Aidankong/stm32-cubemx) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell and IOC configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include STM32CubeMX CLI commands, IOC key-value configuration examples, and CMake build verification steps.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
