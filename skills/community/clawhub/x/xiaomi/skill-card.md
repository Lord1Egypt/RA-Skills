## Description: <br>
Control Xiaomi Home devices on a local network with miiocli for status checks, power toggles, and MIOT property updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yiqiezhenxi](https://clawhub.ai/user/yiqiezhenxi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and home automation users use this skill to let an agent translate natural language requests into miiocli commands for Xiaomi Home devices on a local network, including status checks, power toggles, and MIOT property updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Xiaomi device tokens can grant local control of smart-home devices. <br>
Mitigation: Treat tokens like passwords: do not share them in chats, commit them to repositories, or store them in broadly readable files. <br>
Risk: Generated miiocli commands can change physical appliance state, including power, heating, cooking, and humidifier settings. <br>
Mitigation: Require explicit user confirmation before state-changing commands and verify the target device and action before execution. <br>
Risk: Token extraction and dependency installation steps may run local commands before device control is configured. <br>
Mitigation: Review token-extraction and install commands before running them, and execute them only in a trusted local environment. <br>


## Reference(s): <br>
- [ClawHub Xiaomi Skill Page](https://clawhub.ai/yiqiezhenxi/xiaomi) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and device configuration placeholders.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands require device IP addresses and Xiaomi tokens, and may change physical device state.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
