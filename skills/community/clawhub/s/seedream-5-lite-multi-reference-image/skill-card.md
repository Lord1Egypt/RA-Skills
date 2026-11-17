## Description:

Uses Seedream 5.0 Lite through AI Hive to generate images from two or more approved reference images while tracking which source contributes each identity, object, structure, material, composition, and palette.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, designers, marketers, and developers use this skill to build multi-reference Seedream 5.0 Lite image-generation prompts with explicit source lineage for approved people, products, environments, materials, layouts, and campaign visuals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected reference images and prompts are sent to AI Hive for generation.

Mitigation: Use only images and prompts that are approved for AI Hive processing, and avoid submitting confidential, unauthorized, or sensitive material.

Risk: The helper stores or reads an AI Hive API key on the local system.

Mitigation: Prefer environment-scoped credentials or the generated config file with restricted permissions, and rotate the key if it is exposed.

Risk: Generation results are downloaded from API-provided URLs and written under the user's account.

Mitigation: Run the skill from a constrained directory or container and review downloaded outputs until result-host validation and filename sanitization are confirmed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/seedream-5-lite-multi-reference-image)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key setup page](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with bash commands; the helper can submit AI Hive image-generation tasks and download image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an AI_HIVE_API_KEY or local AI Hive config file; generated outputs are written under the user's account, defaulting to ~/Downloads/AiHive unless changed.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
