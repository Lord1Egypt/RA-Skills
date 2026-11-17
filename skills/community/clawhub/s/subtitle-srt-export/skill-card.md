## Description:

Export a standard .srt subtitle file from the MEASURED word timings in a job's input.json (written by elevenlabs-tts). Flattens the per-word timings into readable cues (max ~3.5s / ~10 words per cue, breaking on sentence punctuation) and writes <job>/subtitles.srt for upload to YouTube and other platforms. No API call. Re-runnable. Does not modify input.json.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pushpendrachauhan](https://clawhub.ai/user/pushpendrachauhan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content automation users use this skill to convert measured word timings in a job input.json into readable SRT subtitle cues for video platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local shell script reads input.json and overwrites subtitles.srt in the selected job folder.

Mitigation: Run it only in job folders you control and review the target path before execution.

Risk: A fixed .cues.tmp temporary file may be less robust in shared or untrusted job folders.

Mitigation: Avoid running in directories writable by other users, avoid root execution, and consider replacing the fixed temporary file with mktemp.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pushpendrachauhan/skills/subtitle-srt-export)
- [Publisher profile](https://clawhub.ai/user/pushpendrachauhan)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and generated SRT file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes <job>/subtitles.srt and prints cue and word counts; requires jq and awk.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
