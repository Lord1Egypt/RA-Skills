## Description:

Z Image helps agents submit prompt-based image generation jobs to PoYo AI's Z-Image endpoint with simple model, prompt, and size parameters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to prepare and submit PoYo Z-Image text-to-image jobs, including prompt, model, aspect ratio, authentication, and follow-up status handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image prompts and payload data are sent to PoYo's external API.

Mitigation: Submit only prompts and payload data appropriate for PoYo processing and the user's data-handling requirements.

Risk: API keys can be exposed if passed directly on the command line or stored in unprotected files.

Mitigation: Set POYO_API_KEY through a protected environment or secret manager and avoid passing real API keys as command-line arguments.

Risk: Webhook callbacks can leak task results or metadata if pointed at an endpoint the user does not control.

Mitigation: Use callback_url only with HTTPS endpoints controlled by the user, or rely on authenticated status polling instead.

## Reference(s):

- [PoYo Z Image API Reference](references/api.md)
- [PoYo Z-Image Model Page](https://poyo.ai/models/z-image)
- [PoYo Z-Image API Docs](https://docs.poyo.ai/api-manual/image-series/z-image)
- [PoYo Z-Image OpenAPI JSON](https://docs.poyo.ai/api-manual/image-series/z-image.json)
- [PoYo Task Status Docs](https://docs.poyo.ai/api-manual/task-management/status)
- [PoYo API Key Dashboard](https://poyo.ai/dashboard/api-key)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON payloads and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include the chosen model id, payload summary, reference-image status, returned task_id, and next polling or webhook step.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
