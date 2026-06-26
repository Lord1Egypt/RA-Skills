## Description: <br>
Provides Raspberry Pi camera photo capture, video recording, and GIF generation through an HTTP service and Python client. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CLD1994](https://clawhub.ai/user/CLD1994) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to deploy and operate a Raspberry Pi HTTP camera service for capturing photos, recording H264/MP4/GIF video, and managing media files from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The service exposes camera and media controls over a network API without built-in authentication. <br>
Mitigation: Run it only on a trusted network, bind it to localhost or firewall it, and add authentication or another access control before broader use. <br>
Risk: Remote download and delete endpoints can expose or remove captured media if the service is reachable by unintended clients. <br>
Mitigation: Restrict those endpoints, limit network reachability, and protect stored output files according to the deployment environment. <br>
Risk: The installer creates a persistent system service and performs privileged installation steps. <br>
Mitigation: Review the sudo installer behavior before deployment and avoid running the service process as root. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/CLD1994/raspberry-pi-camera-service) <br>
- [Client usage guide](references/client_usage.md) <br>
- [Deployment guide](references/deploy_service.md) <br>
- [Service design document](references/design.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes deployment steps, client API usage, and service configuration guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
