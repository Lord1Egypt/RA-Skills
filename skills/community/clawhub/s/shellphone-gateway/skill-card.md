## Description: <br>
Guides setup of ShellPhone/OpenClaw Gateway for connecting iOS devices to self-hosted AI agents over WebSocket. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[loserbcc](https://clawhub.ai/user/loserbcc) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and self-hosters use this skill to install and connect the gateway, iOS TestFlight app, local AI agents, and the speech services described by the release. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The self-hosted privacy claim is incomplete because ScrappyLabs speech features may send audio or text outside the local environment. <br>
Mitigation: Before installing, confirm whether ScrappyLabs is optional, what data it receives, and how to disable TTS or ASR features. <br>
Risk: The release depends on third-party GitHub, PyPI, Docker Compose, and TestFlight distribution paths. <br>
Mitigation: Verify the repository, package, compose file, and TestFlight publisher before running or connecting devices. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/loserbcc/shellphone-gateway) <br>
- [Gateway GitHub](https://github.com/loserbcc/openclaw-gateway) <br>
- [ShellPhone TestFlight](https://testflight.apple.com/join/BnjD4BEf) <br>
- [ScrappyLabs](https://scrappylabs.ai) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown setup guidance with shell commands and URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference external install, TestFlight, and speech-service links.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
