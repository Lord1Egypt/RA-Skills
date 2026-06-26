## Description: <br>
Transcribes Xiaoyuzhou podcast episodes to text by using a compatible xyz API service for episode metadata and audio URLs, then running local Qwen3-ASR speech recognition. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[worldwonderer](https://clawhub.ai/user/worldwonderer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to search, fetch, download, and transcribe Xiaoyuzhou podcast episodes locally into transcript files. It is suited for single-episode transcription, podcast discovery, recent-episode listing, and batch transcription workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles reusable Xiaoyuzhou account tokens through a configurable xyz API service and stores them locally. <br>
Mitigation: Use a trusted xyz API service, preferably on localhost, and protect or delete ~/.xiaoyuzhou-asr.json when finished. <br>
Risk: Pointing XYZ_BASE_URL at an untrusted server may expose a phone number, SMS code, access token, or refresh token. <br>
Mitigation: Verify XYZ_BASE_URL before login or transcription and do not use third-party xyz servers unless they are trusted with these credentials. <br>
Risk: The ASR binary path is configurable and could run an unintended local binary. <br>
Mitigation: Verify the QWEN3_ASR_BIN or detected local_transcribe path before running transcription. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/worldwonderer/xiaoyuzhou-asr) <br>
- [xyz API reference](references/xyz-api.md) <br>
- [Qwen3-ASR reference](references/qwen3-asr.md) <br>
- [ultrazg/xyz](https://github.com/ultrazg/xyz) <br>
- [Qwen3-ASR-0.6B model](https://huggingface.co/Qwen/Qwen3-ASR-0.6B) <br>
- [qwen3-asr-rs](https://github.com/alan890104/qwen3-asr-rs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, plain text, SRT subtitles, JSON transcript metadata, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write one transcript file per episode and supports checkpoint/resume for batch output.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and CHANGELOG, released 2026-05-05) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
