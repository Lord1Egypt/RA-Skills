## Description:

Yolo Utilities guides agents in choosing and running yoloutils CLI subcommands for YOLO dataset inspection, conversion, copying, cleanup, cropping, resizing, classification dataset preparation, and model testing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[netkiller](https://clawhub.ai/user/netkiller)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and ML practitioners use this skill when they need an agent to provide precise yoloutils commands, parameter checks, side-effect warnings, and verification steps for YOLO dataset workflows. It is suited for dataset maintenance tasks such as label statistics, label merging, sample copying, label removal or replacement, image cropping and resizing, dataset conversion, classification splits, and model test reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Commands using --clean can delete target, output, or checklist directories before processing.

Mitigation: Confirm all destination paths, keep backups, and test on a small sample before running the command on the full dataset.

Risk: The remove command without --target and the change command modify label files in place.

Mitigation: Prefer a separate target directory when supported, and create a backup before any in-place label removal or replacement.

Risk: Some workflows can overwrite files when output paths flatten directories or reuse inferred filenames.

Mitigation: Inspect planned source and target layouts for duplicate basenames, and verify output counts and sample files after execution.

## Reference(s):

- [Yolo Utilities on ClawHub](https://clawhub.ai/netkiller/skills/yoloutils)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration file references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes command prerequisites, side-effect notes, and post-run verification steps.]

## Skill Version(s):

1.0.0 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
