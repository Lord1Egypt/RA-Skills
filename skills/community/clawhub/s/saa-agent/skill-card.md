## Description: <br>
Enables AI agents to generate images using the Character Select Stand Alone App (SAA) image generation backend via command-line interface. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mirabarukaso](https://clawhub.ai/user/mirabarukaso) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and AI-agent users use this skill to drive a local or reachable SAA image-generation backend from CLI commands, including standard and regional prompt workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: WSS connections weaken transport security when certificate and hostname verification are disabled. <br>
Mitigation: Install only when the SAA backend and network path are trusted; prefer local or private-network use. <br>
Risk: Credentials can be exposed through command-line arguments, transcripts, or logs. <br>
Mitigation: Avoid passing real passwords on the command line when possible and redact credentials from transcripts and logs. <br>
Risk: The skeleton-key option can forcefully unlock the backend while another generation is active. <br>
Mitigation: Use --skeleton-key only after confirming no other generation is active and the user explicitly approves the unlock. <br>
Risk: Automatic retries can worsen backend congestion when SAA reports a busy state. <br>
Mitigation: Do not chain retries; wait 20-60 seconds and let the user decide when to retry. <br>


## Reference(s): <br>
- [Character Select Stand Alone App project](https://github.com/mirabarukaso/character_select_stand_alone_app) <br>
- [SAA Agent ClawHub listing](https://clawhub.ai/mirabarukaso/saa-agent) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown with inline bash commands; generated images are saved as PNG files or emitted as base64 when requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a running SAA backend, SAAC enabled, a WebSocket address, and Python dependencies for websockets and aiohttp.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
