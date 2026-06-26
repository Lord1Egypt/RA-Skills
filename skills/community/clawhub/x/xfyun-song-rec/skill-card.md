## Description: <br>
Recognize songs by singing or audio file using iFlytek's Query By ACRCloud technology. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Dzy-1026](https://clawhub.ai/user/Dzy-1026) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users use this skill to identify music from a selected audio file or singing sample for song discovery, karaoke, audio content recognition, and music search workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected audio files are sent to iFlytek's service for recognition. <br>
Mitigation: Use only audio that is approved for external processing, and avoid private speech, confidential recordings, or copyrighted material without the right approvals. <br>
Risk: The skill requires iFLYTEK API credentials on the machine where it runs. <br>
Mitigation: Store XF_SONG_APP_ID, XF_SONG_API_KEY, and XF_SONG_API_SECRET in the environment or approved agent configuration, and rotate them if exposure is suspected. <br>


## Reference(s): <br>
- [iFLYTEK music recognition API documentation](https://www.xfyun.cn/doc/voiceservice/music_recognition/API.html) <br>
- [ClawHub release page](https://clawhub.ai/Dzy-1026/xfyun-song-rec) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/Dzy-1026) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Console text with a JSON recognition result] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an audio file path, Python 3, network access, and iFLYTEK API credentials in XF_SONG_APP_ID, XF_SONG_API_KEY, and XF_SONG_API_SECRET.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
