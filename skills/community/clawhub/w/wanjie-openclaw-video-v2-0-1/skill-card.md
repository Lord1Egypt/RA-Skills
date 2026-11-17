## Description:

Generates videos from natural-language prompts in OpenClaw by submitting Veo requests to the Wanjie Ark model service and returning the resulting video link.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liangshenghzj888-stack](https://clawhub.ai/user/liangshenghzj888-stack)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use this skill to submit Chinese natural-language video prompts to a Wanjie Ark Veo model workflow and receive the generated video link through the agent experience.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads an OpenClaw provider API key and sends prompts with that credential to the Wanjie endpoint.

Mitigation: Use a dedicated skill-scoped credential where possible, limit credential permissions, and avoid prompts containing sensitive data.

Risk: Prompt-bearing logs and result files may be written locally.

Mitigation: Review log locations, redact or delete sensitive task logs, and document retention expectations before shared or managed deployments.

Risk: The artifact can install Python dependencies at runtime and run background workers or scheduled monitoring.

Mitigation: Pin and preinstall dependencies, review background execution settings, and provide an operational path to disable monitoring.

Risk: Returned video links may be opened automatically.

Mitigation: Validate returned URLs before opening them automatically, or require manual review in higher-risk environments.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/liangshenghzj888-stack/skills/wanjie-openclaw-video-v2-0-1)
- [Wanjie Ark model service](https://www.wjark.com/)

## Skill Output:

**Output Type(s):** [Text, Files]

**Output Format:** [Plain text status messages and URL-bearing result files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May run video generation in the background, write local logs/results, and open returned video links automatically.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
