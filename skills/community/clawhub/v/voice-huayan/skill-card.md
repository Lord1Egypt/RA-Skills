## Description: <br>
Local Chinese TTS playback on Windows using Piper zh_CN-huayan-medium with automatic fallback to System.Speech. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mecyalika](https://clawhub.ai/user/mecyalika) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when they want an agent to read Chinese text aloud locally on Windows in the huayan voice style. It is intended for direct speaker playback with a Piper voice preference and System.Speech fallback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan reports this as a suspicious local TTS/model-preparation package because the documented Windows playback runner is missing. <br>
Mitigation: Confirm the expected Windows runner is present and reviewed before relying on the advertised playback workflow. <br>
Risk: The included shell script can install Python packages and download model assets from remote sources. <br>
Mitigation: Run setup only in a contained environment, verify package and model sources manually, and avoid elevated privileges. <br>
Risk: The release under-discloses network downloads and package installation behavior. <br>
Mitigation: Review the server security guidance and artifact scripts before installation or deployment. <br>


## Reference(s): <br>
- [ClawHub voice-huayan release page](https://clawhub.ai/mecyalika/voice-huayan) <br>
- [Publisher profile](https://clawhub.ai/user/mecyalika) <br>
- [Piper voices on Hugging Face](https://huggingface.co/rhasspy/piper-voices) <br>
- [sherpa-onnx TTS model assets](https://github.com/k2-fsa/sherpa-onnx/releases/tag/tts-models) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, Guidance] <br>
**Output Format:** [Markdown with inline PowerShell command examples and playback status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Direct speaker playback when available; successful playback is reported with PLAYBACK_OK.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
