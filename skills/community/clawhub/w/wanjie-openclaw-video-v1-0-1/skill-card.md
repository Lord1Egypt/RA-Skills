## Description:

Generates short videos from natural-language prompts through the Wanjie Ark Veo model service in OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liangshenghzj888-stack](https://clawhub.ai/user/liangshenghzj888-stack)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users and developers use this skill to trigger Veo video generation from chat prompts and retrieve generated video links without manually invoking command-line tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads a local OpenClaw model-provider configuration that contains API credentials.

Mitigation: Use a dedicated low-privilege API key and review credential access before installation.

Risk: The skill sends prompts and an API key to the Wanjie endpoint.

Mitigation: Avoid submitting sensitive prompts unless the Wanjie service is approved for the intended data.

Risk: The skill starts detached background work and may install dependencies at runtime.

Mitigation: Review background task and dependency behavior, including any scheduled monitor, before deployment.

Risk: The skill can automatically open provider-returned links.

Mitigation: Inspect generated result links and run the skill in an environment where automatic browser opening is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liangshenghzj888-stack/skills/wanjie-openclaw-video-v1-0-1)
- [Wanjie Ark model service](https://www.wjark.com/)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, API calls]

**Output Format:** [Markdown guidance and chat replies with local status/result files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces background video-generation requests, writes local log and result files, and may open provider-returned video links.]

## Skill Version(s):

1.0.0 (source: release evidence and manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
