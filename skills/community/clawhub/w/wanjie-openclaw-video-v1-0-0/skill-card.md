## Description:

Generates Veo videos from natural-language prompts through Wanjie Ark for OpenClaw and records the resulting link workflow in local text files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liangshenghzj888-stack](https://clawhub.ai/user/liangshenghzj888-stack)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use this skill to trigger short Veo video-generation jobs from chat prompts and monitor the generated result link through the skill's background workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically reads a local OpenClaw API key and sends it to a hard-coded external service.

Mitigation: Use only a dedicated, low-quota Wanjie API key and avoid keeping unrelated provider keys as the first OpenClaw provider entry.

Risk: The skill can make network calls and open returned URLs without an explicit user confirmation step.

Mitigation: Require explicit confirmation before generation requests and before opening returned URLs.

Risk: The skill can install the requests dependency automatically at runtime.

Mitigation: Pin dependencies and install them in a controlled environment before deployment.

Risk: The artifact describes background monitoring behavior and Windows Task Scheduler usage that may continue outside a single chat turn.

Mitigation: Document and review how to disable background monitoring before installation or use.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/liangshenghzj888-stack/skills/wanjie-openclaw-video-v1-0-0)
- [Wanjie Ark model service platform](https://www.wjark.com/)

## Skill Output:

**Output Type(s):** [text, files]

**Output Format:** [Plain text status messages plus local text result and log files containing success, failure, and returned URL details.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill starts a background worker, writes result state to veo_result.txt, and may open a returned URL in the user's browser.]

## Skill Version(s):

1.0.0 (source: server release metadata and manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
