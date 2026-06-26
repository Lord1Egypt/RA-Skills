## Description: <br>
Install, start, stop, and health-check Yuzhua (gesture + voice + OpenClaw gateway) with minimal manual setup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[juguangyuan520-dotcom](https://clawhub.ai/user/juguangyuan520-dotcom) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and local OpenClaw users use this skill to install and manage Yuzhua for gesture-triggered, local voice AI conversations through an OpenClaw gateway. It supports setup, startup, health checks, and stopping the local Yuzhua process. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The install script clones or updates the configured Yuzhua repository. <br>
Mitigation: Install only when the configured repository is trusted and review local changes before running the downloaded project. <br>
Risk: The skill may create or use a local .env file that can contain tokens. <br>
Mitigation: Review the generated .env, keep real tokens out of commits, and restrict access to the local project directory. <br>
Risk: Conversation routing goes through the local OpenClaw gateway. <br>
Mitigation: Confirm what the gateway sends to configured providers before using the skill with sensitive prompts or audio. <br>
Risk: The stop script terminates processes on the configured port and may affect an unrelated local process. <br>
Mitigation: Check the configured port before running stop.sh and change YUZHUA_PORT when another service uses the default port. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/juguangyuan520-dotcom/yuzhua) <br>
- [Yuzhua GitHub Repository](https://github.com/juguangyuan520-dotcom/Yuzhua) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash commands and environment variable guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local setup and operations guidance for cloning or updating Yuzhua, preparing .env, starting the app, checking the local status endpoint, and stopping the configured port.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
