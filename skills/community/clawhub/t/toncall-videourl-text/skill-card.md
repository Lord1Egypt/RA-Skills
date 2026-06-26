## Description: <br>
Transcribes speech from an accessible video URL by downloading the video, extracting audio with ffmpeg, uploading the audio to Volcengine TOS, calling Volcengine speech recognition, saving transcript text, and cleaning temporary files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[juysoft](https://clawhub.ai/user/juysoft) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn directly accessible video-file URLs into transcript text. It is intended for workflows where sending extracted audio to Volcengine services and storing transcript text locally are acceptable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Extracted audio from submitted videos is uploaded to Volcengine services for storage and speech recognition. <br>
Mitigation: Use the skill only for videos whose audio may be sent to those services, and avoid private, regulated, copyrighted, or very large videos unless that data flow is acceptable. <br>
Risk: Cloud credentials and speech recognition credentials are required in a local config.ini file. <br>
Mitigation: Keep config.ini private, use dedicated least-privilege TOS buckets and API keys, and rotate credentials if they are exposed. <br>
Risk: Transcript text is saved on disk after processing. <br>
Mitigation: Review local transcript retention for the environment and remove generated text files when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/juysoft/toncall-videourl-text) <br>
- [ffmpeg downloads](https://ffmpeg.org/download.html) <br>
- [Volcengine ASR submit endpoint](https://openspeech.bytedance.com/api/v3/auc/bigmodel/submit) <br>
- [Volcengine ASR query endpoint](https://openspeech.bytedance.com/api/v3/auc/bigmodel/query) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text transcript files and status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a directly accessible video URL, local ffmpeg, the Python requests package, Volcengine TOS credentials, and Volcengine speech recognition credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
