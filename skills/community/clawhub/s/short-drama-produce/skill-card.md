## Description:

在创作者明确确认后，单条或按批调用已配置接口执行图片、视频、配音或配乐生成并保存产物与运行记录。用于“生成图/视频/配音/音乐”“开始跑图/跑视频”“把定稿提示词送去生成”；不写提示词、不改台词，不把预览或定稿当扣费确认。

This skill is ready for commercial/non-commercial use.

## Publisher:

[worldwonderer](https://clawhub.ai/user/worldwonderer)

### License/Terms of Use:

MIT

## Use Case:

Creators and production teams use this skill to submit approved image, video, voice, and music generation jobs to configured services, then save the media and run records in a short-drama project.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The supplied security review flags concerns about provider requests, prompts changing after finalization, and creator approval not being confirmed in some supplied execution paths; its analysis is incomplete.

Mitigation: Review the source and each complete job preview, then confirm the exact jobs before running them.

Risk: Credential handling and download redirects are identified as areas of concern when contacting generation providers.

Mitigation: Use trusted provider endpoints and reviewed adapters, and keep API keys in environment variables or a system credential store.

## Reference(s):

- [ClawHub release](https://clawhub.ai/worldwonderer/skills/short-drama-produce)
- [Generation interface protocol](references/adapter-contract.md)
- [Built-in provider guide](references/builtin-providers.md)
- [OpenAI image generation API](https://developers.openai.com/api/reference/resources/images/methods/generate)
- [Volcengine video generation API](https://www.volcengine.com/docs/82379/1520757)
- [MiniMax video generation API](https://platform.minimax.io/docs/api-reference/video-generation-v2-create)
- [MiniMax music generation API](https://platform.minimax.io/docs/api-reference/music-generation)
- [MiniMax speech synthesis API](https://platform.minimax.io/docs/api-reference/speech-t2a-http)

## Skill Output:

**Output Type(s):** [Image files, Video files, Audio files, Text previews, JSON run records]

**Output Format:** [PNG, JPEG, WebP, MP4, MP3 or WAV media, with JSON status and run records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs one job or a batch after creator confirmation; saves generated media and traceable run records.]

## Skill Version(s):

1.0.15 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
