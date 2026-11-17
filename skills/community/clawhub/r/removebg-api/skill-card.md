## Description:

Remove image backgrounds using the remove.bg API with API-key auth and transparent PNG output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rolandkakonyi](https://clawhub.ai/user/rolandkakonyi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operators use this skill to send selected workspace images to remove.bg and save background-removed outputs for agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected workspace images are sent to the remove.bg service for cloud processing.

Mitigation: Install and use the skill only when cloud processing of those images is acceptable.

Risk: remove.bg API use can consume free credits or paid quota.

Mitigation: Configure and monitor REMOVE_BG_API_KEY usage according to the account holder's remove.bg plan.

Risk: Unexpected input or output paths can cause failed runs or misplaced outputs.

Mitigation: Use image inputs inside the OpenClaw workspace and output paths under outputs/removebg-api/.

## Reference(s):

- [removebg-api on ClawHub](https://clawhub.ai/rolandkakonyi/skills/removebg-api)
- [Publisher profile](https://clawhub.ai/user/rolandkakonyi)
- [remove.bg API key dashboard](https://www.remove.bg/dashboard#api-key)
- [remove.bg API endpoint](https://api.remove.bg/v1.0/removebg)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files]

**Output Format:** [Transparent image file with terminal status text and MEDIA line]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires REMOVE_BG_API_KEY; writes outputs under outputs/removebg-api/.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
