## Description: <br>
Text-to-Speech using SiliconFlow API (CosyVoice2). Supports multiple voices, languages, and dialects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lilei0311](https://clawhub.ai/user/lilei0311) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to generate local audio files from text through SiliconFlow's CosyVoice2 text-to-speech API, with selectable voices, speech speed, and output formats. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text submitted for speech generation is sent to SiliconFlow under the user's API key. <br>
Mitigation: Use the skill only for text that may be processed by SiliconFlow, and prefer a limited API key where possible. <br>
Risk: The skill can auto-detect an API key from ~/.openclaw/openclaw.json. <br>
Mitigation: Verify the configured SiliconFlow key before running the skill, especially on shared or reused agent environments. <br>
Risk: Caller-selected output paths may overwrite local files. <br>
Mitigation: Choose explicit non-sensitive output paths and review existing files before writing generated audio. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lilei0311/siliconflow-tts-gen) <br>
- [SiliconFlow API endpoint](https://api.siliconflow.cn/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files, guidance] <br>
**Output Format:** [JSON status output and generated audio files such as mp3, opus, wav, or pcm.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SILICONFLOW_API_KEY or a SiliconFlow API key in ~/.openclaw/openclaw.json; text is sent to SiliconFlow and output paths are caller-selected.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
