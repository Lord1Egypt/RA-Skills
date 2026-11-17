## Description:

小剪刀视频剪辑 guides an agent through a user-confirmed workflow for uploading media, analyzing editing needs, generating clips or narration, selecting voice and BGM, running TTS, and composing the final video.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guyuxiu](https://clawhub.ai/user/guyuxiu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and media creators use this skill to turn uploaded videos into edited clips or narrated videos through a step-by-step confirmation workflow. The agent coordinates cloud media upload, task creation, analysis, clipping, OCR, TTS, BGM selection, and final composition.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User tokens may be exposed if pasted into chat or command lines.

Mitigation: Use a scoped, revocable token through a secure secret mechanism when available, and rotate tokens after use.

Risk: The workflow can upload overly broad local files to external cloud services.

Mitigation: Stage only the intended media in a dedicated folder and avoid providing arbitrary local paths.

Risk: Uploaded media is sent to the listed cloud video, OCR, ASR, TTS, and composition services.

Mitigation: Use this skill only with media approved for those services and confirm each upload or composition step before execution.

## Reference(s):

- [认证与加密协议](references/00-auth.md)
- [任务管理](references/01-task.md)
- [需求分析](references/02-analysis.md)
- [AI智能剪辑的前置结果](references/03-clipping.md)
- [AI解说脚本生成](references/04-narration.md)
- [音色推荐与BGM推荐](references/05-voice-bgm.md)
- [字幕识别与字幕位置计算](references/06-subtitle-ocr.md)
- [字幕TTS生成](references/07-tts.md)
- [异步任务轮询](references/08-task-status.md)
- [错误码](references/09-error-codes.md)
- [视频最终合成接口文档](references/10-compose.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API calls, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands, JSON snippets, task data, and generated media URLs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include signed media URLs, task IDs, SRT text, subtitle mask coordinates, audio ZIP links, and final video or draft URLs.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
