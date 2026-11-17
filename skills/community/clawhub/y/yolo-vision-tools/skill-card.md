## Description:

Use Ultralytics YOLO to perform computer vision tasks, such as detecting people or objects in images and videos, classifying images, estimating human poses, and tracking cars, people, or animals in videos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ruoyu05](https://clawhub.ai/user/ruoyu05)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and vision practitioners use this skill to select, install, configure, and run Ultralytics YOLO models for image and video detection, segmentation, classification, pose estimation, object tracking, and custom training workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence reports a runnable diagnostics script with a shell-injection risk.

Mitigation: Review scripts before execution and do not run scripts/check_environment.py until the shell=True path handling is fixed.

Risk: Installation examples may use mutable remote packages, GitHub @main installs, or container images.

Mitigation: Use a virtual environment, pin package versions and container digests, and avoid mutable install targets for managed deployments.

Risk: Generated YOLO outputs and environment reports can contain sensitive source media, model details, or system information.

Mitigation: Store outputs in approved locations, review reports before sharing, and keep third-party upload integrations disabled unless intentionally enabled.

## Reference(s):

- [Environment Check](references/environment_check.md)
- [Installation Guide](references/installation_guide.md)
- [Task Types](references/task_types.md)
- [Model Names](references/model_names.md)
- [Model Selection](references/model_selection.md)
- [Configuration Samples](references/configuration_samples.md)
- [Dataset Preparation](references/dataset_preparation.md)
- [Training Basics](references/training_basics.md)
- [Parameter Reference](references/parameter_reference.md)
- [Ultralytics Documentation](https://docs.ultralytics.com)
- [Ultralytics Configuration Reference](https://docs.ultralytics.com/usage/cfg/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline Python and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose workspace files, YOLO output folders, reports, model-selection guidance, and environment diagnostics.]

## Skill Version(s):

1.2.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
