## Description: <br>
Speech enhancement / vocal denoising on remote (FREE) L4 GPU. Trigger when user says: denoise, remove noise, clean up audio, 去噪, 降噪, enhance audio. Takes local audio/video files and returns noise-reduced speech audio. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[speech2srt](https://clawhub.ai/user/speech2srt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and media operations teams use this skill to clean speech audio from local audio or video files by uploading selected media to Modal for GPU-based denoising and downloading enhanced WAV outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected audio or video files are sent to Modal for cloud processing. <br>
Mitigation: Use explicit file selections, avoid sensitive recordings unless external processing is acceptable, and confirm that Modal use is permitted for the data. <br>
Risk: Directory inputs may include unintended media files. <br>
Mitigation: List discovered media files and ask the user to confirm the exact selection before upload. <br>
Risk: Uploaded task data may remain in the Modal volume after processing. <br>
Mitigation: Run the documented recursive cleanup command after successful download. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/speech2srt/speech-denoise) <br>
- [Error Handling](references/error-handling.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Markdown, Guidance] <br>
**Output Format:** [Markdown with inline bash commands, local file paths, and enhanced WAV audio files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Downloads enhanced WAV files beside the original inputs and reports processed file count, result paths, sizes, and real-time factor.] <br>

## Skill Version(s): <br>
1.3.1 (source: server evidence release; SKILL.md frontmatter v1.3.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
