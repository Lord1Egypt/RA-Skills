## Description: <br>
Local text-to-speech using Qwen3-TTS-12Hz-1.7B-CustomVoice for generating WAV audio from text with selectable languages, speakers, and voice instructions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paki81](https://clawhub.ai/user/paki81) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers and agent users use this skill to generate WAV speech files from text with selectable speakers, languages, and natural-language voice instructions. It supports local offline synthesis after model download and can also be configured to use a remote TTS server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill advertises offline local text-to-speech, but remote HTTP modes can transmit input text to another server. <br>
Mitigation: Keep QWEN_TTS_REMOTE unset for private or offline use and avoid sending sensitive text to remote endpoints. <br>
Risk: The included server mode can expose an unauthenticated TTS API if bound to a broad network interface. <br>
Mitigation: Bind the server to localhost or a tightly controlled private network and add access controls before exposing it. <br>


## Reference(s): <br>
- [Qwen3-TTS-12Hz-1.7B-CustomVoice model card](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice) <br>
- [Qwen3-TTS Skill page](https://clawhub.ai/paki81/qwen-tts) <br>
- [References Directory](references/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and configuration examples; generated runtime artifacts are WAV audio files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May output local file paths for generated WAV audio and may call a configured remote TTS endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
