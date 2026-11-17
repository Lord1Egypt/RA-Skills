## Description:

Reduces speech frequencies in video audio with ffmpeg equalizer filters while preserving mechanical and environmental sounds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangyanbo2007](https://clawhub.ai/user/zhangyanbo2007)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, media operators, and external users use this skill to generate ffmpeg commands that reduce spoken voice in videos while retaining useful non-speech audio such as machinery or ambient sounds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated output may not fully remove voices because frequency filtering cannot separate overlapping speech and environmental sounds.

Mitigation: Review the generated '_novoice' video and tune equalizer gain or bandwidth before using the result.

Risk: Replacing the original video can permanently lose the source audio if the filtered result is unsatisfactory.

Mitigation: Keep backups and only replace the original after confirming the generated '_novoice' file.

Risk: The installation examples include package-manager commands that can change the local system.

Mitigation: Run installation commands only when ffmpeg is needed and the package manager source is trusted.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces commands and parameter-tuning guidance; generated media should be reviewed before replacing originals.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
