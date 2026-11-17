## Description:

Local speech-to-text using Qwen3-ASR on macOS and Linux with a CPU-only, no-cloud workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huanglizhuo](https://clawhub.ai/user/huanglizhuo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users use this skill to transcribe local audio files or stdin audio without sending content to a cloud transcription API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer downloads an unverified latest remote binary from GitHub Releases.

Mitigation: Install only after accepting that supply-chain risk, and prefer a pinned or independently verified binary when deploying in controlled environments.

Risk: The wrapper can delete an original WAV file because it cleans up the selected input path on exit.

Mitigation: Use copies, stdin, or direct qwen-asr invocation for WAV inputs until the cleanup behavior is fixed.

Risk: The skill stores a large local model under the user's home directory.

Mitigation: Confirm disk capacity and expected storage location before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huanglizhuo/skills/qwen-asr-local)
- [ClawHub publisher profile](https://clawhub.ai/user/huanglizhuo)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text transcription guidance with Markdown and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Transcription output depends on the local qwen-asr binary, the downloaded model, optional ffmpeg conversion, and user-supplied audio.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
