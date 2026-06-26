## Description: <br>
TencentCloud TTS converts text into MP3 or WAV speech files using Tencent Cloud Text-to-Speech with configurable voice and output settings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jizhouli](https://clawhub.ai/user/jizhouli) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent workflows use this skill to turn short text into local speech audio files through Tencent Cloud TTS. It also helps configure Tencent Cloud credentials, voice type, audio codec, and output file paths. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Tencent Cloud API credentials are required and could be exposed if placed in shared shells, logs, or source files. <br>
Mitigation: Use environment variables or a secret manager, scope the key to speech synthesis where possible, and rotate credentials if they may have been exposed. <br>
Risk: Text submitted for synthesis is sent to Tencent Cloud for processing. <br>
Mitigation: Do not submit confidential, regulated, or sensitive text unless Tencent Cloud processing is acceptable for the use case. <br>
Risk: Generated audio can overwrite an existing local file when an output path is reused. <br>
Mitigation: Choose explicit output filenames or directories that will not overwrite important files. <br>


## Reference(s): <br>
- [Tencent Cloud Text-to-Speech Documentation](https://cloud.tencent.com/document/product/1073) <br>
- [Tencent Cloud TTS API Error Codes](https://cloud.tencent.com/document/api/1073/37996) <br>
- [ClawHub Skill Page](https://clawhub.ai/jizhouli/tencentcloud-tts) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance, Python code examples, shell commands, JSON-style status dictionaries, and MP3 or WAV audio files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated audio is written to the requested output file path; text is sent to Tencent Cloud TTS for synthesis.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
