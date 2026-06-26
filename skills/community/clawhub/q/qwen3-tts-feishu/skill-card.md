## Description: <br>
Qwen3-TTS + Feishu Voice converts text into local speech audio with Qwen3-TTS and can send the result as a Feishu voice message. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shawnreality](https://clawhub.ai/user/shawnreality) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users can use this skill to synthesize multilingual speech locally, save it as an audio file, and optionally deliver it to a Feishu recipient after configuring the required app credentials and audio tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Feishu sending script has unsafe filename handling that could run local code when given a crafted audio filename. <br>
Mitigation: Review the script before use, avoid filenames from untrusted sources, and quote or sanitize filename handling before using it in shared or production workflows. <br>
Risk: The skill uses FEISHU_APP_SECRET to obtain Feishu tenant access tokens. <br>
Mitigation: Store Feishu credentials in environment variables or a secret manager, avoid committing them to files, and limit access to the Feishu app credentials. <br>
Risk: Generated audio may be sent to Feishu recipients through the configured bot. <br>
Mitigation: Send only audio that is appropriate for Feishu and confirm the intended recipient open_id before delivery. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shawnreality/qwen3-tts-feishu) <br>
- [Feishu tenant access token API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal) <br>
- [Feishu file upload API](https://open.feishu.cn/open-apis/im/v1/files) <br>
- [Feishu message send API](https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with Python and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, ffmpeg, sox, FEISHU_APP_ID, and FEISHU_APP_SECRET; supports macOS and Linux.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
