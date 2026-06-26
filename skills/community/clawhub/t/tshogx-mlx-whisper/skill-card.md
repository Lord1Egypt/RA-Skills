## Description: <br>
Local speech-to-text with MLX Whisper (Apple Silicon optimized, no API key). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TSHOGX](https://clawhub.ai/user/TSHOGX) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to run local speech-to-text, subtitle generation, language-hinted transcription, and translation workflows on Apple Silicon Macs with MLX Whisper. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a local mlx_whisper CLI and uses a Hugging Face model source that may be downloaded and cached locally. <br>
Mitigation: Install and run the CLI only from trusted sources, confirm the selected model, and account for local model cache storage. <br>
Risk: Transcripts or subtitle files can contain sensitive audio content and are written to user-selected output locations. <br>
Mitigation: Choose output directories deliberately and handle generated transcript or subtitle files according to the sensitivity of the source media. <br>


## Reference(s): <br>
- [MLX Whisper homepage](https://github.com/ml-explore/mlx-examples/tree/main/whisper) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides use of mlx_whisper with local audio or video files and user-selected output paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
