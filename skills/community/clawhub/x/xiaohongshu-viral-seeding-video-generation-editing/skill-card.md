## Description:

Generates and edits Xiaohongshu/RED product seeding, unboxing, review, and brand collaboration videos from prompts, product images, reference videos, or existing footage through AI Hive.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and developers use this skill to turn product facts, media assets, and campaign goals into Xiaohongshu-style video generation workflows while preserving product accuracy and avoiding unsupported claims.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send the user's AI Hive API key to a configurable server.

Mitigation: Keep the default AI Hive endpoint unless a custom endpoint is fully trusted, inspect ~/.ai-hive/config.json, and rotate the key if it may have been used with an untrusted base URL.

Risk: Downloaded outputs may be written using unsafe filenames.

Mitigation: Use a dedicated empty output directory or --no-download until filename containment is fixed.

Risk: Installing and running the helper script introduces dependency and execution risk.

Mitigation: Review the skill before installing and run it in a virtual environment with pinned dependencies.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/xiaohongshu-viral-seeding-video-generation-editing)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API access page](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with bash commands; CLI task output is JSON and generated video downloads are MP4 files unless --no-download is used.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses an AI Hive API key, optional media uploads, configurable routing, and a configurable output directory.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
