## Description:

Automates watermark-removal image processing by submitting images to a configured local GUI watch folder and collecting completed output files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[muxiazi](https://clawhub.ai/user/muxiazi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to process single images or image batches through a locally running watermark-removal GUI. It is intended for environments where the GUI is already installed, configured, and monitoring matching input and output folders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an external local GUI application whose source and integrity are not established by the bundled artifact.

Mitigation: Install and use the GUI only when the operator trusts and can verify that application.

Risk: A user-controlled task subdirectory can resolve outside the configured watch folder.

Mitigation: Use automatically generated task subdirectories, avoid passing user-controlled values to --subdir, and prefer a hardened version that rejects absolute paths, '..' components, and resolved paths outside input_dir.

Risk: The --move option can remove original input files while submitting them for processing.

Mitigation: Prefer copying files and use --move only when backups exist and the deletion behavior is intended.

Risk: Shared GUI input and output folders can mix tasks or expose files between users.

Mitigation: Use dedicated input and output folders and keep per-task subdirectories enabled for isolation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/muxiazi/skills/watermark-remover-skill)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON result files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns processed image paths, undetected-watermark paths, pending files, elapsed time, and exit codes when run through the bundled CLI.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
