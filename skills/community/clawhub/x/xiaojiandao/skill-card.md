## Description: <br>
小剪刀AI视频剪辑skill。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guyuxiu](https://clawhub.ai/user/guyuxiu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and creators use this skill to upload video to Xiao Jian Dao/Cutflow services, analyze editing needs, generate AI clips or narration, choose voice and background music, synthesize TTS, and compose a finished video with step-by-step user confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send user videos, derived frames, audio, OCR text, prompts, device metadata, and signed media links to Xiao Jian Dao/Cutflow services. <br>
Mitigation: Confirm with the user before uploads or task creation, avoid sensitive media unless the user accepts that processing, and treat returned signed URLs as private. <br>
Risk: The skill asks for Xiao Jian Dao tokens and supports entering tokens in chat. <br>
Mitigation: Do not paste tokens into chat; use a secure secret store or environment variable such as XJD_TOKEN when possible. <br>
Risk: Video processing task creation may consume credits or account balance. <br>
Mitigation: Confirm before credit-consuming task creation and stop on insufficient balance or authorization errors. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/guyuxiu/xiaojiandao) <br>
- [认证与加密协议](references/00-auth.md) <br>
- [任务管理](references/01-task.md) <br>
- [需求分析](references/02-analysis.md) <br>
- [AI智能剪辑的前置结果](references/03-clipping.md) <br>
- [AI解说脚本生成](references/04-narration.md) <br>
- [音色推荐与BGM推荐](references/05-voice-bgm.md) <br>
- [字幕识别与字幕位置计算](references/06-subtitle-ocr.md) <br>
- [字幕TTS生成](references/07-tts.md) <br>
- [异步任务轮询](references/08-task-status.md) <br>
- [错误码](references/09-error-codes.md) <br>
- [视频最终合成接口文档](references/10-compose.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON snippets, API call parameters, and signed media links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces stepwise user-facing confirmations, task IDs, analysis summaries, narration text, TTS/audio selections, progress updates, and final video URLs.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
