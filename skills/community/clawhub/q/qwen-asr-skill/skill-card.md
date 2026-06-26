## Description: <br>
Provides CPU-based speech-to-text transcription with automatic language detection for 22 Chinese dialects and 30 languages using the Qwen3-ASR-0.6B model. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yszheda](https://clawhub.ai/user/yszheda) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to convert audio messages or uploaded audio files into text, with optional language or dialect selection for Chinese dialect and multilingual recognition. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audio inputs may contain sensitive speech content. <br>
Mitigation: Run the service in the intended local environment, use trusted audio inputs, and review temporary-file handling before deployment. <br>
Risk: First use may download large model weights and CPU inference requires substantial memory. <br>
Mitigation: Plan disk and memory capacity, pin trusted dependency and model versions, and test latency on the target host. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yszheda/qwen-asr-skill) <br>
- [Qwen3-ASR-0.6B model](https://huggingface.co/Qwen/Qwen3-ASR-0.6B) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, shell commands] <br>
**Output Format:** [JSON API responses containing transcription text, detected language, confidence, and duration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts audio file or base64 audio input, optional language or dialect selection, and optional timestamp requests.] <br>

## Skill Version(s): <br>
1.3.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
