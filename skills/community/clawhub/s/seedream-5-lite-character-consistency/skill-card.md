## Description:

Guides agents to create a character continuity bible and shot-specific change orders for Seedream 5.0 Lite image generation with authorized character reference images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and content teams use this skill to keep a recurring character, mascot, virtual persona, comic character, or branded IP visually consistent across poses, expressions, outfits, scenes, and channel variants.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reference images and prompts are uploaded to AI Hive for image generation.

Mitigation: Install only if you trust AI Hive with those inputs, and use only authorized reference images and approved prompts.

Risk: The helper requires an AI Hive API key that may be provided through an environment variable, command argument, or local config file.

Mitigation: Prefer an environment variable or verify that ~/.ai-hive/config.json is permission-restricted before storing credentials there.

Risk: Generated images may still drift from the approved identity, proportions, clothing, or brand boundaries.

Mitigation: Review generated outputs against the continuity bible and shot change order before release.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/seedream-5-lite-character-consistency)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key setup](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with bash command examples and JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated image files are saved locally by the helper script, typically under ~/Downloads/AiHive unless the user chooses another output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
