## Description: <br>
TencentCloud ASR helps agents transcribe local audio files or public audio URLs with Tencent Cloud speech recognition, including short sentence recognition, fast medium-length transcription, and asynchronous long-recording transcription. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Stardusten](https://clawhub.ai/user/Stardusten) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can use this skill to route audio transcription requests through Tencent Cloud ASR, inspect audio, configure credentials, and integrate a CLI transcription backend with host systems such as OpenClaw. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use Tencent Cloud credentials, read local audio, and send audio or transcripts to Tencent Cloud. <br>
Mitigation: Use least-privilege Tencent credentials, avoid processing sensitive recordings without consent, and prefer manual credential setup over sharing secrets through an agent conversation. <br>
Risk: The skill may attempt automatic Python or system dependency installation for transcription support. <br>
Mitigation: Preinstall dependencies manually where possible and avoid granting sudo or package-manager authority unless the installation path has been reviewed. <br>
Risk: Server security evidence says the QQ Bot workaround should be transparently disclosed. <br>
Mitigation: Require clear disclosure when the QQ Bot workaround is used and review that behavior before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Stardusten/tencentcloud-asr) <br>
- [CLI transcription backend](references/cli_transcription_backend.md) <br>
- [Tencent Cloud ASR environment configuration](references/env_config.md) <br>
- [FFmpeg installation guidance](references/ffmpeg_guide.md) <br>
- [Audio routing and large-file strategy](references/routing_strategy.md) <br>
- [Tencent Cloud ASR self-check](references/self_check.md) <br>
- [Tencent Cloud ASR activation and credential setup](references/tencent_cloud_activation.md) <br>
- [Tencent Cloud sentence recognition API](https://cloud.tencent.com/document/product/1093/35646) <br>
- [Tencent Cloud flash recognition API](https://cloud.tencent.com/document/product/1093/52097) <br>
- [Tencent Cloud file recognition API](https://cloud.tencent.com/document/product/1093/37823) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; scripts emit plain-text transcripts or JSON status and result objects.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read local audio or public audio URLs, call Tencent Cloud ASR, and print transcripts or diagnostics.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
