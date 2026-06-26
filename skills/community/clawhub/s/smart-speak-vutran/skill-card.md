## Description: <br>
Multilingual Text-to-Speech (TTS) with intelligent Pinyin-to-Hanzi conversion for text containing Vietnamese, Chinese (Pinyin), or English. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Jaskies](https://clawhub.ai/user/Jaskies) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate multilingual MP3 speech from mixed Vietnamese, Chinese or Pinyin, and English text. The workflow prepares language-specific text segments, invokes TTS voices, and merges generated audio into one output file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local edge-tts and ffmpeg commands to synthesize and merge audio. <br>
Mitigation: Verify the configured executable paths and review generated commands before execution; keep output paths inside the intended workspace. <br>
Risk: Text supplied for synthesis may be sent to the Edge TTS service. <br>
Mitigation: Avoid using secrets or sensitive personal content unless the user accepts the external TTS data handling. <br>
Risk: Hardcoded local paths may not match the user's environment. <br>
Mitigation: Adjust the edge-tts path and MP3 output path for the deployment environment before running the workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Jaskies/smart-speak-vutran) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with bash and JSON examples, plus generated MP3 audio files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local edge-tts and ffmpeg availability; text segments are passed as JSON and merged into a single MP3 output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
