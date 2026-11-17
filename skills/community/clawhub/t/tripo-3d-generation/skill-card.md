## Description:

Generate 3D models from text or images, including characters, objects, scenes, game assets, e-commerce products, architecture models, 3D printing files, rigged characters, animations, stylized models, and exports to GLB, FBX, OBJ, STL, USDZ, and 3MF.

This skill is ready for commercial/non-commercial use.

## Publisher:

[meterlong](https://clawhub.ai/user/meterlong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and creators use this skill to request text-to-3D or image-to-3D generation, poll task status, retrieve model download links, and perform post-processing such as rigging, animation, stylization, texture generation, and format conversion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: 3D prompts, image URLs, task IDs, and uploaded file URLs are sent to Tripo or, for free-tier use, to the operator proxy.

Mitigation: Do not submit sensitive prompts or private asset URLs; use TRIPO_API_KEY when direct routing to Tripo is preferred over the free-tier proxy.

Risk: Free-tier use relies on a local anonymous identifier stored at ~/.tripo-skill-id when possible.

Mitigation: Delete ~/.tripo-skill-id to reset the local free-tier identifier, or use TRIPO_API_KEY for account-based usage.

Risk: Generated or converted 3D assets may require review before production, printing, game-engine import, or animation use.

Mitigation: Inspect mesh quality, scale, file format, rigging, and animation results before using generated assets in downstream workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/meterlong/skills/tripo-3d-generation)
- [Publisher profile](https://clawhub.ai/user/meterlong)
- [Tripo website](https://www.tripo3d.ai/)
- [Tripo API platform](https://platform.tripo3d.ai/)
- [Tripo API documentation](https://platform.tripo3d.ai/docs/generation)
- [Tripo API keys](https://platform.tripo3d.ai/api-keys)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with JSON-like task results, status fields, model download URLs, and inline shell configuration commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return task IDs, generation status, progress, credit information, Tripo model URLs, rendered image URLs, and setup guidance for TRIPO_API_KEY or TRIPO_PROXY_SECRET.]

## Skill Version(s):

2.0.5 (source: server release metadata and manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
