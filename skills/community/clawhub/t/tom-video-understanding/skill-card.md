## Description: <br>
Local video comprehension skill. Use ffmpeg to extract audio and frames, FunASR for speech recognition, and qwen3-vl for image understanding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tomuiv](https://clawhub.ai/user/tomuiv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to inspect video content by extracting audio and frames, transcribing Chinese speech locally, and generating frame descriptions with a local vision model. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private video content, transcripts, frame descriptions, or summaries could leave the local machine if the optional cloud summary step is used. <br>
Mitigation: Use the local ffmpeg, FunASR, and Ollama workflow for private videos, and only use a cloud summary provider after choosing and trusting that provider. <br>
Risk: The skill proposes local shell commands for extracting media and running models, so users could overwrite generated audio or frame files if they run commands without review. <br>
Mitigation: Review commands and output paths before execution, and run them in a working directory prepared for extracted audio and frames. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tomuiv/tom-video-understanding) <br>
- [Ollama Download](https://ollama.com/download) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local transcripts, frame descriptions, and video summaries; optional cloud summary steps can expose derived video content to a chosen provider.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
