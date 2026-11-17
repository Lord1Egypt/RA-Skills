## Description:

Youtube Highest Quality Downloader - Download highest quality silent video and pure audio from YouTube, then merge into video with sound

This skill is ready for commercial/non-commercial use.

## Publisher:

[accidwar](https://clawhub.ai/user/accidwar)

### License/Terms of Use:


## Use Case:

Developers and other users can use this skill to download separate high-quality video and audio streams from a YouTube URL and merge them into a single playable video file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-controlled URLs, output names, or output directories may be passed into shell commands.

Mitigation: Only run the scripts with trusted values until command execution is changed to argument lists without shell=True or os.system.

Risk: The shell workflow can install yt-dlp without a pinned version.

Mitigation: Use an explicit, pinned dependency setup that is reviewed before installation.

Risk: Wildcard or unvalidated media file selection can merge or remove unintended files in the output directory.

Mitigation: Use a dedicated output directory and validate generated filenames before running ffmpeg or cleanup commands.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance]

**Output Format:** [Markdown instructions with command-line examples and scripts that create local media files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local video and audio intermediates and a merged MP4 file when its scripts are run.]

## Skill Version(s):

1.0.1 (source: server release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
