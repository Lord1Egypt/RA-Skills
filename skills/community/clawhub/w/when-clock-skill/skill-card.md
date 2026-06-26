## Description: <br>
Control WHEN/WHEN Voice LAN clock devices with voice time announcement, weather broadcast on WHEN Voice, alarm CRUD, and countdown timer modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[master-gong](https://clawhub.ai/user/master-gong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate configured WHEN and WHEN Voice LAN clocks from an agent or CLI, including listing, adding, editing, and deleting alarms and creating countdown timer reminders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change alarms on configured LAN clocks, and set_timer can replace an existing alarm when the device already has ten alarms. <br>
Mitigation: Configure only your own device IPs, run get_alarm before edit_alarm, delete_alarm, or set_timer, and avoid set_timer on a full alarm list unless replacing the tenth alarm is intended. <br>
Risk: The bundled protocol documents describe administrative endpoints beyond normal clock and alarm control. <br>
Mitigation: Treat the protocol documents as administrative reference material and avoid Wi-Fi, password, reboot, OTA, or factory-reset endpoints unless device administration is intentional. <br>
Risk: The artifact config.json contains example private LAN addresses that may not match the user's devices. <br>
Mitigation: Replace config.json device entries with the intended clock IDs and IP addresses before running the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/master-gong/when-clock-skill) <br>
- [WHEN product page](https://iottimer.com/products/when/) <br>
- [WHEN Voice product page](https://iottimer.com/products/when_voice/) <br>
- [WHEN web API protocol](artifact/docs/WHEN_WEB_API_PROTOCOL.md) <br>
- [WHEN Voice web API protocol](artifact/docs/WHEN_VOICE_WEB_API_PROTOCOL.md) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON responses from a Python CLI, with errors on stderr and numeric exit codes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires config.json device entries with device IDs and LAN clock IP addresses.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and artifact _meta.json; SKILL.md frontmatter says 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
