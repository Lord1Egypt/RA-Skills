## Description:

Generates Veo videos from natural language prompts through the Wanjie Ark model service with background task monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liangshenghzj888-stack](https://clawhub.ai/user/liangshenghzj888-stack)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users can use this skill to request short Veo video generation from chat prompts and monitor completion through the skill's background workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Video prompts and a configured API key are sent to a Wanjie-hosted service.

Mitigation: Use a dedicated low-quota Wanjie key and confirm the selected provider credential before installation.

Risk: The artifact can install Python dependencies at runtime and run background generation tasks.

Mitigation: Review or disable automatic dependency installation and background task behavior before use in managed environments.

Risk: Generated result URLs may be opened automatically in the user's browser and written to local result/log files.

Mitigation: Review browser-opening behavior and local log/result retention for the deployment environment.

## Reference(s):

- [Wanjie Ark Model Service Platform](https://www.wjark.com/)
- [ClawHub Skill Page](https://clawhub.ai/liangshenghzj888-stack/skills/wanjie-openclaw-video-v1-0-2)

## Skill Output:

**Output Type(s):** [Text, API Calls, Files]

**Output Format:** [Chat reply text with generated video result links recorded in local text files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a configured Wanjie API key and may open generated result URLs in the user's browser.]

## Skill Version(s):

1.0.0 (source: server evidence release.version and manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
