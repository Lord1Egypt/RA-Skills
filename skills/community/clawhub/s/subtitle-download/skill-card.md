## Description:

Batch-download missing subtitles for a media library of organized movie folders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mina-atef-00](https://clawhub.ai/user/mina-atef-00)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and media-library maintainers use this skill to plan and run a Podman-based Subliminal workflow that fills missing subtitle files while preserving exact video-to-subtitle filename stems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper script uses read-write access to the selected media library and can rename or delete subtitle files during normalization and conversion.

Mitigation: Set MOVIES explicitly to the intended folder, review the planned changes, and back up existing subtitle files before running the script.

Risk: The workflow runs a Podman image and ffmpeg conversion steps that affect files in the mounted movie library.

Mitigation: Review the Podman image and tag, inspect the script before execution, and verify converted .srt files are non-empty before removing source subtitle formats.

## Reference(s):

- [Research Summary](references/research-summary.md)
- [ClawHub Skill Page](https://clawhub.ai/mina-atef-00/skills/subtitle-download)
- [Publisher Profile](https://clawhub.ai/user/mina-atef-00)
- [Project Homepage](https://github.com/mina-atef-00/agent-skills)
- [Rustitles](https://github.com/fosterbarnes/rustitles)
- [Bazarr](https://github.com/morpheus65535/bazarr)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and a helper shell script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance is oriented to Linux, Podman, Subliminal, and organized movie folders with exact-stem .srt subtitle files.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
