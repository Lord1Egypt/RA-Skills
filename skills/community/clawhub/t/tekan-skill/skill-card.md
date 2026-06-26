## Description: <br>
特看视频 AI 创作工具 lets an agent generate and edit videos, images, digital-human videos, ecommerce assets, background removal outputs, and voice/TTS assets through Tekan scripts and APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tekancn](https://clawhub.ai/user/tekancn) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
External creators, marketers, ecommerce teams, and developers use this skill to create AI videos, images, product visuals, digital-human presentations, cloned or synthetic voices, and organized board outputs from natural-language requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores account credentials and requires OAuth-backed access to Tekan services. <br>
Mitigation: Install only when the publisher and Tekan/Topview are trusted, use trusted machines, and run logout or remove ~/.tekan/credentials.json on shared machines. <br>
Risk: The skill can upload personal media, product assets, faces, voices, and other user files for remote processing. <br>
Mitigation: Explicitly confirm uploads before execution, avoid confidential assets unless remote processing is acceptable, and do not submit third-party faces or voices without consent. <br>
Risk: The skill can spend account credits and perform sensitive creative actions such as voice cloning, watermark removal, webhook use, and deletion. <br>
Mitigation: Confirm paid generation jobs, voice cloning, watermark removal, webhook URLs, and deletion actions before running the corresponding scripts. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/tekancn/tekan-skill) <br>
- [Tekan website](https://tekan.cn) <br>
- [README](artifact/README.md) <br>
- [Authentication reference](artifact/references/auth.md) <br>
- [Video generation reference](artifact/references/video_gen.md) <br>
- [AI image reference](artifact/references/ai_image.md) <br>
- [Ecommerce image reference](artifact/references/ecommerce_image.md) <br>
- [Digital human reference](artifact/references/avatar4.md) <br>
- [Voice reference](artifact/references/voice.md) <br>
- [Text-to-voice reference](artifact/references/text2voice.md) <br>
- [Board reference](artifact/references/board.md) <br>
- [User account reference](artifact/references/user.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, API calls, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON-like task results, and links to generated media or board items] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated media is produced through remote Tekan services and may require OAuth login, account credits, and uploaded user files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
