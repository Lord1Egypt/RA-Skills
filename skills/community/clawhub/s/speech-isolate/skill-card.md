## Description: <br>
Vocal isolation / background music removal on remote (FREE) L4 GPU; takes local audio/video files and returns isolated vocals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[speech2srt](https://clawhub.ai/user/speech2srt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to run a remote audio pipeline that separates vocals from music or other background sound, then denoises the speech output. It is intended for local audio or video files that can be uploaded to Modal for processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected audio or video files are uploaded to Modal for cloud processing. <br>
Mitigation: Use the skill only for files that are acceptable to process in Modal, and confirm file selections before upload. <br>
Risk: Cleanup uses a recursive remove command against a slug-named volume path. <br>
Mitigation: Use a unique slug for each task and verify the exact slug before running cleanup. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/speech2srt/speech-isolate) <br>
- [Error Handling](references/error-handling.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Files] <br>
**Output Format:** [Markdown with inline bash code blocks and local WAV output paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Downloads isolated 24-bit WAV files named <stem>_isolated.wav and may report processed-file count, file sizes, and real-time factor metrics.] <br>

## Skill Version(s): <br>
1.3.1 (source: evidence release, frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
