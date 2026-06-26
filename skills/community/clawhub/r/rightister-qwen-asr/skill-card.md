## Description: <br>
Provides offline Chinese and mixed Chinese-English speech-to-text recognition using qwen-asr with local C-based inference. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rightister](https://clawhub.ai/user/rightister) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to run local speech-to-text transcription for Chinese or mixed Chinese-English audio, including edge deployments where offline inference is preferred. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local binaries and FFmpeg against user-provided audio files. <br>
Mitigation: Use trusted qwen-asr sources, keep local dependencies minimal, and review audio inputs before running local processing. <br>
Risk: Initial setup requires model files and local build dependencies. <br>
Mitigation: Download models from trusted sources, confirm applicable model terms, and install only the required FFmpeg and BLAS dependencies. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rightister/rightister-qwen-asr) <br>
- [qwen-asr reference notes](references/README.md) <br>
- [qwen-asr GitHub repository](https://github.com/antirez/qwen-asr) <br>
- [Qwen3-ASR-0.6B model](https://huggingface.co/antirez/qwen3-asr-0.6b) <br>
- [Qwen3-ASR-1.7B model](https://huggingface.co/antirez/qwen3-asr-1.7b) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text transcription with Markdown usage guidance and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local qwen-asr checkout, compiled binary, FFmpeg, a BLAS backend, and downloaded model files; inference runs offline after setup.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
