## Description:

Generate publication-ready scientific figures with the official SciDraw AI web app and public API for paper figures, graphical abstracts, mechanism diagrams, research workflows, and model architectures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[toplocalai](https://clawhub.ai/user/toplocalai)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, authors, educators, and technical teams use this skill to plan, generate, inspect, and iterate scientific figure images through SciDraw AI for publications, reports, grants, workflows, mechanisms, and model architecture diagrams.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and credentials may be sent to an arbitrary HTTP(S) endpoint if SCIDRAW_API_BASE_URL is configured.

Mitigation: Use the default SciDraw AI API base URL unless there is a trusted operational reason to override it, and rotate the API key after any untrusted or HTTP endpoint exposure.

Risk: Scientific prompts may contain confidential, regulated, unpublished, or otherwise sensitive research details.

Mitigation: Review prompts before generation and omit sensitive material unless SciDraw processing is acceptable for the data involved.

Risk: API generation can consume SciDraw AI account credits.

Mitigation: Confirm the resolution and image count with the user before starting a generation request.

## Reference(s):

- [SciDraw AI drawing homepage](https://sci-draw.com/ai-drawing)
- [SciDraw AI API documentation](https://sci-draw.com/docs/api)
- [SciDraw AI OpenAPI specification](https://sci-draw.com/api/openapi.yaml)
- [SciDraw AI API keys](https://sci-draw.com/settings/api-keys)
- [ClawHub skill page](https://clawhub.ai/toplocalai/skills/scidraw-ai-scientific-illustration)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code, Files]

**Output Format:** [Markdown guidance with shell commands and generated image file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call the SciDraw AI API when SCIDRAW_API_KEY is configured and user confirmation is obtained for credit-consuming generation.]

## Skill Version(s):

1.0.1 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
