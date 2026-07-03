## Description: <br>
Converts Markdown or text chapter files into MP3 audiobook audio using the Xiaomi MiMo TTS API, with batch processing, long-text segmentation, voice and style options, and resume support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhouchang1988](https://clawhub.ai/user/zhouchang1988) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to turn trusted chapter directories into MP3 audiobook files through the Xiaomi MiMo TTS API, choosing voices, styles, chapter ranges, and output folders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Chapter text and the API key may be sent to the configured TTS API endpoint, including a custom endpoint if one is supplied. <br>
Mitigation: Use only trusted chapter content, treat the API key as sensitive, and avoid custom base URLs unless the endpoint is controlled and trusted. <br>
Risk: The shell wrapper constructs and evaluates a command from option values, so untrusted paths or option values can affect command execution. <br>
Mitigation: Prefer invoking the Python synthesis script directly and pass only trusted paths and option values when using the wrapper. <br>


## Reference(s): <br>
- [Xiaomi MiMo Token Plan](https://mimo.mi.com/token-plan) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Files] <br>
**Output Format:** [Markdown guidance with shell commands; execution produces MP3 audio files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses chapter directory, output directory, API key, voice, style, model, endpoint, delay, and chapter range options.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
