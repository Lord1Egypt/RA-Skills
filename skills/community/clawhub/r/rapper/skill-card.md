## Description: <br>
Create and debug SenseAudio rap, hip-hop, or vocal song generation workflows using the SenseAudio lyric and music generation APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scikkk](https://clawhub.ai/user/scikkk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to produce rap lyrics, create vocal songs from lyrics, tune song style controls, and poll asynchronous SenseAudio generation jobs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a SenseAudio API key and may consume API quota when generation or polling requests are made. <br>
Mitigation: Use a dedicated SenseAudio API key for this workflow, keep it in the SENSEAUDIO_API_KEY environment variable, and review generated requests before running them. <br>
Risk: Lyrics, prompts, and style instructions sent to SenseAudio may contain private or sensitive content. <br>
Mitigation: Avoid sending private lyrics or sensitive prompt content unless the user is comfortable sharing it with SenseAudio. <br>


## Reference(s): <br>
- [SenseAudio homepage](https://nightly.senseaudio.cn) <br>
- [SenseAudio Music Reference](artifact/references/music.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown with inline JSON and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses SENSEAUDIO_API_KEY and may include polling logic for asynchronous generation tasks.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
