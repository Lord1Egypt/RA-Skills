## Description: <br>
Processes local videos by extracting audio, transcribing speech, generating timestamped SRT/VTT subtitles, suggesting titles, and rendering subtitled video output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chall2015](https://clawhub.ai/user/chall2015) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, educators, and developers use this skill to create editable transcripts, subtitles, title suggestions, and subtitled videos from local recordings. It is suited to short-form media, course videos, interviews, meetings, and localization workflows where users can review and correct the generated text before publication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Media processing can expose private speech, audio, transcripts, subtitle files, and rendered videos. <br>
Mitigation: Use a private working directory, process only recordings the user is allowed to transcribe, and review or delete generated audio, transcript, subtitle, and video files when finished. <br>
Risk: Speech recognition and title suggestions may contain transcription errors or misleading wording. <br>
Mitigation: Install faster-whisper for real transcription when needed and review generated transcripts, subtitles, and titles before publishing. <br>
Risk: Untrusted subtitle style files or unusual filenames may interact poorly with FFmpeg filter escaping. <br>
Mitigation: Use trusted style JSON files and conservative filenames until FFmpeg filter escaping is hardened. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chall2015/video-processor) <br>
- [README](artifact/README.md) <br>
- [Post-processing guide](artifact/后处理使用指南.md) <br>
- [Subtitle post-processing full guide](artifact/字幕后处理完整指南.md) <br>
- [Model comparison test report](artifact/模型对比测试.md) <br>
- [Subtitle style template](artifact/subtitle_style_template.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with Python and shell command examples; generated local artifacts include transcripts, SRT/VTT subtitles, title text, JSON video metadata, and MP4 video output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local FFmpeg for media processing. Real transcription requires faster-whisper or OpenAI Whisper; otherwise the tool can fall back to simulated transcript output for testing.] <br>

## Skill Version(s): <br>
2.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
