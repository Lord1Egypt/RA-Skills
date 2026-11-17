## Description:

Windows SAPI5 text-to-speech with Neural voices for generating audio on Windows 10/11 with no GPU use, instant generation, and automatic language voice selection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[korddie](https://clawhub.ai/user/korddie)

### License/Terms of Use:


## Use Case:

Developers and Windows users use this skill to generate WAV speech audio from text with Windows SAPI5 voices. It helps select an available voice by language, adjust rate, save audio locally, and optionally play the result immediately.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated audio files may contain the spoken text and are stored locally by default.

Mitigation: Choose an appropriate output path, limit sensitive text, and remove generated WAV files when they are no longer needed.

Risk: The optional neural-voice adapter is third-party software distributed outside the skill.

Mitigation: Install the adapter only after verifying that the project and downloaded release are trusted for the intended environment.

Risk: The skill asks the user to run a local PowerShell script.

Mitigation: Review the script before execution and run it only in a trusted Windows environment with the intended permissions.

## Reference(s):

- [NaturalVoiceSAPIAdapter](https://github.com/gexgd0419/NaturalVoiceSAPIAdapter)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Files, Guidance]

**Output Format:** [Markdown with PowerShell code blocks, command examples, and parameter tables; runtime output is WAV audio.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local WAV files by default and can emit MEDIA:<path> for playback workflows.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
