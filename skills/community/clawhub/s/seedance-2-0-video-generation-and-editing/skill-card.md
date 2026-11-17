## Description:

Helps creators generate Seedance2.0 videos from text or reference images, video, or audio through AI Hive, with task submission, polling, and result download support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, video editors, post-production teams, advertising teams, e-commerce operators, and developers use this skill to produce videos for ads, product displays, social commerce, short dramas, and social media. It helps an agent configure AI Hive access, select Seedance2.0 text-to-video, image-to-video, or reference-to-video modes, submit jobs, query task status, and download generated media.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and uploaded media are sent to AI Hive during generation.

Mitigation: Use only media and prompts approved for processing by AI Hive.

Risk: Custom API base URLs can expose API keys or media to an untrusted endpoint.

Mitigation: Use the default AI Hive endpoint unless the alternative endpoint is fully trusted; rotate the API key if endpoint configuration may have changed.

Risk: Hostile API responses could overwrite user-writable files through result download handling.

Mitigation: Use a dedicated output directory and review downloaded files until path handling is fixed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wubin1836/skills/seedance-2-0-video-generation-and-editing)
- [AI Hive Console](https://ai-hive.iclip.cn/chat)
- [AI Hive API Base URL](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, task status, files]

**Output Format:** [Markdown guidance with inline bash commands, JSON task responses, and downloaded media files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write API configuration to the user's AI Hive config file during initialization and may download generated MP4, MOV, PNG, or model-supported media files to the selected output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact CHANGELOG top entry is 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
