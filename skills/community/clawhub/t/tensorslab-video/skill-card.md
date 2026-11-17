## Description:

Generate videos using TensorsLab's AI video generation models, supporting text-to-video and image-to-video workflows with prompt enhancement, progress tracking, and local file saving.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bob5-tensorslab](https://clawhub.ai/user/bob5-tensorslab)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate short videos from text prompts or source images through TensorsLab, with configurable models, aspect ratios, durations, and output directories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, optional source images, and the TensorsLab API key are sent to the TensorsLab API.

Mitigation: Use the skill only with content appropriate for TensorsLab, store the API key in TENSORSLAB_API_KEY, and avoid passing the key on the command line.

Risk: The downloader trusts server-provided URLs without host allowlisting or download size limits.

Mitigation: Run the skill in a virtual environment, use a constrained output directory, and monitor downloaded files and storage usage.

## Reference(s):

- [TensorsLab Video API Reference](references/api_reference.md)
- [TensorsLab API](https://api.tensorslab.com)
- [ClawHub skill page](https://clawhub.ai/bob5-tensorslab/skills/tensorslab-video)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated local video files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TENSORSLAB_API_KEY and may write MP4 files to a local output directory.]

## Skill Version(s):

1.0.3 (source: server release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
