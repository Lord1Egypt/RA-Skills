## Description:

Download YouTube video audio and convert it to MP3, with optional cookies support for age-restricted videos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[banner90](https://clawhub.ai/user/banner90)

### License/Terms of Use:

MIT

## Use Case:

Developers and external users can use this OpenClaw skill to download audio from a YouTube URL as an MP3 file for downstream translation or playback workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package entry points to an unbundled absolute-path Python file, so installation may execute or depend on code outside the packaged artifact.

Mitigation: Review the package before installing, require a bundled package-relative entry path, and verify the downloader script before execution.

Risk: The skill supports cookies for age-restricted videos without documented safe-handling guidance for the cookies file.

Mitigation: Use cookies only with trusted code, keep the cookies file private and temporary, and delete it after the download workflow is complete.

## Reference(s):


## Skill Output:

**Output Type(s):** [Files, JSON]

**Output Format:** [JSON status object with an audio file path for a generated MP3 file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require a private cookies.txt file for age-restricted videos and a Windows Python environment when used as documented.]

## Skill Version(s):

1.0.6 (source: server release metadata; artifact package.json and openclaw.plugin.json report 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
