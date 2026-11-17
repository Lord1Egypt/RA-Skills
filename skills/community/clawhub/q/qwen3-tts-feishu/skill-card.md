## Description:

Generates local speech audio with Qwen3-TTS and can send the resulting voice message through Feishu as an audio bubble.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shawnreality](https://clawhub.ai/user/shawnreality)

### License/Terms of Use:


## Use Case:

Developers and automation users use this skill to synthesize multilingual speech locally, save WAV output, convert it to Opus, and send it to Feishu recipients with a self-managed Feishu app.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Feishu helper script has unsafe WAV filename handling that can execute attacker-controlled Python while Feishu credentials are available.

Mitigation: Patch scripts/send_voice_feishu.sh before running it, use only trusted WAV paths in a trusted workspace, and provide Feishu credentials only for the send operation.

Risk: Synthesized audio may be uploaded to Feishu and delivered to the configured recipient.

Mitigation: Do not synthesize or send sensitive text unless that upload and delivery path is acceptable.

Risk: Unpinned dependencies can change behavior across installations.

Mitigation: Pin Python dependencies and review resolved packages before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/shawnreality/skills/qwen3-tts-feishu)
- [Feishu Tenant Access Token Endpoint](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal)
- [Feishu File Upload Endpoint](https://open.feishu.cn/open-apis/im/v1/files)
- [Feishu Message Send Endpoint](https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with Python and bash examples; scripts produce WAV and Opus audio files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local Qwen3-TTS model files, Python dependencies, ffmpeg or sox, and Feishu app credentials for message sending.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
