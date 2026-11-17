## Description:

Convert videos for compatibility and uploads -- pick the right container, codec, and bitrate for each destination, fix rejected uploads, and shrink files without visible quality loss.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leooooooow](https://clawhub.ai/user/leooooooow)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and content teams use this skill to prepare video files for marketplace, social, ad manager, CMS, email, and course-platform upload requirements. It helps select conversion settings, generate reproducible ffmpeg commands, verify outputs, and document quality tradeoffs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated ffmpeg commands may overwrite existing files when output paths or overwrite flags are used carelessly.

Mitigation: Review each command before execution, especially output paths and any -y flags.

Risk: The workflow depends on running ffmpeg or ffprobe against local video files.

Mitigation: Install only if comfortable using local media-processing tools and inspect generated commands before running them.

Risk: Upload platform limits and codec requirements can change after the bundled reference tables were written.

Mitigation: Confirm destination requirements against current platform documentation before large batches or high-value delivery.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/leooooooow/skills/upload-video-converter)
- [Conversion Delivery Template](references/output-template.md)
- [Baseline Upload Requirements by Destination Type](references/platform-upload-specs.md)
- [ffmpeg Recipes: Probe, Encode Ladders, Size Math](references/ffmpeg-recipes.md)
- [Troubleshooting Rejected or Broken Uploads](references/troubleshooting-guide.md)
- [Conversion -- Pre-Delivery Checklist](assets/conversion-checklist.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with ffmpeg and ffprobe command blocks, per-destination spec tables, verification notes, and handoff text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces recommendations and commands for the agent user to review and run; it does not process video directly.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
