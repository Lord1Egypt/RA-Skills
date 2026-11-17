## Description:

Records broadcast FM stations from an RTL-SDR with IQ capture, offline WBFM demodulation, RDS station-name extraction, and automatic MP3 naming.

This skill is ready for commercial/non-commercial use.

## Publisher:

[igrikxd](https://clawhub.ai/user/igrikxd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical users use this skill to check RTL-SDR broadcast-FM readiness, scan stations, decode RDS station names, and record selected stations as named MP3 files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can run a redsea binary from a predictable /tmp fallback path.

Mitigation: Use a trusted redsea installation from PATH or patch/remove the /tmp fallback before deployment.

Risk: The scripts create MP3, JSON cache, scan summary, and debug files in the selected output directory.

Mitigation: Run with an explicit output directory and avoid privileged execution.

## Reference(s):

- [Pipeline Notes](references/pipeline-notes.md)
- [ClawHub Skill Page](https://clawhub.ai/igrikxd/skills/rtl-sdr-fm-rds-recorder)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands, JSON command output, plain text file paths, MP3 audio files, and metadata/debug JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include scan summaries, RDS cache and debug JSON, MP3 recordings, and optional intermediate IQ/WAV files when requested.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
