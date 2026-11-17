## Description:

Tripo3D helps agents generate 3D models from text prompts, images, or multiview image sets through the Tripo3D API, including refinement, polling, and download workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[richardcoder849](https://clawhub.ai/user/richardcoder849)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to prepare Tripo3D API calls for text-to-3D, image-to-3D, multiview generation, model refinement, polling, and asset download workflows. It is intended for agents helping users create 3D models through the Tripo3D third-party service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and uploaded images are sent to Tripo3D as a third-party generation service.

Mitigation: Use only prompts and image files approved for Tripo3D, and confirm the exact upload inputs before running image or multiview workflows.

Risk: The workflow uses TRIPO3D_API_KEY and downloads generated assets from short-lived URLs.

Mitigation: Keep the API key in an environment variable, avoid exposing it in chat or files, and confirm the intended download destination before fetching model files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/richardcoder849/skills/tripo3d)
- [Tripo3D platform](https://platform.tripo3d.ai)
- [Tripo3D OpenAPI base URL](https://api.tripo3d.ai/v2/openapi)
- [Tripo3D Studio](https://studio.tripo3d.ai/?from=landingpage_header&category=featured&model_type=all&recommended=recommended&use_case=all)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON and PowerShell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe API calls, polling steps, task IDs, model download steps, and Tripo3D configuration requirements.]

## Skill Version(s):

1.0.1 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
