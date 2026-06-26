## Description: <br>
Generates speech with Xiaomi MiMo TTS (mimo-v2-tts), including voice selection, style tags, emotion labels, dialect support, and API-key based execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jazzqi](https://clawhub.ai/user/jazzqi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to synthesize local speech audio from text through Xiaomi MiMo, with optional style, voice, emotion, and dialect controls for agent responses, demos, and content generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text submitted for synthesis is sent to Xiaomi's MiMo API. <br>
Mitigation: Avoid sending sensitive text unless the user is comfortable with Xiaomi MiMo API processing and has reviewed the service terms. <br>
Risk: Generated audio files may overwrite or leave behind local artifacts if output paths are chosen carelessly. <br>
Mitigation: Use explicit, non-critical output paths and remove generated audio files after use. <br>
Risk: Smart mode uses heuristic keyword rules and may choose an unintended emotion, dialect, or style. <br>
Mitigation: Use explicit style tags when accuracy matters, and keep smart mode opt-in for higher-sensitivity workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jazzqi/xiaomi-mimo-tts) <br>
- [Xiaomi MiMo platform](https://platform.xiaomimimo.com/) <br>
- [Xiaomi MiMo chat completions API endpoint](https://api.xiaomimimo.com/v1/chat/completions) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact changelog](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration instructions, API Calls] <br>
**Output Format:** [Audio files (.ogg or .wav), terminal status text, and optional dry-run JSON payload previews.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires XIAOMI_API_KEY or MIMO_API_KEY for real synthesis; generated audio files should be stored in safe output paths and removed when no longer needed.] <br>

## Skill Version(s): <br>
1.2.5 (source: server release metadata; artifact package.json reports 1.0.2 and artifact _meta.json reports 1.1.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
