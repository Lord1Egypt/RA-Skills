## Description: <br>
Converts webpage content into a two-speaker Chinese podcast by extracting source material, drafting and checking dialogue, generating a structured TTS script, and producing final audio. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yangjinghua0127](https://clawhub.ai/user/yangjinghua0127) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn a webpage into a Chinese two-person podcast package, including a source brief, dialogue draft, structured TTS script, audio chunks, and a final MP3. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Podcast text is sent to the Volcano/ByteDance TTS service using the user's VOLC credentials. <br>
Mitigation: Use only content approved for that transfer, avoid confidential webpages unless the transfer is acceptable, and protect VOLC_APPID and VOLC_TOKEN. <br>
Risk: The skill clears skills/podcast-maker/workspace before each run. <br>
Mitigation: Keep important files outside that workspace and treat it as disposable output storage. <br>
Risk: Generated summaries, dialogue, and scripts may omit or distort source material. <br>
Mitigation: Review source_brief.json, podcast_content.md, and podcast_script.json before publishing or relying on the audio. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yangjinghua0127/url2podcast) <br>
- [Volcano/ByteDance TTS HTTP endpoint](https://openspeech.bytedance.com/api/v1/tts) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, audio files] <br>
**Output Format:** [Markdown guidance with JSON artifacts, shell commands, WAV chunks, and final MP3 audio.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ffmpeg, curl, python3, VOLC_APPID, and VOLC_TOKEN; writes outputs under skills/podcast-maker/workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
