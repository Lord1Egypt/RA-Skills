## Description:

Collects TikTok, Douyin, Bilibili, and related creator data through the TikHub API, with helpers for comments, user/video metadata, paid video downloads, audio extraction, and Whisper transcription.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kk-kingkong](https://clawhub.ai/user/kk-kingkong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operations teams use this skill to collect creator platform data, download videos, extract audio, and generate transcripts for analysis workflows. It is intended for trusted TikHub API usage where the operator controls API credentials and local output handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CPU/background Whisper transcription path has a high-impact command-injection flaw.

Mitigation: Avoid the CPU/background Whisper path until shell=True is removed and command arguments are executed without shell interpolation.

Risk: The skill can run background local transcription processes with limited user control.

Mitigation: Run transcription in a supervised session, review process status and logs, and prefer the Apple GPU mlx-whisper path when available.

Risk: Video download calls can use paid TikHub API endpoints and consume account balance.

Mitigation: Check balance first, confirm each paid download workflow before execution, and use small batches with delays.

Risk: Comments, user data, local media files, extracted audio, transcripts, identifiers, and URLs may be stored locally or sent to TikHub.

Mitigation: Use only trusted links and files, handle outputs as potentially sensitive data, and confirm that collection complies with platform terms and applicable policy.

## Reference(s):

- [TikHub API Documentation](https://api.tikhub.io/docs)
- [TikHub User Console](https://user.tikhub.io)
- [ClawHub Skill Page](https://clawhub.ai/kk-kingkong/skills/tiktok-pipeline)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with Python snippets, shell commands, JSON result files, downloaded media files, extracted audio, and transcript text files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call external TikHub endpoints, consume paid API balance, write local media/comment/transcript files, and run local ffmpeg or Whisper transcription processes.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
