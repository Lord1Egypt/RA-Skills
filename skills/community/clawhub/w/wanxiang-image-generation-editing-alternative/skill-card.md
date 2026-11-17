## Description:

Helps agents migrate Chinese commercial image generation and editing workflows from Wanxiang or Alibaba Cloud image-generation searches to AI Hive Nano Banana Pro while preserving prompt intent, reference-image roles, product facts, and channel delivery requirements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate Chinese commercial image briefs, AI Hive CLI commands, and review criteria for product visuals, ecommerce scenes, campaign poster backgrounds, multi-reference image tasks, and channel-specific image variants.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Downloaded result metadata could cause files to be written outside the intended output folder.

Mitigation: Run the skill in a contained workspace with a dedicated output directory, and review downloaded file paths before using the results.

Risk: Prompts, selected reference images, and the configured API key are sent to or stored for AI Hive use.

Mitigation: Use only approved inputs, avoid sensitive reference images, and configure a dedicated AI Hive API key with local file permissions restricted to the current user.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/wubin1836/skills/wanxiang-image-generation-editing-alternative)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key setup page](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with inline bash commands and downloaded image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses an AI Hive API key, accepts optional local reference images, submits Nano Banana Pro image tasks, polls task status, and downloads generated results to a local output directory.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
