## Description:

Use ZeroCut CLI media and document tools. Invoke when user needs generate media, run ffmpeg/pandoc, sync resources, or save outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smartdiana](https://clawhub.ai/user/smartdiana)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to have agents invoke ZeroCut CLI commands for media generation, speech audio, ffmpeg or ffprobe work, pandoc conversion, resource syncing, and saved outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated or converted files may be written into the current workspace, and missing output directories may be created.

Mitigation: Specify trusted input resources and explicit output filenames or directories before running commands.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose commands that create output directories and write generated or converted files into the current workspace.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
