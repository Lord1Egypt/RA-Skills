## Description: <br>
Extracts subtitles and transcripts from YouTube videos and saves them as local timestamped text files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[feiskyer](https://clawhub.ai/user/feiskyer) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to retrieve captions for a supplied YouTube URL, first via yt-dlp and then through browser automation when a CLI transcript path is unavailable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may access browser-authenticated YouTube context or session cookies during subtitle extraction. <br>
Mitigation: Prefer a no-cookie transcript path for public videos and require explicit user approval before browser-cookie or browser-automation fallback is used. <br>
Risk: The release has a suspicious security verdict due to unclear consent around browser session cookie use. <br>
Mitigation: Review the skill before installation and use it only when browser-authenticated YouTube access is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/feiskyer/youtube-transcribe-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Timestamped transcript text file plus a concise completion report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Saves output in the current working directory and reports file path, subtitle language, and total line count.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
