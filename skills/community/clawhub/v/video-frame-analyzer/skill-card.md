## Description:

Video Frame Analyzer extracts key frames from short-form AI drama videos, guides multimodal frame-by-frame analysis, and produces structured Markdown reports covering plot, cinematography, characters, dialogue, and adaptation recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roseryztzhoutong](https://clawhub.ai/user/roseryztzhoutong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and content teams use this skill to deconstruct AI drama or short-video footage, extract representative frames, and compile structured narrative, visual, dialogue, and adaptation analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented script lookup can resolve a spoofed smart_extract.py from another installed skill directory.

Mitigation: Review the skill before installing and update execution commands to call this skill's packaged references/smart_extract.py by exact path.

Risk: Video frames and generated report files may contain sensitive or proprietary visual content.

Mitigation: Run the skill only on videos intended for analysis and choose a non-sensitive output directory.

Risk: Unpinned multimedia dependencies can vary across environments.

Mitigation: Install dependencies in an isolated environment with pinned versions where possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/roseryztzhoutong/skills/video-frame-analyzer)
- [README](artifact/README.md)
- [Smart frame extraction script](artifact/references/smart_extract.py)
- [Fallback frame extraction script](artifact/references/extract_frames.py)

## Skill Output:

**Output Type(s):** [markdown, files, shell commands, guidance]

**Output Format:** [Markdown reports with extracted image files and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Frame analysis is performed in small batches of 3-4 images to reduce context-length failures.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
