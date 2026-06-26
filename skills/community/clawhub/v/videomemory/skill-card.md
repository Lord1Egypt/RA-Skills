## Description: <br>
Start VideoMemory from OpenClaw and return the local UI link. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clamepending](https://clawhub.ai/user/clamepending) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to install, start, relaunch, or check VideoMemory and receive the local UI link after setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and runs an external VideoMemory package. <br>
Mitigation: Install only when the user intends to trust that package and review the safe onboarding explanation before running setup. <br>
Risk: Onboarding can install local bridge files and start a local UI service. <br>
Mitigation: Use the documented safe mode and keep track of the local service so it can be stopped or removed later. <br>


## Reference(s): <br>
- [VideoMemory ClawHub page](https://clawhub.ai/clamepending/videomemory) <br>
- [VideoMemory project homepage](https://github.com/Clamepending/videomemory) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Text] <br>
**Output Format:** [Markdown with shell commands and local UI link text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include the returned local VideoMemory UI link, status output, or actual stderr when setup fails.] <br>

## Skill Version(s): <br>
0.1.15 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
