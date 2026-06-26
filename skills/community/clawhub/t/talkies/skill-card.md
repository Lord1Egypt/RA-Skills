## Description: <br>
Self-hosted OpenAI-compatible speech service for transcription, subtitles, text-to-speech, stereo diarization, URL-based audio fetching, and optional voice cloning against a user-run talkies server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[psyb0t](https://clawhub.ai/user/psyb0t) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure and call a self-hosted talkies speech service for ASR, SRT/VTT subtitle generation, TTS, stereo-channel diarization, and OpenAI-compatible audio endpoint migration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends uploaded audio, URL-fetched media, transcripts, and custom voice clips to a self-hosted service that may store staged files. <br>
Mitigation: Use only a trusted talkies server, protect it with TALKIES_AUTH_TOKEN and TLS or localhost binding, and delete staged files and custom voices when they are no longer needed. <br>
Risk: URL-based audio fetching can expose the service to untrusted network targets when clients provide arbitrary file_path URLs. <br>
Mitigation: Enable TALKIES_BLOCK_PRIVATE_DOWNLOADS for untrusted clients and keep download size limits appropriate for the deployment. <br>
Risk: Voice cloning can reproduce a speaker from a reference clip without adequate permission. <br>
Mitigation: Use Qwen3-TTS voice cloning only with clear authorization from the speaker and in compliance with applicable policy and law. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/psyb0t/talkies) <br>
- [Setup Reference](references/setup.md) <br>
- [Model Context Protocol](https://modelcontextprotocol.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, curl examples, JSON snippets, and generated transcript or audio file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs depend on a reachable TALKIES_URL server and optional TALKIES_AUTH_TOKEN bearer credential.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
