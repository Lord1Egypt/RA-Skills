## Description:

Converts multilingual Vietnamese, Chinese, Pinyin, and English text segments into a single spoken MP3 file using edge-tts and ffmpeg.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jaskies](https://clawhub.ai/user/jaskies)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and content creators use this skill to generate multilingual spoken audio for lessons or announcements from Vietnamese, Chinese, Pinyin, and English text segments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installation guidance includes sudo and unpinned pip commands.

Mitigation: Review commands before execution, install in a virtual environment, and pin dependency versions where possible.

Risk: Text sent to the cloud TTS provider may include sensitive content.

Mitigation: Avoid synthesizing confidential or sensitive text unless provider data handling is acceptable for the use case.

Risk: The script uses a hard-coded local edge-tts executable path.

Mitigation: Update the edge-tts path for the deployment machine or invoke an executable resolved from the local environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jaskies/skills/smart-speak-jaskies)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Files]

**Output Format:** [Markdown guidance with bash command examples and JSON segment input; generated runtime output is MP3 audio.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local Python 3, edge-tts, and ffmpeg; the user supplies text segments, voices, and an output path.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
