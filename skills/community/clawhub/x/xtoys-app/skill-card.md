## Description: <br>
Control xtoys.app devices via webhook for remote intimate device control. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kasuganosora](https://clawhub.ai/user/kasuganosora) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to configure and invoke xtoys.app webhook controls for connected intimate devices, including intensity changes, stop commands, action listing, and connection tests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent direct physical-control authority over connected intimate devices. <br>
Mitigation: Use only with explicit, current consent from every affected person and require confirmation before every non-zero control action. <br>
Risk: The advertised stop or test tools may not reliably stop an active device. <br>
Mitigation: Do not rely on these tools as emergency controls until the implementation is fixed and verified with the target device setup. <br>
Risk: A leaked webhook ID could allow unauthorized remote control. <br>
Mitigation: Treat the webhook ID like a password, keep it out of public files, and prefer secure environment or secret storage. <br>
Risk: Dependency behavior may change because requirements use broad lower bounds. <br>
Mitigation: Pin reviewed dependency versions before deployment. <br>


## Reference(s): <br>
- [Xtoys.app](https://xtoys.app) <br>
- [ClawHub skill page](https://clawhub.ai/kasuganosora/xtoys-app) <br>
- [Artifact README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, API Calls, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, Python snippets, JSON configuration, and webhook API calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an xtoys.app webhook ID and may send remote physical-control requests to connected devices.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
