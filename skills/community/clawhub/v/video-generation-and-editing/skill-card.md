## Description:

Helps video editors, post-production teams, advertisers, and creators generate or edit videos from text, images, video, or audio through AI Hive.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and production teams use this skill to submit AI Hive video generation, editing, extension, and media-reference workflows without writing API code. It is suited to advertising, e-commerce, TVC, product, social media, short drama, and comic-style video production.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Media and prompts may be sent to AI Hive during generation or editing.

Mitigation: Use only media and prompts that are acceptable to send to AI Hive, and review the service destination before use.

Risk: API keys could be exposed through unsafe handling or shared environments.

Mitigation: Keep the AI Hive API key secret, prefer environment variables or a protected config file, and use a dedicated virtual environment.

Risk: Custom base URLs and downloaded outputs may introduce trust and file-handling risk.

Mitigation: Avoid custom base URLs unless they are fully trusted, and inspect downloaded outputs because result URLs and remote-derived filenames are not strictly constrained.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/video-generation-and-editing)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive user and API key page](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands and downloaded video files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated tasks can return task IDs and may download MP4, MOV, or other formats supported by the selected AI Hive model.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
