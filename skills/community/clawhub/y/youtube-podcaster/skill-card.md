## Description: <br>
Extracts YouTube transcript text and converts it into a multi-voice AI podcast using Gemini for script generation, OpenAI TTS for speech, and FFmpeg for audio assembly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaudata](https://clawhub.ai/user/kaudata) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill to turn public YouTube video transcripts into editable podcast scripts, synthesized multi-voice audio, and caption files. It is suited for agent-assisted local media generation workflows that can provide Gemini and OpenAI API credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles Gemini and OpenAI API keys for transcript search, script generation, and speech synthesis. <br>
Mitigation: Use dedicated .env credentials with spending limits, rotate keys when needed, and avoid entering keys in shared or untrusted environments. <br>
Risk: Transcript and generated script content is sent to Gemini and OpenAI services. <br>
Mitigation: Avoid private, sensitive, or regulated video content unless the external service use is approved for that data. <br>
Risk: The release runs a local Node server, installs npm dependencies, invokes FFmpeg, and creates removable session files. <br>
Mitigation: Install from trusted package sources, run locally on 127.0.0.1, stop the tracked server process when finished, and use the reset/delete controls for generated files. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kaudata/youtube-podcaster) <br>
- [Publisher profile](https://clawhub.ai/user/kaudata) <br>
- [Source code URL listed in artifact](https://github.com/kaudata/youtube-podcaster) <br>


## Skill Output: <br>
**Output Type(s):** [text, audio, WebVTT, files, shell commands, configuration] <br>
**Output Format:** [Plain text transcripts and scripts, M4A audio, WebVTT captions, and ZIP/file downloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated session files are stored locally under a downloads session folder and can be deleted with the skill cleanup controls.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
