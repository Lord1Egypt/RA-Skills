## Description:

Use PoYo AI Seedance 1.5 Pro for higher-end image-to-video generation through the PoYo generation endpoint, including 4s, 8s, or 12s clips, optional audio, fixed-lens control, broad aspect-ratio support, and PoYo payloads for seedance-1.5-pro.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to prepare, submit, and track PoYo Seedance video-generation jobs with authenticated JSON payloads. It is useful when an agent needs to choose model parameters, provide curl-based submission guidance, or report the returned task_id for follow-up polling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PoYo API credentials can be exposed if passed directly on the command line or stored in shell history.

Mitigation: Set POYO_API_KEY through a protected environment or secret mechanism and rotate the key if it may have been exposed.

Risk: Generation prompts, reference image URLs, and payload data are sent to PoYo.

Mitigation: Install and use the skill only when sending that data to PoYo is intended and acceptable for the use case.

## Reference(s):

- [Local API Reference](artifact/references/api.md)
- [PoYo Seedance 1.5 Pro Model Page](https://poyo.ai/models/seedance-1-5-pro)
- [PoYo Seedance 1.5 Pro API Docs](https://docs.poyo.ai/api-manual/video-series/seedance-1-5-pro)
- [PoYo Task Status Docs](https://docs.poyo.ai/api-manual/task-management/status)
- [PoYo Seedance 1.5 Pro OpenAPI JSON](https://docs.poyo.ai/api-manual/video-series/seedance-1-5-pro.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON payloads and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include the chosen model id, payload summary, reference image involvement, returned task_id, and polling or webhook next steps.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
