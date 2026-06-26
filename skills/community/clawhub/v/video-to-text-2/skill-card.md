## Description: <br>
Video to text converter. Downloads videos from Bilibili using bilibili-api, from other sites using yt-dlp, then transcribes audio using faster-whisper. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Lkyyyy320](https://clawhub.ai/user/Lkyyyy320) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and content teams use this skill to convert online videos or local media files into text transcripts or subtitle-ready text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bilibili authentication values such as SESSDATA, bili_jct, and buvid3 are login credentials. <br>
Mitigation: Avoid pasting credentials into chat or shell history, avoid hardcoding them in shared copies of the script, and rotate or log out of Bilibili if they are exposed. <br>
Risk: The skill downloads or reads user-selected videos before transcription. <br>
Mitigation: Use it only with videos you are allowed to access and transcribe, and install it only if you trust the referenced Python packages. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Lkyyyy320/video-to-text-2) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Text transcript output with Markdown usage guidance and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can print transcripts to the terminal or write them to a user-selected output file.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
