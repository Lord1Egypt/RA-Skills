## Description: <br>
Wake-on-LAN skill for waking computers by device name or IP address and managing saved device configurations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Lroyia](https://clawhub.ai/user/Lroyia) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and device administrators use WOL to wake authorized computers on a local network and maintain the device records needed for Wake-on-LAN commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores and changes device records that include network identifiers such as MAC addresses and IP addresses. <br>
Mitigation: Use add and delete commands only for intentional device-list changes, and avoid exposing the device configuration file in conversation. <br>
Risk: Wake commands can send packets to devices on the local network. <br>
Mitigation: Run wake commands only for devices the user is authorized to wake, and verify the target name or IP address before execution. <br>
Risk: The release security summary says the script can expose full MAC addresses despite privacy guidance. <br>
Mitigation: Review or patch the script before relying on MAC masking, and treat MAC addresses as sensitive device identifiers. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Lroyia/wol) <br>
- [Device configuration reference](references/devices.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Text and Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can modify saved device records and can send Wake-on-LAN packets on the local network.] <br>

## Skill Version(s): <br>
1.0.2 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
