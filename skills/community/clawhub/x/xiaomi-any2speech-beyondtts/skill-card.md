## Description: <br>
Xiaomi-any2speech guides an agent to call Xiaomi's public speech API to turn text, URLs, files, or reference voice samples into long-form, multi-speaker bilingual WAV speech for TTS, voice cloning, podcasts, audiobooks, rap, news, and radio-drama styles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whiteshirt0429](https://clawhub.ai/user/whiteshirt0429) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and end users use this skill to generate spoken audio from supplied text, web pages, documents, or voice prompts, choosing styles such as narration, podcasts, audiobooks, debates, rap, and radio drama. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected text, files, URLs, and reference voice recordings may be uploaded to Xiaomi's public API. <br>
Mitigation: Use only content and voice samples you have permission to send to the third-party service, and avoid private documents or sensitive recordings. <br>
Risk: Generated audio may be sent to Feishu when that optional delivery path is requested. <br>
Mitigation: Enable Feishu delivery only after an explicit user request and confirm the target chat and credentials before sending. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/whiteshirt0429/xiaomi-any2speech-beyondtts) <br>
- [Publisher Profile](https://clawhub.ai/user/whiteshirt0429) <br>
- [Xiaomi Public Speech API](https://miplus-tts-public.ai.xiaomi.com) <br>
- [Feishu OpenAPI Tenant Token Endpoint](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal) <br>
- [Feishu OpenAPI File Upload Endpoint](https://open.feishu.cn/open-apis/im/v1/files) <br>
- [Feishu OpenAPI Message Endpoint](https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands that create WAV audio files and optionally send audio through Feishu] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local WAV files; optional Feishu delivery requires user request and Feishu credentials.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
