## Description: <br>
Python-based LiveVideoStore client with voice interaction, GUI, volume control, session management, and encrypted audio transmission for live streaming. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[robertlee-lab](https://clawhub.ai/user/robertlee-lab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and researchers use LiveVideoStore to run a Python Xiaoyou voice client for live-streaming voice interaction, including push-to-talk recording, session management, and encrypted audio transport. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Microphone audio and device identifiers may be transmitted to remote Xiaoyou/Tenclass service endpoints after a voice session starts. <br>
Mitigation: Run only in trusted environments, disclose remote voice processing to users, avoid sensitive audio, and review endpoint trust before installation. <br>
Risk: The Windows setup path asks users to copy an unverified opus.dll into C:\Windows\System32. <br>
Mitigation: Prefer a verified, pinned, app-local Opus dependency and avoid modifying system directories. <br>
Risk: The artifact contains or creates persistent device identifiers and MAC-like values for service registration. <br>
Mitigation: Treat local device configuration as environment-specific data and avoid publishing reused identifiers. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/robertlee-lab/ult-xiaoyou) <br>
- [Xiaozhi device console referenced by the client](https://xiaozhi.me/console/devices) <br>
- [Opus dependency source referenced by the client](https://github.com/QiKeO/py-xiaozhi) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes runtime guidance for a Python voice client that uses microphone input, MQTT, UDP audio transport, and local device configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
