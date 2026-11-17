## Description:

Generates WeChat Official Account article cover assets by reading an article or topic, selecting visual imagery, creating a square master image, applying Chinese title overlays, and producing WeChat-ready cover formats with QA checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jondeng11-creator](https://clawhub.ai/user/jondeng11-creator)

### License/Terms of Use:

MIT

## Use Case:

Content creators, social media operators, and agents preparing WeChat Official Account articles use this skill to turn an article file or topic brief into a publication-ready cover set and a short design/QA note.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable URL imports can reduce reproducibility.

Mitigation: Install from a trusted reviewed source and prefer pinned or reviewed release artifacts when reproducible deployment matters.

Risk: Generic trigger phrases may activate the skill in the wrong context.

Mitigation: Invoke the skill explicitly by name or with a clear WeChat cover request before allowing it to read files or create outputs.

Risk: The skill reads article inputs and writes generated images to an output directory.

Mitigation: Confirm the article path and output folder before execution, especially in sensitive project directories.

Risk: Large or untrusted image files may create processing or safety concerns during PIL post-processing.

Mitigation: Avoid unusually large or untrusted input images and review source images before processing.

## Reference(s):

- [WeChat cover rules](references/wechat-cover-rules.md)
- [ClawHub skill page](https://clawhub.ai/jondeng11-creator/skills/wc-cover-studio)

## Skill Output:

**Output Type(s):** [Files, Markdown, Shell commands, Guidance]

**Output Format:** [PNG image files, Markdown notes, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces 900x383 wide, 1080x1080 square, and single-image dual-use WeChat cover variants; QA output reports title-region and layout checks.]

## Skill Version(s):

1.1.0 (source: server release metadata and artifact config.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
