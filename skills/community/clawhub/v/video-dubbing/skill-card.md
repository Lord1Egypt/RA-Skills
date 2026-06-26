## Description: <br>
VoxCPM中文配音 converts foreign-language videos into Chinese-dubbed videos with Whisper transcription, API-backed translation, VoxCPM speech synthesis, subtitle handling, resumable processing, and optional background music. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[newaiguy](https://clawhub.ai/user/newaiguy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, localization teams, and developers use this skill to generate Chinese-dubbed versions of foreign-language videos, including translated narration, SRT subtitles, subtitle-cover handling, and optional background music mixing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Transcripts and selected video frames may be sent to configured third-party AI endpoints for translation and hard-subtitle detection. <br>
Mitigation: Use the skill only with media approved for those endpoints, configure trusted API URLs, and avoid processing confidential content unless the endpoint terms and controls are acceptable. <br>
Risk: The package includes a Bilibili upload script that can publish videos using session credentials from a hardcoded local credential path. <br>
Mitigation: Remove or ignore scripts/upload_bilibili.py unless publishing to Bilibili is intended, and do not place Bilibili credentials at the referenced path unless upload authority is explicitly approved. <br>
Risk: Generated dubbed audio, subtitles, and BGM mixing may change the meaning, attribution, or rights posture of source videos. <br>
Mitigation: Review the translated transcript, generated subtitles, source licensing, and platform publishing settings before distributing the output video. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/newaiguy/video-dubbing) <br>
- [VoxCPM](https://github.com/modelscope/VoxCPM) <br>
- [OpenAI Whisper](https://github.com/openai/whisper) <br>
- [Hunyuan-MT-7B](https://huggingface.co/tencent/Hunyuan-MT-7B) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON configuration, generated MP4 video files, and SRT subtitle files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Primary outputs are Chinese-dubbed video files and subtitle files under the configured workspace output directory; optional BGM mixing can produce an additional video file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter and manifest report 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
