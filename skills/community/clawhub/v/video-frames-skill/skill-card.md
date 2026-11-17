## Description:

Video frame extraction and processing tool based on PyAV, supporting single-frame extraction, batch sampling, directory processing, video information display, video compression, and WebP image conversion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[indulgeback](https://clawhub.ai/user/indulgeback)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and media-processing users use this skill to install, diagnose, and run PyAV-based commands for extracting video frames, sampling keyframes, compressing videos, and converting images to WebP.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented automatic installer executes a remote shell script from a mutable main branch.

Mitigation: Inspect the installer before execution or use a pinned, checksum-verified local install flow.

Risk: Recursive batch media processing can write many output files and convert or compress media in bulk.

Mitigation: Run commands on copied inputs, choose explicit output directories, and review options before recursive execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/indulgeback/skills/video-frames-skill)
- [Project homepage from artifact metadata](https://github.com/indulgeback/video-frame-extractor)
- [Issue tracker from artifact documentation](https://github.com/indulgeback/video-frame-extractor/issues)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may install dependencies, inspect local media tooling, and write extracted or compressed media files to user-selected output paths.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
