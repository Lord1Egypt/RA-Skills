## Description:

在创作者明确确认后，单条或按批次执行短剧项目的图片、视频、TTS/配音或成片配乐生成任务，并把产出文件与运行记录存回项目。用户说“生成这张图/这段视频/这句配音/这段配乐”“开始跑图/跑视频/合成语音/生成音乐”“把定稿提示词送去生成”，或要求批量执行已确认媒体任务时使用；不负责编写提示词、拆镜头、改台词、写歌词或定角色音色设定，也绝不把预览、继续、预算说明或之前的定稿状态当作本次调用付费接口的确认。

This skill is ready for commercial/non-commercial use.

## Publisher:

[worldwonderer](https://clawhub.ai/user/worldwonderer)

### License/Terms of Use:

MIT

## Use Case:

短剧创作者使用此技能，在逐条或批次预览并明确确认后，调用已配置的媒体生成服务制作图片、视频、配音或音乐，并将成品与运行记录保存到项目中。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated requests may expose credentials through redirects.

Mitigation: Review provider endpoints and redirect handling, and keep credentials in environment variables or a system credential store.

Risk: Paid generation may run without confirmed current consent.

Mitigation: Require the creator to review the current single-task or batch preview and explicitly confirm before dispatch.

Risk: Generated files may be downloaded to an unintended destination.

Mitigation: Review configured output paths and verify that downloads are saved to the intended project locations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/worldwonderer/skills/short-drama-produce)
- [Generation adapter contract](artifact/references/adapter-contract.md)
- [Built-in generation providers](artifact/references/builtin-providers.md)
- [GPT Image 2 model documentation](https://developers.openai.com/api/docs/models/gpt-image-2)
- [OpenAI image generation API](https://developers.openai.com/api/reference/resources/images/methods/generate)
- [OpenAI image editing API](https://developers.openai.com/api/reference/resources/images/methods/edit)
- [Volcengine video generation API](https://www.volcengine.com/docs/82379/1520757)
- [MiniMax video generation API](https://platform.minimax.io/docs/api-reference/video-generation-v2-create)
- [MiniMax music generation API](https://platform.minimax.io/docs/api-reference/music-generation)
- [MiniMax speech synthesis API](https://platform.minimax.io/docs/api-reference/speech-t2a-http)

## Skill Output:

**Output Type(s):** [Files]

**Output Format:** [Generated image, video, voice, and music files, with project run records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are saved to project paths; generation uses configured providers and requires explicit creator confirmation.]

## Skill Version(s):

1.0.9 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
