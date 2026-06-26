## Description: <br>
Video Pipeline Bundle helps agents guide and run a local video workflow for silence removal, speech-to-subtitle generation, subtitle burn-in, format conversion, and video concatenation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Leochens](https://clawhub.ai/user/Leochens) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and video operators use this skill to process batches of local video from raw footage into subtitles, burned-caption videos, converted files, and final merged outputs. It is suited to agent-assisted video processing workflows that need explicit dependency checks and step-by-step execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can change the local Python environment while installing video-processing dependencies. <br>
Mitigation: Review dependency commands first and run the skill in a virtual environment, container, or other isolated workspace. <br>
Risk: Transcription correction can send video-derived text to the selected LLM provider. <br>
Mitigation: Avoid confidential videos unless the provider and account settings are acceptable for that data, and use restricted API keys supplied through environment variables. <br>
Risk: Optional progress notifications can expose filenames or processing status to an external chat target. <br>
Mitigation: Leave notifications disabled for sensitive work, or verify OPENCLAW_TARGET before enabling them. <br>
Risk: The clipping workflow can rename source video files. <br>
Mitigation: Back up original videos or test on copies before running batch processing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Leochens/video-pipeline-bundle) <br>
- [MiniMax Open Platform](https://platform.minimaxi.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Code, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated local video, subtitle, and text files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create edited videos, SRT subtitle files, burned-caption videos, merged videos, and transcript text files in local output directories.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
